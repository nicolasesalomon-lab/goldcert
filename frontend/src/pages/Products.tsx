import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { Proveedor, Producto, ModeloProveedor, ModeloProducto } from '../types';
export default function Products(){
  const [providers, setProviders] = useState<Proveedor[]>([]);
  const [products, setProducts] = useState<Producto[]>([]);
  const [mp, setMp] = useState<ModeloProveedor[]>([]);
  const [mm, setMm] = useState<ModeloProducto[]>([]);
  const [productForm, setProductForm] = useState({ nombre:'', categoria:'', marca:'', origen:'', proveedor_id:0 });
  const [mpForm, setMpForm] = useState({ producto_id:0, codigo_proveedor:'' });
  const [mmForm, setMmForm] = useState({ modelo_proveedor_id:0, codigo_goldmund:'' });
  const load = async () => {
    setProviders(await api.listProviders());
    setProducts(await api.listProducts());
    setMp(await api.listModeloProveedor());
    setMm(await api.listModeloProducto());
  };
  useEffect(()=>{ load(); },[]);
  const createProduct = async (e:React.FormEvent) => { e.preventDefault(); await api.createProduct(productForm); setProductForm({nombre:'',categoria:'',marca:'',origen:'',proveedor_id:0}); await load(); };
  const createMp = async (e:React.FormEvent) => { e.preventDefault(); await api.createModeloProveedor(mpForm); setMpForm({producto_id:0,codigo_proveedor:''}); await load(); };
  const createMm = async (e:React.FormEvent) => { e.preventDefault(); await api.createModeloProducto(mmForm); setMmForm({modelo_proveedor_id:0,codigo_goldmund:''}); await load(); };
  return (
    <div className="grid gap-6">
      <div className="card p-5">
        <h1 className="page-title mb-3">Productos</h1>
        <form onSubmit={createProduct} className="grid gap-3 sm:grid-cols-5">
          <input className="input" placeholder="Nombre" value={productForm.nombre} onChange={e=>setProductForm({...productForm, nombre:e.target.value})} />
          <input className="input" placeholder="Categoría" value={productForm.categoria} onChange={e=>setProductForm({...productForm, categoria:e.target.value})} />
          <input className="input" placeholder="Marca" value={productForm.marca} onChange={e=>setProductForm({...productForm, marca:e.target.value})} />
          <input className="input" placeholder="Origen" value={productForm.origen} onChange={e=>setProductForm({...productForm, origen:e.target.value})} />
          <select className="input" value={productForm.proveedor_id} onChange={e=>setProductForm({...productForm, proveedor_id:Number(e.target.value)})}>
            <option value="0">Proveedor...</option>
            {providers.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
          <button className="btn btn-primary col-span-full">Crear producto</button>
        </form>
      </div>
      <div className="card p-5">
        <h2 className="font-semibold mb-3">Modelos (Proveedor)</h2>
        <form onSubmit={createMp} className="grid gap-3 sm:grid-cols-3">
          <select className="input" value={mpForm.producto_id} onChange={e=>setMpForm({...mpForm, producto_id:Number(e.target.value)})}>
            <option value="0">Producto...</option>
            {products.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
          <input className="input" placeholder="Código proveedor (type)" value={mpForm.codigo_proveedor} onChange={e=>setMpForm({...mpForm, codigo_proveedor:e.target.value})} />
          <button className="btn btn-primary">Crear</button>
        </form>
        <div className="grid gap-2 mt-3">{mp.map(m => <div key={m.id} className="card p-3">#{m.id} · Prod {m.producto_id} · {m.codigo_proveedor}</div>)}</div>
      </div>
      <div className="card p-5">
        <h2 className="font-semibold mb-3">Modelos (Producto)</h2>
        <form onSubmit={createMm} className="grid gap-3 sm:grid-cols-3">
          <select className="input" value={mmForm.modelo_proveedor_id} onChange={e=>setMmForm({...mmForm, modelo_proveedor_id:Number(e.target.value)})}>
            <option value="0">Modelo proveedor...</option>
            {mp.map(m => <option key={m.id} value={m.id}>#{m.id} · {m.codigo_proveedor}</option>)}
          </select>
          <input className="input" placeholder="Código Goldmund" value={mmForm.codigo_goldmund} onChange={e=>setMmForm({...mmForm, codigo_goldmund:e.target.value})} />
          <button className="btn btn-primary">Crear</button>
        </form>
        <div className="grid gap-2 mt-3">{mm.map(m => <div key={m.id} className="card p-3">#{m.id} · MP {m.modelo_proveedor_id} · {m.codigo_goldmund}</div>)}</div>
      </div>
    </div>
  );
}
