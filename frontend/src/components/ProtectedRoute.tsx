import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
export default function ProtectedRoute({children}:{children:JSX.Element}){
  const { token } = useAuth();
  if(!token) return <Navigate to="/login" replace />;
  return children;
}
