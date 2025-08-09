import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { Proveedor, Fabrica, Auditoria } from '../types';
export default function Providers(){
  const [items, setItems] = useState<Proveedor[]>([]);
  const [form, setForm] = useState({ nombre:'', contacto_email:'', contacto_telefono:'' });
  const [fabrica, setFabrica] = useState({ proveedor_id:0, direccion:'' });
  const [audit, setAudit] = useState({ fabrica_id:0, fecha_auditoria:'', fecha_vencimiento:'' });
  const [factories, setFactories] = useState<Fabrica[]>([]);
  const [audits, setAudits] = useState<Auditoria[]>([]);
  const [err, setErr] = useState<string|null>(null);
  const load = async () => {
    setItems(await api.listProviders() as Proveedor[]);
    setFactories(await api.listFactories() as Fabrica[]);
    setAudits(await api.listAudits() as Auditoria[]);
  };
  useEffect(()=>{ load(); },[]);
  const createProv = async (e:React.FormEvent)=>{
    e.preventDefault(); setErr(null);
    if(!form.nombre.trim()) return setErr('Nombre obligatorio');
    await api.createProvider(form);
    setForm({nombre:'',contacto_email:'',contacto_telefono:''}); await load();
  };
  const createFab = async (e:React.FormEvent)=>{
    e.preventDefault(); setErr(null);
    if(!fabrica.proveedor_id) return setErr('Elegí proveedor');
    await api.createFactory(fabrica); setFabrica({proveedor_id:0, direccion:''}); await load();
  };
  const createAudit = async (e:React.FormEvent)=>{
    e.preventDefault(); setErr(null);
    if(!audit.fabrica_id) return setErr('Elegí fábrica');
    await api.createAudit(audit); setAudit({fabrica_id:0, fecha_auditoria:'', fecha_vencimiento:''}); await load();
  };
  return (
    <div className="grid gap-6">
      <div className="card p-5">
        <h1 className="page-title mb-3">Proveedores</h1>
        <form onSubmit={createProv} className="grid gap-3 sm:grid-cols-4">
          <input className="input" placeholder="Nombre" value={form.nombre} onChange={e=>setForm({...form, nombre:e.target.value})} />
          <input className="input" placeholder="Email" value={form.contacto_email} onChange={e=>setForm({...form, contacto_email:e.target.value})} />
          <input className="input" placeholder="Teléfono" value={form.contacto_telefono} onChange={e=>setForm({...form, contacto_telefono:e.target.value})} />
          <button className="btn btn-primary">Cargar proveedor</button>
        </form>
      </div>
      <div className="card p-5">
        <h2 className="font-semibold mb-3">Fábricas</h2>
        <form onSubmit={createFab} className="grid gap-3 sm:grid-cols-3">
          <select className="input" value={fabrica.proveedor_id} onChange={e=>setFabrica({...fabrica, proveedor_id: Number(e.target.value)})}>
            <option value="0">Proveedor...</option>
            {items.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
          <input className="input" placeholder="Dirección" value={fabrica.direccion} onChange={e=>setFabrica({...fabrica, direccion:e.target.value})} />
          <button className="btn btn-primary">Agregar fábrica</button>
        </form>
        <div className="grid gap-2 mt-3">
          {factories.map(f => <div key={f.id} className="card p-3 flex items-center justify-between"><div>#{f.id} · Prov {f.proveedor_id} · {f.direccion||'—'}</div></div>)}
        </div>
      </div>
      <div className="card p-5">
        <h2 className="font-semibold mb-3">Auditorías</h2>
        <form onSubmit={createAudit} className="grid gap-3 sm:grid-cols-4">
          <select className="input" value={audit.fabrica_id} onChange={e=>setAudit({...audit, fabrica_id: Number(e.target.value)})}>
            <option value="0">Fábrica...</option>
            {factories.map(f => <option key={f.id} value={f.id}>#{f.id} · Prov {f.proveedor_id}</option>)}
          </select>
          <input className="input" type="date" value={audit.fecha_auditoria} onChange={e=>setAudit({...audit, fecha_auditoria:e.target.value})} />
          <input className="input" type="date" value={audit.fecha_vencimiento} onChange={e=>setAudit({...audit, fecha_vencimiento:e.target.value})} />
          <button className="btn btn-primary">Agregar auditoría</button>
        </form>
        <div className="grid gap-2 mt-3">
          {audits.map(a => <div key={a.id} className="card p-3 flex items-center justify-between"><div>#{a.id} · Fabr {a.fabrica_id} · {a.fecha_auditoria} → {a.fecha_vencimiento}</div></div>)}
        </div>
        {err && <p className="text-red-600 text-sm mt-2">{err}</p>}
      </div>
    </div>
  );
}
