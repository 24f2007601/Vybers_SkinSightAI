# Running SkinSight-AI with Cloudflare Tunnel

Run the app locally on your machine and share a secure, public HTTPS link with anyone via Cloudflare's free edge network. No port forwarding, no router setup, and no paid hosting needed.

---

## Prerequisites

1. Install Cloudflare Tunnel (`cloudflared`):
   - **Windows (PowerShell)**:
     ```powershell
     winget install Cloudflare.cloudflared
     ```
   - **macOS (Homebrew)**:
     ```bash
     brew install cloudflared
     ```
   - **Linux**:
     ```bash
     curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
     sudo dpkg -i cloudflared.deb
     ```

---

## Step-by-Step Instructions

### Step 1: Start the Backend (Terminal 1)
```powershell
# Activate your virtual environment if using one
uvicorn src.api.main:app --port 8000
```
Backend will be listening on `http://localhost:8000`.

### Step 2: Start the Frontend (Terminal 2)
```powershell
cd frontend
npm install
npm run dev
```
Frontend will be running on `http://localhost:5173`.

---

### Step 3: Launch Cloudflare Tunnel (Terminal 3)

Run the tunnel command pointing to your frontend:
```powershell
cloudflared tunnel --url http://localhost:5173
```

You will see output similar to:
```text
2026-11-24T02:00:00Z INF +--------------------------------------------------------------------------------------------+
2026-11-24T02:00:00Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2026-11-24T02:00:00Z INF |  https://temporary-subdomain.trycloudflare.com                                             |
2026-11-24T02:00:00Z INF +--------------------------------------------------------------------------------------------+
```

Copy the `https://*.trycloudflare.com` URL and open it in any browser or share it with judges/users.

---

## Alternative: Single Container via Docker + Cloudflare

If you are running the unified Docker container:
```powershell
# 1. Build & run container
docker build -t skinsight-ai .
docker run -p 8000:8000 skinsight-ai

# 2. Expose the unified container (serves both React & FastAPI on 8000)
cloudflared tunnel --url http://localhost:8000
```
Visit the generated `.trycloudflare.com` URL.
