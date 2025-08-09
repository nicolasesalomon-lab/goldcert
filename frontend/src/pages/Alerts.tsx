import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
export default function Alerts(){
  const [data, setData] = useState<any>({certificados:[], auditorias:[], sugerencias:[]});
  useEffect(()=>{ api.getAlerts().then(setData); },[]);
  return (
    <div className="grid gap-6">
      <div className="card p-5">
        <h1 className="page-title mb-3">Alertas</h1>
        <h2 className="font-semibold mb-2">Certificados</h2>
        <div className="grid gap-2">
          {data.certificados.map((c:any)=>(
            <div key={c.id} className="card p-3 flex items-center justify-between">
              <div>#{c.id} · Prod {c.producto_id} · Estado: <b>{c.status}</b> · vence en {c.vence_en_dias} días</div>
            </div>
          ))}
          {data.certificados.length===0 && <p className="subtle">Sin alertas.</p>}
        </div>
      </div>
      <div className="card p-5">
        <h2 className="font-semibold mb-2">Auditorías</h2>
        <div className="grid gap-2">
          {data.auditorias.map((a:any)=>(
            <div key={a.id} className="card p-3">#{a.id} · Fabr {a.fabrica_id} · vence en {a.vence_en_dias} días</div>
          ))}
          {data.auditorias.length===0 && <p className="subtle">Sin alertas.</p>}
        </div>
      </div>
      <div className="card p-5">
        <h2 className="font-semibold mb-2">Sugerencias</h2>
        <div className="grid gap-2">
          {data.sugerencias.map((s:any, idx:number)=>(
            <div key={idx} className="card p-3">• {s.tipo} {s.certificado_id ? `(cert #${s.certificado_id})` : ''}</div>
          ))}
          {data.sugerencias.length===0 && <p className="subtle">Sin sugerencias por ahora.</p>}
        </div>
      </div>
    </div>
  );
}
