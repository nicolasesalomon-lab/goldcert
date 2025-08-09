import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { Producto, ModeloProveedor, Proveedor, Fabrica, Certificado } from '../types';
const REQUIRED = ["TEST_REPORT","ETIQUETAS","MANUALES","MODELOS_MAP","OCC"];
const REQUIRED_SE_TIPO = ["DECL_IDENTIDAD","VERIF_IDENTIDAD"];
export default function Wizard(){
  const [products, setProducts] = useState<Producto[]>([]);
  const [mprov, setMprov] = useState<ModeloProveedor[]>([]);
  const [providers, setProviders] = useState<Proveedor[]>([]);
  const [factories, setFactories] = useState<Fabrica[]>([]);
  const [step, setStep] = useState(1);
  const [error, setError] = useState<string|null>(null);
  const [ok, setOk] = useState<string|null>(null);
  const [form, setForm] = useState<any>({
    producto_id: 0, tipo_certificacion_id: 1, ambito_certificado: 'tipo',
    modelo_proveedor_id: 0, fabrica_id: 0, fecha_emision: new Date().toISOString().slice(0,10), fecha_vencimiento: ''
  });
  useEffect(()=>{
    (async ()=>{
      setProducts(await api.listProducts());
      setMprov(await api.listModeloProveedor());
      setProviders(await api.listProviders());
      setFactories(await api.listFactories());
    })();
  },[]);
  const next = () => setStep(s => s+1);
  const prev = () => setStep(s => Math.max(1, s-1));
  const uploadAttachment = async (e:React.ChangeEvent<HTMLInputElement>, category:string) => {
    if(!e.target.files || e.target.files.length===0) return;
    setError(null); setOk(null);
    const file = e.target.files[0];
    const object_type = 'producto';
    const object_id = object_type==='producto' ? form.producto_id : form.modelo_proveedor_id;
    try{
      await api.uploadAttachment(object_type, object_id, category, file);
      setOk(`Adjunto ${category} cargado`);
    }catch(err:any){
      setError(err.message || 'Error subiendo adjunto');
    }
  };
  const submit = async () => {
    setError(null); setOk(null);
    try{
      const res = await api.createCertificate(form);
      setOk(`Certificado creado #${(res as Certificado).id}`);
      setStep(1);
    }catch(e:any){
      setError(e.message || 'Error creando certificado');
    }
  };
  const showPrereq = () => {
    const req = [...REQUIRED, ...(form.tipo_certificacion_id===1 && form.ambito_certificado==='tipo' ? REQUIRED_SE_TIPO : [])];
    return (
      <div className="grid gap-3">
        {req.map(cat => (
          <div key={cat} className="card p-3">
            <div className="font-medium">{cat}</div>
            <input type="file" onChange={(e)=>uploadAttachment(e, cat)} />
            <p className="subtle mt-1">Se adjunta al Producto seleccionado.</p>
          </div>
        ))}
      </div>
    );
  };
  return (
    <div className="grid gap-6">
      <h1 className="page-title">Wizard de Certificación</h1>
      {error && <p className="text-red-600 text-sm">{error}</p>}
      {ok && <p className="text-green-700 text-sm">{ok}</p>}
      {step===1 && (
        <div className="card p-5 grid gap-3">
          <h2 className="font-semibold">Paso 1 — Selección</h2>
          <select className="input" value={form.producto_id} onChange={e=>setForm({...form, producto_id:Number(e.target.value)})}>
            <option value="0">Producto...</option>
            {products.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
          <div className="grid sm:grid-cols-3 gap-3">
            <select className="input" value={form.tipo_certificacion_id} onChange={e=>setForm({...form, tipo_certificacion_id:Number(e.target.value)})}>
              <option value="1">SE</option>
              <option value="2">EE</option>
              <option value="3">ENACOM</option>
              <option value="4">INAL</option>
            </select>
            <select className="input" value={form.ambito_certificado??''} onChange={e=>setForm({...form, ambito_certificado: e.target.value || null})}>
              <option value="tipo">Ambito: tipo</option>
              <option value="marca">Ambito: marca</option>
              <option value="">(sin ámbito) ENACOM/INAL</option>
            </select>
            <select className="input" value={form.modelo_proveedor_id} onChange={e=>setForm({...form, modelo_proveedor_id:Number(e.target.value)})}>
              <option value="0">Modelo proveedor...</option>
              {mprov.filter(m=>m.producto_id===form.producto_id).map(m => <option key={m.id} value={m.id}>{m.codigo_proveedor}</option>)}
            </select>
          </div>
          <div className="flex gap-2">
            <button className="btn btn-primary" disabled={!form.producto_id || !form.modelo_proveedor_id} onClick={next}>Siguiente</button>
          </div>
        </div>
      )}
      {step===2 && (
        <div className="card p-5 grid gap-3">
          <h2 className="font-semibold">Paso 2 — Fábrica</h2>
          <select className="input" value={form.fabrica_id} onChange={e=>setForm({...form, fabrica_id:Number(e.target.value)})}>
            <option value="0">Fábrica...</option>
            {factories.map(f => <option key={f.id} value={f.id}>#{f.id} · Prov {f.proveedor_id}</option>)}
          </select>
          <div className="grid sm:grid-cols-2 gap-3">
            <label className="label">Fecha emisión</label>
            <input className="input" type="date" value={form.fecha_emision} onChange={e=>setForm({...form, fecha_emision:e.target.value})} />
            <label className="label">Fecha vencimiento (opcional)</label>
            <input className="input" type="date" value={form.fecha_vencimiento} onChange={e=>setForm({...form, fecha_vencimiento:e.target.value})} />
          </div>
          <div className="flex gap-2">
            <button className="btn btn-outline" onClick={prev}>Atrás</button>
            <button className="btn btn-primary" disabled={!form.fabrica_id} onClick={next}>Siguiente</button>
          </div>
        </div>
      )}
      {step===3 && (
        <div className="card p-5 grid gap-3">
          <h2 className="font-semibold">Paso 3 — Prerrequisitos</h2>
          {showPrereq()}
          <div className="flex gap-2">
            <button className="btn btn-outline" onClick={prev}>Atrás</button>
            <button className="btn btn-primary" onClick={next}>Continuar</button>
          </div>
        </div>
      )}
      {step===4 && (
        <div className="card p-5 grid gap-3">
          <h2 className="font-semibold">Paso 4 — Confirmación</h2>
          <p className="subtle">Se validarán prerrequisitos y auditoría (si ámbito = marca).</p>
          <div className="flex gap-2">
            <button className="btn btn-outline" onClick={prev}>Atrás</button>
            <button className="btn btn-primary" onClick={submit}>Emitir certificado</button>
          </div>
        </div>
      )}
    </div>
  );
}
