import { useEffect, useState } from "react";
import "./ReservasApp.css";

const API_URL = "http://localhost:8000";

function App() {
  const [reservas, setReservas] = useState([]);
  const [mesas, setMesas] = useState([]);
  const [editando, setEditando] = useState(null);
  const [formData, setFormData] = useState({
    nombre: "",
    telefono: "",
    fecha: "",
    hora: "",
    numero_personas: 1,
    estado: "RESERVADO",
    mesa_id: "",
    observacion: ""
  });

  useEffect(() => {
    cargarReservas();
    cargarMesas();
  }, []);

  const cargarReservas = async () => {
    try {
      const res = await fetch(`${API_URL}/api/reservas/`);
      const data = await res.json();
      setReservas(data);
    } catch (error) {
      alert("Error al cargar reservas: " + error.message);
    }
  };

  const cargarMesas = async () => {
    try {
      const res = await fetch(`${API_URL}/api/mesas/`);
      const data = await res.json();
      setMesas(data);
    } catch (error) {
      console.error("Error al cargar mesas:", error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.numero_personas < 1 || formData.numero_personas > 15) {
      alert("El número de personas debe estar entre 1 y 15");
      return;
    }

    try {
      const url = editando 
        ? `${API_URL}/api/reservas/${editando}/`
        : `${API_URL}/api/reservas/`;
      
      const method = editando ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(JSON.stringify(error));
      }

      await cargarReservas();
      limpiarFormulario();
      alert(editando ? "Reserva actualizada exitosamente" : "Reserva creada exitosamente");
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  const handleEditar = (reserva) => {
    setEditando(reserva.id);
    setFormData({
      nombre: reserva.nombre,
      telefono: reserva.telefono,
      fecha: reserva.fecha,
      hora: reserva.hora,
      numero_personas: reserva.numero_personas,
      estado: reserva.estado,
      mesa_id: reserva.mesa.id,
      observacion: reserva.observacion || ""
    });
  };

  const handleEliminar = async (id) => {
    if (!window.confirm("¿Está seguro de eliminar esta reserva?")) return;

    try {
      const res = await fetch(`${API_URL}/api/reservas/${id}/`, {
        method: "DELETE",
      });

      if (res.ok) {
        await cargarReservas();
        alert("Reserva eliminada exitosamente");
      }
    } catch (error) {
      alert("Error al eliminar: " + error.message);
    }
  };

  const limpiarFormulario = () => {
    setEditando(null);
    setFormData({
      nombre: "",
      telefono: "",
      fecha: "",
      hora: "",
      numero_personas: 1,
      estado: "RESERVADO",
      mesa_id: "",
      observacion: ""
    });
  };

  const getEstadoBadgeClass = (estado) => {
    const clases = {
      "RESERVADO": "badge-reservado",
      "COMPLETADA": "badge-completada",
      "ANULADA": "badge-anulada",
      "NO_ASISTEN": "badge-no-asisten"
    };
    return `badge ${clases[estado] || ""}`;
  };

  return (
    <div className="container">
      <h1 className="titulo-principal">
        Sistema de Reservas de Restaurante
      </h1>

      <div className="grid-principal">
        <div className="formulario-container">
          <h2>{editando ? " Editar Reserva" : " Nueva Reserva"}</h2>
          <form onSubmit={handleSubmit} className="formulario">
            <div className="form-group">
              <label className="form-label">Nombre *</label>
              <input
                type="text"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
                className="form-input"
                placeholder="Nombre completo"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Teléfono *</label>
              <input
                type="tel"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
                required
                className="form-input"
                placeholder="+56 9 1234 5678"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Fecha *</label>
              <input
                type="date"
                name="fecha"
                value={formData.fecha}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Hora *</label>
              <input
                type="time"
                name="hora"
                value={formData.hora}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Número de Personas * (1-15)</label>
              <input
                type="number"
                name="numero_personas"
                value={formData.numero_personas}
                onChange={handleChange}
                min="1"
                max="15"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Mesa *</label>
              <select
                name="mesa_id"
                value={formData.mesa_id}
                onChange={handleChange}
                required
                className="form-input"
              >
                <option value="">Seleccione una mesa</option>
                {mesas.map(mesa => (
                  <option key={mesa.id} value={mesa.id}>
                    Mesa {mesa.numero} (Capacidad: {mesa.capacidad} personas)
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Estado *</label>
              <select
                name="estado"
                value={formData.estado}
                onChange={handleChange}
                required
                className="form-input"
              >
                <option value="RESERVADO">Reservado</option>
                <option value="COMPLETADA">Completada</option>
                <option value="ANULADA">Anulada</option>
                <option value="NO_ASISTEN">No Asisten</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Observación</label>
              <textarea
                name="observacion"
                value={formData.observacion}
                onChange={handleChange}
                rows="3"
                className="form-input form-textarea"
                placeholder="Comentarios adicionales (opcional)"
              />
            </div>

            <div className="botones-formulario">
              <button type="submit" className="btn btn-success">
                {editando ? " Actualizar" : " Crear"}
              </button>
              {editando && (
                <button 
                  type="button"
                  onClick={limpiarFormulario}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </div>

        {/* LISTA DE RESERVAS */}
        <div className="lista-container">
          <h2> Lista de Reservas ({reservas.length})</h2>
          
          {reservas.length === 0 ? (
            <div className="mensaje-vacio">
              No hay reservas registradas. ¡Crea la primera!
            </div>
          ) : (
            <div className="reservas-grid">
              {reservas.map((reserva) => (
                <div 
                  key={reserva.id}
                  className={`reserva-card ${editando === reserva.id ? 'editando' : ''}`}
                >
                  <div className="reserva-content">
                    <div className="reserva-info">
                      <h3 className="reserva-nombre">
                         {reserva.nombre}
                      </h3>
                      <p className="reserva-detalle">
                        <strong>Teléfono:</strong> {reserva.telefono}
                      </p>
                      <p className="reserva-detalle">
                        <strong>Fecha:</strong> {reserva.fecha} | 
                        <strong>Hora:</strong> {reserva.hora}
                      </p>
                      <p className="reserva-detalle">
                         <strong>Personas:</strong> {reserva.numero_personas} | 
                         <strong>Mesa:</strong> {reserva.mesa.numero} (Cap: {reserva.mesa.capacidad})
                      </p>
                      <p className="reserva-detalle">
                        <strong>Estado:</strong>{" "}
                        <span className={getEstadoBadgeClass(reserva.estado)}>
                          {reserva.estado.replace('_', ' ')}
                        </span>
                      </p>
                      {reserva.observacion && (
                        <p className="reserva-observacion">
                           {reserva.observacion}
                        </p>
                      )}
                    </div>
                    <div className="reserva-acciones">
                      <button
                        onClick={() => handleEditar(reserva)}
                        className="btn btn-primary"
                      >
                         Editar
                      </button>
                      <button
                        onClick={() => handleEliminar(reserva.id)}
                        className="btn btn-danger"
                      >
                         Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;