import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import WebDeveloper from '../Assets/WebDeveloper.png';

export default function Login() {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const navigate = useNavigate(); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(credentials)
      });
  
      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.detail || 'Login failed');
      }
  
      const { access_token, hospital_id } = await response.json();
      // Store the access token in localStorage or sessionStorage
      localStorage.setItem('accessToken', access_token);
      // Redirect to dashboard
      navigate(`/dashboard/${hospital_id}`);
    } catch (error) {
      alert(error.message || "Something went wrong. Please try again.");
    }
  };

  const onChange = (event) =>
    setCredentials({ ...credentials, [event.target.name]: event.target.value });

  return (
    <>
      <Navbar />
      <section className="vh-100 d-flex justify-content-center align-items-center banner_part">
        <div className="container">
          <div className="row justify-content-start">
            <div className="col-md-6">
              <img src={WebDeveloper} alt="Web Developer" className="login-image" />
            </div>
            <div className="col-md-6 contents">
              <div className="row justify-content-center ">
                <div className="col-md-8">
                  <div className="mb-4">
                    <h3>Log In</h3>
                    <p className="mb-4">
                      Log in to OCRxAI and simplify your medical record management.
                      {/* <strong> For testing, use the placeholders as credentials in the username and password.</strong> */}
                    </p>
                  </div>
                  <form onSubmit={handleSubmit}>
                    <div className="form-group first">
                      <label htmlFor="username">Username</label>
                      <input
                        type="text"
                        className="form-control"
                        id="username"
                        name="username"
                        value={credentials.username}
                        onChange={onChange}
                        placeholder="Hospital1_admin"
                      />
                    </div>
                    <div className="form-group last mb-4">
                      <label htmlFor="password">Password</label>
                      <input
                        type="password"
                        className="form-control"
                        id="password"
                        name="password"
                        value={credentials.password}
                        onChange={onChange}
                        placeholder="password123"
                      />
                    </div>
                    <button type="submit" className="btn btn-block btn-primary">Log In</button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
