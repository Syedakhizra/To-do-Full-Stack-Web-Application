'use client';

import React, { useState } from 'react';
import LoginForm from '../components/auth/LoginForm';
import SignupForm from '../components/auth/SignupForm';

const LoginPage: React.FC = () => {
  const [isLoginView, setIsLoginView] = useState(true);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      {isLoginView ? (
        <LoginForm onSwitchToSignup={() => setIsLoginView(false)} />
      ) : (
        <SignupForm onSwitchToLogin={() => setIsLoginView(true)} />
      )}
    </div>
  );
};

export default LoginPage;