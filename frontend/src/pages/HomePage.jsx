import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
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

        <div className="mt-6 grid gap-4 lg:grid-cols-6">
          <article className="rounded-xl border border-cyan-700 bg-gray-900 p-4">
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
          </article>

          <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
            <h3 className="text-lg font-medium text-white">
              Épica 5 — Árbol General
            </h3>

            <p className="mt-3 text-gray-300">
              Visualiza el pensum académico como una jerarquía de Facultad,
              Carrera, Ciclos y Cursos.
            </p>

            <Link
              to="/general-tree"
              className="mt-5 inline-flex rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500"
            >
              Abrir árbol general
            </Link>
          </article>

          <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
            <h3 className="text-lg font-medium text-white">
              Épica 6 — Árbol Binario
            </h3>

            <p className="mt-3 text-gray-300">
              Inserta, busca, elimina y recorre un BST académico con visualización
              React Flow y métricas estructurales.
            </p>

            <Link
              to="/binary-tree"
              className="mt-5 inline-flex rounded-xl bg-indigo-600 px-4 py-2 font-semibold text-white transition hover:bg-indigo-500"
            >
              Abrir árbol binario
            </Link>
          </article>



          <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
            <h3 className="text-lg font-medium text-white">
              Épica 8 — Árbol B
            </h3>

            <p className="mt-3 text-gray-300">
              Simula un índice académico multi-clave para expedientes, con splits, niveles y búsqueda eficiente.
            </p>

            <Link
              to="/btree"
              className="mt-5 inline-flex rounded-xl bg-sky-600 px-4 py-2 font-semibold text-white transition hover:bg-sky-500"
            >
              Abrir árbol B
            </Link>
          </article>



          <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
            <h3 className="text-lg font-medium text-white">
              Épica 9 — Tabla Hash
            </h3>

            <p className="mt-3 text-gray-300">
              Busca estudiantes por carnet usando función hash propia, buckets,
              encadenamiento y colisiones visibles.
            </p>

            <Link
              to="/hash"
              className="mt-5 inline-flex rounded-xl bg-orange-600 px-4 py-2 font-semibold text-white transition hover:bg-orange-500"
            >
              Abrir tabla hash
            </Link>
          </article>

          <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
            <h3 className="text-lg font-medium text-white">
              Épica 7 — Árbol AVL
            </h3>

            <p className="mt-3 text-gray-300">
              Visualiza inserciones y eliminaciones balanceadas con alturas,
              factores de balance y rotaciones LL, RR, LR y RL.
            </p>

            <Link
              to="/avl"
              className="mt-5 inline-flex rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white transition hover:bg-teal-500"
            >
              Abrir árbol AVL
            </Link>
          </article>
        </div>
      </section>
    </MainLayout>
  );
};

export default HomePage;
