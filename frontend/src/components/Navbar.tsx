import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
export default function Navbar(){
  const { user, logout } = useAuth();
  const nav = useNavigate();
  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="container flex items-center justify-between py-3">
        <Link to="/" className="flex items-center gap-2">
          <span className="font-semibold text-lg">GoldCert v2</span>
        </Link>
        <div className="flex items-center gap-4">
          <Link className="text-gray-700 hover:text-brand-600" to="/providers">Proveedores</Link>
          <Link className="text-gray-700 hover:text-brand-600" to="/products">Productos</Link>
          <Link className="text-gray-700 hover:text-brand-600" to="/wizard">Wizard Cert.</Link>
          <Link className="text-gray-700 hover:text-brand-600" to="/alerts">Alertas</Link>
          <Link className="text-gray-700 hover:text-brand-600" to="/djc">DJC</Link>
          {!!user && <span className="badge">{user.email} · {user.role}</span>}
          {!!user ? <button className="btn btn-outline" onClick={()=>{logout(); nav('/login')}}>Salir</button> : <Link className="btn btn-primary" to="/login">Ingresar</Link>}
        </div>
      </div>
    </nav>
  );
}
