import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getHealthStatus } from "../api/health";
import MainLayout from "../components/layout/MainLayout";

const structures = [
  {
    name: "Árbol General",
    description:
      "Visualiza el pensum académico como una jerarquía de Facultad, Carrera, Ciclos y Cursos.",
    route: "/general-tree",
    action: "Abrir árbol general",
    accent: "from-cyan-500 to-sky-600",
    border: "border-cyan-500/30",
    badge: "Jerarquía",
  },
  {
    name: "Árbol Binario",
    description:
      "Inserta, busca, elimina y recorre un BST académico con React Flow y métricas estructurales.",
    route: "/binary-tree",
    action: "Abrir árbol binario",
    accent: "from-indigo-500 to-violet-600",
    border: "border-indigo-500/30",
    badge: "BST",
  },
  {
    name: "Árbol AVL",
    description:
      "Visualiza balanceo automático, alturas, factores de balance y rotaciones LL, RR, LR y RL.",
    route: "/avl",
    action: "Abrir árbol AVL",
    accent: "from-teal-500 to-emerald-600",
    border: "border-teal-500/30",
    badge: "Balanceado",
  },
  {
    name: "Árbol B",
    description:
      "Simula un índice académico multi-clave para expedientes, con splits, niveles y búsqueda eficiente.",
    route: "/btree",
    action: "Abrir árbol B",
    accent: "from-sky-500 to-blue-600",
    border: "border-sky-500/30",
    badge: "Índice",
  },
  {
    name: "Tabla Hash",
    description:
      "Busca estudiantes por carnet usando función hash propia, buckets, encadenamiento y colisiones visibles.",
    route: "/hash",
    action: "Abrir tabla hash",
    accent: "from-orange-500 to-amber-600",
    border: "border-orange-500/30",
    badge: "Colisiones",
  },
  {
    name: "Grafos DFS/BFS",
    description:
      "Visualiza el mapa de prerrequisitos como grafo dirigido, con recorridos DFS/BFS y orden de visita.",
    route: "/graph",
    action: "Abrir grafo",
    accent: "from-lime-500 to-green-600",
    border: "border-lime-500/30",
    badge: "Prerrequisitos",
  },
  {
    name: "Estructuras Lineales",
    description:
      "Integra lista de inscritos, cola de asesoría y pila de historial en una vista unificada con React Flow.",
    route: "/linear-structures",
    action: "Abrir estructuras lineales",
    accent: "from-cyan-500 to-teal-600",
    border: "border-cyan-500/30",
    badge: "Lista · Cola · Pila",
  },
];

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

  const isBackendOk = backendStatus === "ok";

  return (
    <MainLayout>
      <section className="overflow-hidden rounded-3xl border border-gray-700/80 bg-gray-900 shadow-2xl shadow-black/20">
        <div className="relative border-b border-gray-700/70 bg-gradient-to-br from-gray-800 via-gray-900 to-slate-950 p-8">
          <div className="absolute right-0 top-0 h-40 w-40 rounded-full bg-cyan-500/10 blur-3xl" />
          <div className="absolute bottom-0 left-10 h-32 w-32 rounded-full bg-indigo-500/10 blur-3xl" />

          <div className="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <span className="inline-flex rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-sm font-semibold text-cyan-300">
                Visualizador académico interactivo
              </span>

              <h2 className="mt-4 text-3xl font-bold tracking-tight text-white md:text-4xl">
                Bienvenido a EduStruct
              </h2>

              <p className="mt-3 max-w-2xl text-base leading-7 text-gray-300">
                Explora estructuras de datos clásicas aplicadas a un contexto
                universitario real: pensum, prerrequisitos, expedientes,
                estudiantes, asesorías e historial académico.
              </p>
            </div>

            <article className="rounded-2xl border border-gray-700 bg-gray-950/70 p-4 shadow-lg backdrop-blur">
              <div className="flex items-center gap-3">
                <span
                  className={`h-3 w-3 rounded-full ${isBackendOk ? "bg-green-400" : "bg-red-400"
                    }`}
                />
                <h3 className="text-sm font-semibold uppercase tracking-wide text-gray-300">
                  Backend
                </h3>
              </div>

              <p className="mt-3 text-sm text-gray-300">
                <span className="font-semibold text-white">Estado:</span>{" "}
                <span className={isBackendOk ? "text-green-400" : "text-red-400"}>
                  {backendStatus}
                </span>
              </p>

              <p className="mt-1 max-w-xs text-sm text-gray-400">
                {backendMessage}
              </p>

              {error && <p className="mt-2 text-sm font-medium text-red-400">{error}</p>}
            </article>
          </div>
        </div>

        <div className="bg-gray-800/80 p-6 md:p-8">
          <div className="mb-6 flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h3 className="text-2xl font-bold text-white">
                Módulos disponibles
              </h3>
              <p className="mt-1 text-sm text-gray-400">
                Selecciona una estructura para abrir su simulador visual.
              </p>
            </div>

            <span className="text-sm font-medium text-cyan-300">
              {structures.length} módulos activos
            </span>
          </div>

          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
            {structures.map((structure) => (
              <article
                key={structure.route}
                className={`group flex min-h-[230px] flex-col justify-between rounded-2xl border ${structure.border} bg-gray-950/80 p-5 shadow-lg shadow-black/10 transition duration-300 hover:-translate-y-1 hover:border-gray-500 hover:bg-gray-900`}
              >
                <div>
                  <div className="flex items-start justify-between gap-3">
                    <div
                      className={`rounded-2xl bg-gradient-to-br ${structure.accent} p-[1px]`}
                    >
                      <div className="rounded-2xl bg-gray-950 px-4 py-3">
                        <span className="text-lg font-bold text-white">
                          {structure.name}
                        </span>
                      </div>
                    </div>

                    <span className="rounded-full border border-gray-700 bg-gray-900 px-3 py-1 text-xs font-semibold text-gray-300">
                      {structure.badge}
                    </span>
                  </div>

                  <p className="mt-5 leading-7 text-gray-300">
                    {structure.description}
                  </p>
                </div>

                <Link
                  to={structure.route}
                  className={`mt-6 inline-flex w-full items-center justify-center rounded-xl bg-gradient-to-r ${structure.accent} px-4 py-3 text-sm font-bold text-white shadow-lg shadow-black/20 transition hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-2 focus:ring-offset-gray-900`}
                >
                  {structure.action}
                  <span className="ml-2 transition group-hover:translate-x-1">
                    →
                  </span>
                </Link>
              </article>
            ))}
          </div>
        </div>
      </section>
    </MainLayout>
  );
};

export default HomePage;
