const API_URL = "http://localhost:8000"; 

export async function getReservas() {
  const res = await fetch(`${API_URL}/api/reservas/`);
  return await res.json();
}

export async function createReserva(data) {
  const res = await fetch(`${API_URL}/api/reservas/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await res.json();
}
