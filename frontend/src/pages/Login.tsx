import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
export default function Login(){
  const [email, setEmail] = useState('admin@test.com');
  const [password, setPassword] = useState('admin');
  const [err, setErr] = useState<string|null>(null);
  const nav = useNavigate();
  const { login } = useAuth();
  const submit = async (e:React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    try { await login(email, password); nav('/'); }
    catch(e:any){ setErr(e.message || 'Error'); }
  };
  return (
    <div className="max-w-md mx-auto mt-12 card p-6">
      <h1 className="page-title mb-4">Ingresar</h1>
      <form onSubmit={submit} className="grid gap-3">
        <input className="input" placeholder="Email" type="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="input" placeholder="Contraseña" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        {err && <p className="text-red-600 text-sm">{err}</p>}
        <button className="btn btn-primary">Entrar</button>
      </form>
      <p className="subtle mt-2">Demo: admin@test.com / admin</p>
    </div>
  );
}
