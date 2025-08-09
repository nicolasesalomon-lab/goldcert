import React from 'react';
import Navbar from './Navbar';
export default function Layout({children}:{children:React.ReactNode}){
  return (<div className="min-h-screen bg-neutral-50"><Navbar/><main className="container py-6">{children}</main></div>);
}
