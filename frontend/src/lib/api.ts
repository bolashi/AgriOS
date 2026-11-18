const BASE=import.meta.env.VITE_API_BASE_URL||''
export async function api<T>(path:string,init?:RequestInit):Promise<T>{const r=await fetch(`${BASE}/api${path}`,init);const data=await r.json();if(!r.ok)throw new Error(data.detail||'Request failed');return data as T}
