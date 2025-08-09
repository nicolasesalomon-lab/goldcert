import React, { createContext, useContext, useEffect, useState } from 'react';
import { api } from './api';
import type { User } from '../types';
type AuthContextType = { user: User | null; token: string | null; login: (email:string, password:string)=>Promise<void>; logout:()=>void; };
const AuthContext = createContext<AuthContextType | null>(null);
export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  useEffect(() => {
    api.setToken(token);
    if (token) {
      api.me().then(setUser).catch(() => { setUser(null); setToken(null); localStorage.removeItem('token'); });
    }
  }, [token]);
  const login = async (email:string, password:string) => {
    const res = await api.login(email, password);
    const t = res.access_token as string;
    setToken(t); localStorage.setItem('token', t); api.setToken(t);
    const me = await api.me(); setUser(me as User);
  };
  const logout = () => { setUser(null); setToken(null); localStorage.removeItem('token'); api.setToken(null); };
  return <AuthContext.Provider value={{ user, token, login, logout }}>{children}</AuthContext.Provider>;
};
export const useAuth = () => { const ctx = useContext(AuthContext); if(!ctx) throw new Error('useAuth must be used within AuthProvider'); return ctx; };
