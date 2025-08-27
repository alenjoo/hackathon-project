import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState('');
  
  const [formData, setFormData] = useState({
    serviceType: '',
    description: '',
    feeAmount: '',
  });
  const [requests, setRequests] = useState([]);

  const accessToken = localStorage.getItem('accessToken');

  useEffect(() => {
    const email = localStorage.getItem('userEmail');
    const role = localStorage.getItem('userRole');

    if (!accessToken || role !== 'Citizen') {
      navigate('/login');
    } else {
      setUserEmail(email);
     
      fetchRequests();
    }
  }, [navigate]);

  const fetchRequests = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/requests/mine', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Failed to fetch requests:', text);
        return;
      }

      const data = await res.json();
      setRequests(data);
    } catch (err) {
      console.error('Error fetching requests:', err);
    }
  };

  const SERVICE_FEES = {
    "Birth Certificate": 100.00,
    "Address Change": 50.00,
    "Income Certificate": 75.00,
  };

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
      feeAmount: name === "serviceType" ? SERVICE_FEES[value] || '' : prev.feeAmount
    }));
  };

const handleSubmit = async e => {
  e.preventDefault();

  const options = {
    key: 'rzp_test_NsB3oPpNOVdgRa', // Your Razorpay test key
    amount: formData.feeAmount * 100, // Convert to paise
    currency: 'INR',
    name: 'GovTech Portal',
    description: formData.serviceType,
    handler: function (response) {
      alert('Payment successful! Razorpay Payment ID: ' + response.razorpay_payment_id);
      // You can optionally log this or trigger a backend call here
    },
    prefill: {
      email: userEmail,
    },
    theme: {
      color: '#005ea2',
    },
  };

  const rzp = new window.Razorpay(options);
  rzp.open();
};


  const handleLogout = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  return (
    <div className="dashboard-container">
      <nav className="dashboard-nav">
        <h1>GovTech Portal</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </nav>

      <main className="dashboard-content">
        <h2>Welcome, {userEmail}</h2>
       

        <section className="request-form">
          <h3>Create New Service Request</h3>
          <form onSubmit={handleSubmit}>
            <label>
              Service Type:
              <select name="serviceType" value={formData.serviceType} onChange={handleChange} required>
                <option value="">Select</option>
                <option value="Birth Certificate">Birth Certificate</option>
                <option value="Address Change">Address Change</option>
                <option value="Income Certificate">Income Certificate</option>
              </select>
            </label>

            <label>
              Description:
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
              />
            </label>

            <label>
              Fee Amount:
              <input
                type="number"
                name="feeAmount"
                value={formData.feeAmount}
                readOnly
              />
            </label>

            <button type="submit">Submit Request</button>
          </form>
        </section>

        <section className="request-list">
          <h3>My Requests</h3>
          <table>
            <thead>
              <tr>
                <th>Service Type</th>
                <th>Description</th>
                <th>Fee</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(req => (
                <tr key={req.RequestID}>
                  <td>{req.ServiceType}</td>
                  <td>{req.Description}</td>
                  <td>{req.FeeAmount}</td>
                  <td>{req.Status}</td>
                  <td>{new Date(req.CreatedAt).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
