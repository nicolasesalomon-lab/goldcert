import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom'
import './index.css'
import { AuthProvider } from './lib/auth'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Providers from './pages/Providers'
import Products from './pages/Products'
import Wizard from './pages/Wizard'
import Alerts from './pages/Alerts'
import DJC from './pages/DJC'
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
            <Route path="/providers" element={<ProtectedRoute><Providers/></ProtectedRoute>} />
            <Route path="/products" element={<ProtectedRoute><Products/></ProtectedRoute>} />
            <Route path="/wizard" element={<ProtectedRoute><Wizard/></ProtectedRoute>} />
            <Route path="/alerts" element={<ProtectedRoute><Alerts/></ProtectedRoute>} />
            <Route path="/djc" element={<ProtectedRoute><DJC/></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
)
