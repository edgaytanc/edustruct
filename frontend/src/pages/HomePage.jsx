import { useEffect, useState } from "react";
import { getHealthStatus } from "../api/health";
import MainLayout from "../components/layout/MainLayout";

const HomePage = () => {
  const [backendStatus, setBackendStatus] = useState("Cargando...");
  const [backendMessage, setBackendMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await getHealthStatus();
        setBackendStatus(data?.data?.status || "ok");
        setBackendMessage(data?.message || "Conexión exitosa");
      } catch (err) {
        setError("No se pudo conectar con el backend");
        setBackendStatus("error");
        setBackendMessage(err?.message || "Error desconocido");
      }
    };

    fetchHealth();
  }, []);

  return (
    <MainLayout>
      <section className="rounded-2xl border border-gray-700 bg-gray-800 p-6 shadow-lg">
        <h2 className="text-xl font-semibold text-white">
          Bienvenido a EduStruct
        </h2>

        <p className="mt-3 text-gray-300">
          Proyecto orientado a la visualización interactiva de estructuras de
          datos aplicadas al contexto educativo.
        </p>

        <div className="mt-6 rounded-xl border border-cyan-700 bg-gray-900 p-4">
          <h3 className="text-lg font-medium text-cyan-400">
            Estado de conexión con el backend
          </h3>

          <p className="mt-3">
            <span className="font-semibold text-white">Estado:</span>{" "}
            <span
              className={
                backendStatus === "ok" ? "text-green-400" : "text-red-400"
              }
            >
              {backendStatus}
            </span>
          </p>

          <p className="mt-2 text-gray-300">
            <span className="font-semibold text-white">Mensaje:</span>{" "}
            {backendMessage}
          </p>

          {error && (
            <p className="mt-3 font-medium text-red-400">
              {error}
            </p>
          )}
        </div>
      </section>
    </MainLayout>
  );
};

export default HomePage;