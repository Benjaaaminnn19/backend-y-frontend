import { useEffect, useState } from "react";
import { getReservas, createReserva } from "./api";

function App() {
  const [reservas, setReservas] = useState([]);
  const [nombre, setNombre] = useState("");

  useEffect(() => {
    getReservas().then((data) => setReservas(data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const nueva = await createReserva({ nombre });
    setReservas([...reservas, nueva]);
    setNombre("");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Reservas desde Django API</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nombre reserva"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
        <button type="submit">Agregar</button>
      </form>

      <h2>Lista de Reservas</h2>
      <ul>
        {reservas.map((r) => (
          <li key={r.id}>{r.nombre}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
