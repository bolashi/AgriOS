# Deployment notes

- Backend: deploy the `backend` folder to Hugging Face Spaces (Docker) or a Python host.
  CPU inference may be slow and free services may have memory limits/cold starts.
- Frontend: deploy `frontend/dist` to Netlify or Vercel and set `VITE_API_BASE_URL`
  to the public backend URL.
- v0.1 uses localStorage in each browser. v0.2 can replace `src/lib/store.ts` with
  a Supabase-backed repository and authentication.
- Never commit `.env`, API keys, or model weights.
