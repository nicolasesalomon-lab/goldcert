import React from 'react';
export default function Dashboard(){
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div className="card p-5"><h3 className="font-semibold mb-1">Bienvenido</h3><p className="subtle">Usá la barra para navegar.</p></div>
      <div className="card p-5"><h3 className="font-semibold mb-1">Certificados</h3><p className="subtle">Wizard y alertas disponibles.</p></div>
      <div className="card p-5"><h3 className="font-semibold mb-1">DJC</h3><p className="subtle">Generá declaraciones y descarga PDF.</p></div>
    </div>
  );
}
