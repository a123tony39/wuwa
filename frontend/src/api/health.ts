const API_BASE = import.meta.env.VITE_API_BASE

export interface HealthResponse {
  status: string
  message: string
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/api/health`)

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`)
  }

  return res.json()
}