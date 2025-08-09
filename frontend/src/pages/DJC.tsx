import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { ModeloProducto } from '../types';
export default function DJC(){
  const [djcId, setDjcId] = useState<number| null>(null);
  const [mm, setMm] = useState<ModeloProducto[]>([]);
  const [selected, setSelected] = useState<number>(0);
  const [ok, setOk] = useState<string|null>(null);
  const [err, setErr] = useState<string|null>(null);
  useEffect(()=>{ api.listModeloProducto().then(setMm as any); },[]);
  const create = async ()=>{
    setErr(null); setOk(null);
    try{
      const djc = await api.createDJC();
      setDjcId(djc.id);
      setOk(`DJC creada: ${djc.numero}`);
    }catch(e:any){ setErr(e.message || 'Error'); }
  };
  const add = async ()=>{
    if(!djcId || !selected) return;
    setErr(null); setOk(null);
    try{ await api.addModeloToDJC(djcId, selected); setOk('Modelo agregado'); }
    catch(e:any){ setErr(e.message || 'Error'); }
  };
  const pdf = ()=>{ if(djcId) api.getDJCPdf(djcId); };
  return (
    <div className="grid gap-6">
      <h1 className="page-title">Declaración Jurada (DJC)</h1>
      {ok && <p className="text-green-700 text-sm">{ok}</p>}
      {err && <p className="text-red-700 text-sm">{err}</p>}
      <div className="card p-5 flex gap-3 items-center">
        <button className="btn btn-primary" onClick={create}>Crear DJC</button>
        {djcId && <><select className="input" value={selected} onChange={e=>setSelected(Number(e.target.value))}>
          <option value="0">Modelo producto...</option>
          {mm.map(m => <option key={m.id} value={m.id}>#{m.id} · MP {m.modelo_proveedor_id} · {m.codigo_goldmund}</option>)}
        </select>
        <button className="btn btn-outline" onClick={add}>Agregar modelo</button>
        <button className="btn btn-outline" onClick={pdf}>Descargar PDF</button></>}
      </div>
    </div>
  );
}
