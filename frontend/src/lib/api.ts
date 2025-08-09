const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
export class API {
  token: string | null;
  constructor(token: string | null) { this.token = token; }
  setToken(t: string | null) { this.token = t; }
  async request(path: string, options: RequestInit = {}) {
    const headers: any = { ...(options.headers || {}) };
    if (!(options.body instanceof FormData)) headers['Content-Type'] = 'application/json';
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
    const res = await fetch(`${API_URL}${path}`, { ...options, headers });
    if (!res.ok) { throw new Error(await res.text()); }
    const ct = res.headers.get('content-type') || '';
    return ct.includes('application/json') ? res.json() : res.text();
  }
  async login(email:string, password:string) { return this.request('/auth/login', { method:'POST', body: JSON.stringify({email,password})}); }
  async me() { return this.request('/auth/me'); }
  listProviders(){ return this.request('/v2/providers/'); }
  createProvider(data:any){ return this.request('/v2/providers/', { method:'POST', body: JSON.stringify(data)}); }
  listFactories(){ return this.request('/v2/factories/'); }
  createFactory(data:any){ return this.request('/v2/factories/', { method:'POST', body: JSON.stringify(data)}); }
  listAudits(){ return this.request('/v2/audits/'); }
  createAudit(data:any){ return this.request('/v2/audits/', { method:'POST', body: JSON.stringify(data)}); }
  listProducts(){ return this.request('/v2/products/'); }
  createProduct(data:any){ return this.request('/v2/products/', { method:'POST', body: JSON.stringify(data)}); }
  listModeloProveedor(){ return this.request('/v2/models/proveedor'); }
  createModeloProveedor(data:any){ return this.request('/v2/models/proveedor', { method:'POST', body: JSON.stringify(data)}); }
  listModeloProducto(){ return this.request('/v2/models/producto'); }
  createModeloProducto(data:any){ return this.request('/v2/models/producto', { method:'POST', body: JSON.stringify(data)}); }
  createCertificate(data:any){ return this.request('/v2/certificates/', { method:'POST', body: JSON.stringify(data)}); }
  listCertificates(){ return this.request('/v2/certificates/', { method:'GET' }); }
  getAlerts(){ return this.request('/v2/alerts/'); }
  async uploadAttachment(object_type:string, object_id:number, category:string, file:File){
    if(!this.token) throw new Error('No token');
    const form = new FormData();
    form.append('object_type', object_type);
    form.append('object_id', String(object_id));
    form.append('category', category);
    form.append('file', file);
    const res = await fetch(`${API_URL}/v2/attachments/upload`, { method:'POST', headers: { Authorization: `Bearer ${this.token}` }, body: form });
    if(!res.ok) throw new Error(await res.text());
    return res.json();
  }
  createDJC(){ return this.request('/v2/djc/', { method:'POST' }); }
  addModeloToDJC(djc_id:number, modelo_id:number){ return this.request(`/v2/djc/${djc_id}/add-modelo/${modelo_id}`, { method:'POST' }); }
  getDJCPdf(djc_id:number){ window.open(`${API_URL}/v2/djc/${djc_id}/pdf`, '_blank'); }
}
export const api = new API(localStorage.getItem('token'));
