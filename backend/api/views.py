
import os
import json
import uuid
import hashlib


from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


import razorpay
from decouple import config


from api.models import User, Role, ServiceRequest, PaymentTransaction
from api.constants import SERVICE_FEES


@api_view(['GET'])
def health(request):
    return JsonResponse({"status": "ok"})


@api_view(['POST'])
def signup(request):
    data = request.data
    required_fields = ['name', 'email', 'mobile', 'password']

    for field in required_fields:
        if not data.get(field):
            return Response({'detail': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    if len(data['password']) < 8:
        return Response({'detail': 'Password must be at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(Email=data['email']).exists():
        return Response({'detail': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        salt = os.urandom(32).hex()
        salted_password = data['password'] + salt
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()

        citizen_role = Role.objects.get(RoleName='Citizen')

        user = User.objects.create(
            Name=data['name'],
            Email=data['email'],
            Mobile=data['mobile'],
            Salt=salt,
            PasswordHash=password_hash,
            Role=citizen_role
        )

        return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)

    except Role.DoesNotExist:
        return Response({'detail': 'Citizen role not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except IntegrityError:
        return Response({'detail': 'Database error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(Email=email)
        salted = password + user.Salt
        hashed = hashlib.sha256(salted.encode()).hexdigest()

        if hashed != user.PasswordHash:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.Role.RoleName
        refresh['email'] = user.Email

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'name': user.Name,
                'email': user.Email,
                'role': user.Role.RoleName
            }
        })

    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def payment_health(request):
    try:
        key_id = config("RAZORPAY_KEY_ID")
        key_secret = config("RAZORPAY_KEY_SECRET")
        secret_key = config("RAZORPAY_SECRET_KEY")

        if not key_id or not key_secret or not secret_key:
            return JsonResponse({"status": "Missing keys"}, status=500)

        return JsonResponse({"status": "OK", "gateway": "Razorpay Sandbox"})

    except Exception as e:
        return JsonResponse({"status": "Error", "detail": str(e)}, status=500)


@api_view(['POST'])
def create_order(request):
    try:
        data = json.loads(request.body)
        service_type = data.get("serviceType")
        description = data.get("description")
        fee_amount = float(data.get("requestFee"))

        expected_fee = SERVICE_FEES.get(service_type)
        if expected_fee != fee_amount:
            return JsonResponse({"error": "Fee mismatch"}, status=403)

        user_id = request.headers.get("X-User-ID")
        user = User.objects.get(UserID=user_id)

        idempotency_key = f"{user.UserID}_{service_type}_{uuid.uuid4().hex[:6]}"
        client = razorpay.Client(auth=(config("RAZORPAY_KEY_ID"), config("RAZORPAY_KEY_SECRET")))

        order = client.order.create({
            "amount": int(fee_amount * 100),
            "currency": "INR",
            "receipt": f"req_{uuid.uuid4().hex}",
            "payment_capture": 1
        })

        PaymentTransaction.objects.create(
            User=user,
            Amount=fee_amount,
            Currency="INR",
            OrderId=order["id"],
            Status="Pending",
            GatewayResponse=order,
            IdempotencyKey=idempotency_key
        )

        return JsonResponse({"order_id": order["id"], "amount": fee_amount})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
def create_service_request(request):
    try:
        data = json.loads(request.body)
        service_type = data.get("serviceType")
        description = data.get("description")
        fee_amount = float(data.get("feeAmount"))
        order_id = data.get("orderId")
        payment_id = data.get("paymentId")
        signature = data.get("signature")

        expected_fee = SERVICE_FEES.get(service_type)
        if expected_fee != fee_amount:
            return JsonResponse({"error": "Fee tampering detected"}, status=403)

        user_id = request.headers.get("X-User-ID")
        user = User.objects.get(UserID=user_id)

        txn = PaymentTransaction.objects.filter(OrderId=order_id, User=user).first()
        if not txn:
            return JsonResponse({"error": "Transaction not found"}, status=404)

        txn.PaymentId = payment_id
        txn.Signature = signature
        txn.Status = "Success"
        txn.save()

        sr = ServiceRequest.objects.create(
            User=user,
            ServiceType=service_type,
            Description=description,
            FeeAmount=fee_amount,
            Status="Paid"
        )

        return JsonResponse({"message": "Request created successfully", "RequestID": sr.RequestID})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
def get_user_requests(request):
    email = request.headers.get("X-User-Email") or request.user.Email
    user = User.objects.get(Email=email)

    requests = ServiceRequest.objects.filter(User=user).order_by('-CreatedAt')
    data = [{
        "RequestID": r.RequestID,
        "ServiceType": r.ServiceType,
        "Description": r.Description,
        "FeeAmount": float(r.FeeAmount),
        "Status": r.Status,
        "CreatedAt": r.CreatedAt.isoformat()
    } for r in requests]
    return Response(data)
