import { useCallback, useEffect, useMemo, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useEdgesState,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";

import {
  configureHashTable,
  deleteHashKey,
  getHashTableState,
  insertHashEntry,
  loadHashDemo,
  resetHashTable,
  searchHashKey,
  traverseHashBuckets,
} from "../api/hashTable";
import MainLayout from "../components/layout/MainLayout";

const getPayload = (response) => response?.data || {};

const getApiErrorMessage = (error) => {
  const apiMessage = error?.response?.data?.message;
  const details = error?.response?.data?.error?.details || [];

  if (details.length > 0) {
    const detailText = details
      .map((detail) => detail.issue || detail.message || detail.field)
      .filter(Boolean)
      .join(", ");

    return detailText ? `${apiMessage || "Error de operación"}: ${detailText}` : apiMessage;
  }

  return apiMessage || error?.message || "No se pudo completar la operación.";
};

const normalizeCarnet = (value) => String(value ?? "").trim();

const buildStudentValue = ({ key, name, career, studentId }) => ({
  student_id: studentId || `STU-${key}`,
  carnet: key,
  full_name: name || `Estudiante ${key}`,
  career: career || "Ingeniería en Sistemas",
});

const getStudentSummary = (value) => {
  if (!value || typeof value !== "object") {
    return String(value || "Sin datos");
  }

  return value.full_name || value.name || value.student_id || "Sin nombre";
};

const createHashLabel = ({ label, metadata }) => {
  if (metadata?.role === "bucket") {
    return (
      <div className="min-w-[130px] text-center">
        <p className="font-mono text-sm font-bold text-white">{label}</p>
        <p className="mt-1 text-[11px] uppercase tracking-wide text-gray-300">
          {metadata.size} elemento{metadata.size === 1 ? "" : "s"}
        </p>
        {metadata.hasCollision && (
          <p className="mt-1 rounded-lg border border-orange-400 bg-orange-500/20 px-2 py-1 text-[10px] font-bold text-orange-100">
            Colisión visible
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="min-w-[170px] text-center">
      <p className="font-mono text-sm font-bold text-white">{metadata?.key}</p>
      <p className="mt-1 text-xs text-gray-200">{getStudentSummary(metadata?.value)}</p>
      <p className="mt-1 text-[10px] uppercase tracking-wide text-gray-400">
        Posición cadena: {metadata?.chainPosition ?? 0}
      </p>
      {metadata?.collision && (
        <p className="mt-1 text-[10px] font-semibold text-orange-200">Nodo en colisión</p>
      )}
    </div>
  );
};

const getNodeStyle = (node) => {
  const metadata = node?.data?.metadata || {};
  const isBucket = metadata.role === "bucket";
  const hasCollision = metadata.hasCollision || metadata.bucketHasCollision;
  const isHighlighted = metadata.isHighlighted;
  const isCollisionEntry = metadata.collision;

  if (isBucket) {
    return {
      minWidth: 150,
      border: `2px solid ${hasCollision ? "#fb923c" : isHighlighted ? "#facc15" : "#64748b"}`,
      borderRadius: 16,
      background: hasCollision ? "#431407" : isHighlighted ? "#713f12" : "#111827",
      color: "#f8fafc",
      padding: 10,
      boxShadow: hasCollision || isHighlighted ? "0 0 0 4px rgba(251, 146, 60, 0.18)" : "none",
    };
  }

  return {
    minWidth: 190,
    border: `2px solid ${isHighlighted ? "#facc15" : isCollisionEntry ? "#fb923c" : "#22c55e"}`,
    borderRadius: 16,
    background: isHighlighted ? "#713f12" : isCollisionEntry ? "#431407" : "#052e16",
    color: "#f8fafc",
    padding: 10,
    boxShadow: isHighlighted || isCollisionEntry ? "0 0 0 4px rgba(250, 204, 21, 0.18)" : "none",
  };
};

const normalizeHashNodes = (nodes = []) => nodes.map((node) => {
  const metadata = node?.data?.metadata || {};

  return {
    ...node,
    draggable: false,
    data: {
      ...node.data,
      label: createHashLabel({ label: node?.data?.label, metadata }),
    },
    style: getNodeStyle(node),
  };
});

const normalizeHashEdges = (edges = []) => edges.map((edge) => ({
  ...edge,
  style: {
    stroke: edge.animated ? "#fb923c" : "#64748b",
    strokeWidth: edge.animated ? 3 : 2,
  },
  labelStyle: {
    fill: "#e5e7eb",
    fontWeight: 700,
  },
}));

const MetricCard = ({ label, value, helper }) => (
  <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
    <p className="text-sm text-gray-400">{label}</p>
    <p className="mt-2 text-2xl font-bold text-white">{value}</p>
    {helper && <p className="mt-1 text-xs text-gray-500">{helper}</p>}
  </article>
);

const HashPage = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [table, setTable] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [capacityInput, setCapacityInput] = useState("7");
  const [keyInput, setKeyInput] = useState("2024001");
  const [nameInput, setNameInput] = useState("Ana López");
  const [careerInput, setCareerInput] = useState("Ingeniería en Sistemas");
  const [searchInput, setSearchInput] = useState("2024001");
  const [deleteInput, setDeleteInput] = useState("2024001");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [searchResult, setSearchResult] = useState(null);
  const [traversal, setTraversal] = useState(null);

  const applyPayload = useCallback((payload) => {
    setTable(payload.table || null);
    setMetrics(payload.metrics || null);
    setNodes(normalizeHashNodes(payload.nodes || []));
    setEdges(normalizeHashEdges(payload.edges || []));
  }, [setEdges, setNodes]);

  const runOperation = useCallback(async (operation, successMessage) => {
    setError("");
    setMessage("");

    try {
      const response = await operation();
      const payload = getPayload(response);
      applyPayload(payload);
      setMessage(successMessage || response?.message || "Operación completada correctamente.");
      return payload;
    } catch (err) {
      setError(getApiErrorMessage(err));
      return null;
    }
  }, [applyPayload]);

  const loadState = useCallback(async () => {
    await runOperation(getHashTableState, "Estado de la tabla hash cargado.");
  }, [runOperation]);

  useEffect(() => {
    loadState();
  }, [loadState]);

  const handleConfigure = async (event) => {
    event.preventDefault();
    const capacity = Number(capacityInput);
    const payload = await runOperation(
      () => configureHashTable(capacity),
      `Tabla hash configurada con ${capacity} buckets.`,
    );

    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleInsert = async (event) => {
    event.preventDefault();
    const key = normalizeCarnet(keyInput);
    const value = buildStudentValue({ key, name: nameInput.trim(), career: careerInput.trim() });
    const payload = await runOperation(
      () => insertHashEntry(key, value),
      `Carnet ${key} insertado en la tabla hash.`,
    );

    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    const key = normalizeCarnet(searchInput);

    setError("");
    setMessage("");

    try {
      const response = await searchHashKey(key);
      const payload = getPayload(response);
      applyPayload(payload);
      setSearchResult(payload.search || null);
      setTraversal(null);
      setMessage(payload.found ? `Carnet ${key} encontrado.` : `Carnet ${key} no encontrado.`);
    } catch (err) {
      setError(getApiErrorMessage(err));
    }
  };

  const handleDelete = async (event) => {
    event.preventDefault();
    const key = normalizeCarnet(deleteInput);
    const payload = await runOperation(
      () => deleteHashKey(key),
      `Carnet ${key} eliminado de la tabla hash.`,
    );

    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleLoadDemo = async () => {
    const payload = await runOperation(loadHashDemo, "Dataset demo con colisiones cargado.");
    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleTraverse = async () => {
    setError("");
    setMessage("");

    try {
      const response = await traverseHashBuckets();
      const payload = getPayload(response);
      applyPayload(payload);
      setTraversal(payload.traversal || null);
      setSearchResult(null);
      setMessage("Recorrido por buckets generado correctamente.");
    } catch (err) {
      setError(getApiErrorMessage(err));
    }
  };

  const handleReset = async () => {
    const payload = await runOperation(resetHashTable, "Tabla hash reiniciada.");
    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const hasNodes = nodes.length > 0;
  const buckets = table?.buckets || [];

  const traversalSummary = useMemo(() => {
    if (!traversal) {
      return "Sin recorrido ejecutado.";
    }

    return traversal.steps
      .map((step) => `B${step.bucketIndex}:${step.key}`)
      .join(" → ");
  }, [traversal]);

  return (
    <MainLayout>
      <section className="space-y-6">
        <header className="rounded-2xl border border-gray-700 bg-gray-800 p-6 shadow-lg">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-widest text-orange-400">
                Épica 9 · Tabla Hash
              </p>
              <h2 className="mt-2 text-2xl font-bold text-white">
                Búsqueda de estudiantes por carnet
              </h2>
              <p className="mt-3 max-w-3xl text-gray-300">
                Implementa una tabla hash manual con función hash propia, buckets, encadenamiento separado,
                eliminación, búsqueda y colisiones visibles. Nada de dict disfrazado: aquí cada choque deja huella.
              </p>
            </div>

            <div className="rounded-xl border border-orange-700 bg-orange-950/50 p-4 text-sm text-orange-100">
              <p className="font-semibold">Estrategia de colisión</p>
              <p className="mt-1">Encadenamiento separado para explicar buckets y cadenas sin magia negra.</p>
            </div>
          </div>
        </header>

        <div className="grid gap-4 lg:grid-cols-5">
          <MetricCard label="Elementos" value={metrics?.count ?? 0} helper="Carnets almacenados" />
          <MetricCard label="Buckets" value={metrics?.capacity ?? 0} helper="Tamaño de tabla" />
          <MetricCard label="Colisiones" value={metrics?.collisions ?? 0} helper="Inserciones con bucket ocupado" />
          <MetricCard label="Factor de carga" value={metrics?.loadFactor ?? 0} helper="elementos / buckets" />
          <MetricCard label="Cadena máxima" value={metrics?.maxChainLength ?? 0} helper="Mayor bucket encadenado" />
        </div>

        {(message || error) && (
          <div className={`rounded-xl border p-4 ${error ? "border-red-700 bg-red-950 text-red-100" : "border-green-700 bg-green-950 text-green-100"}`}>
            {error || message}
          </div>
        )}

        <div className="grid gap-6 xl:grid-cols-[380px_1fr]">
          <aside className="space-y-5">
            <form onSubmit={handleConfigure} className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Configuración</h3>
              <label className="mt-4 block text-sm font-medium text-gray-300" htmlFor="hash-capacity">
                Tamaño inicial de tabla
              </label>
              <div className="mt-2 flex gap-2">
                <input
                  id="hash-capacity"
                  min="3"
                  type="number"
                  value={capacityInput}
                  onChange={(event) => setCapacityInput(event.target.value)}
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-orange-400"
                />
                <button className="rounded-xl bg-orange-600 px-4 py-2 font-semibold text-white transition hover:bg-orange-500" type="submit">
                  Aplicar
                </button>
              </div>
              <p className="mt-2 text-xs text-gray-400">Reconfigurar reinicia la tabla para recalcular buckets.</p>
            </form>

            <form onSubmit={handleInsert} className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Insertar estudiante</h3>
              <input
                value={keyInput}
                onChange={(event) => setKeyInput(event.target.value)}
                placeholder="Carnet. Ej. 2024001"
                className="mt-4 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-orange-400"
              />
              <input
                value={nameInput}
                onChange={(event) => setNameInput(event.target.value)}
                placeholder="Nombre completo"
                className="mt-3 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-orange-400"
              />
              <input
                value={careerInput}
                onChange={(event) => setCareerInput(event.target.value)}
                placeholder="Carrera"
                className="mt-3 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-orange-400"
              />
              <button className="mt-3 w-full rounded-xl bg-indigo-600 px-4 py-2 font-semibold text-white transition hover:bg-indigo-500" type="submit">
                Insertar carnet
              </button>
            </form>

            <form onSubmit={handleSearch} className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Buscar por carnet</h3>
              <input
                value={searchInput}
                onChange={(event) => setSearchInput(event.target.value)}
                placeholder="Carnet a buscar"
                className="mt-4 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-lime-400"
              />
              <button className="mt-3 w-full rounded-xl bg-lime-700 px-4 py-2 font-semibold text-white transition hover:bg-lime-600" type="submit">
                Buscar carnet
              </button>
              {searchResult && (
                <div className="mt-4 rounded-xl border border-gray-700 bg-gray-950 p-3 text-sm text-gray-300">
                  <p><span className="font-semibold text-white">Resultado:</span> {searchResult.found ? "Encontrado" : "No encontrado"}</p>
                  <p><span className="font-semibold text-white">Bucket:</span> {searchResult.bucketIndex}</p>
                  <p><span className="font-semibold text-white">Comparaciones:</span> {searchResult.comparisons}</p>
                  <p><span className="font-semibold text-white">Posición cadena:</span> {searchResult.chainPosition ?? "N/A"}</p>
                </div>
              )}
            </form>

            <form onSubmit={handleDelete} className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Eliminar carnet</h3>
              <input
                value={deleteInput}
                onChange={(event) => setDeleteInput(event.target.value)}
                placeholder="Carnet a eliminar"
                className="mt-4 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-red-400"
              />
              <button className="mt-3 w-full rounded-xl bg-red-700 px-4 py-2 font-semibold text-white transition hover:bg-red-600" type="submit">
                Eliminar carnet
              </button>
            </form>

            <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Demo y estado</h3>
              <div className="mt-4 grid grid-cols-2 gap-2">
                <button onClick={handleLoadDemo} className="rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white transition hover:bg-teal-500" type="button">
                  Cargar demo
                </button>
                <button onClick={handleTraverse} className="rounded-xl bg-gray-700 px-4 py-2 font-semibold text-white transition hover:bg-gray-600" type="button">
                  Recorrer buckets
                </button>
                <button onClick={loadState} className="rounded-xl bg-gray-700 px-4 py-2 font-semibold text-white transition hover:bg-gray-600" type="button">
                  Refrescar
                </button>
                <button onClick={handleReset} className="rounded-xl bg-red-700 px-4 py-2 font-semibold text-white transition hover:bg-red-600" type="button">
                  Reset
                </button>
              </div>
            </section>
          </aside>

          <main className="space-y-6">
            <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-white">Visualización React Flow</h3>
                  <p className="mt-1 text-sm text-gray-400">Cada fila inicia con un bucket; los nodos hacia la derecha son la cadena de colisión.</p>
                </div>
                <div className="text-sm text-gray-300">
                  Buckets con colisión: <span className="text-orange-300">{metrics?.collisionBucketCount ?? 0}</span>
                </div>
              </div>

              <div className="mt-4 h-[620px] overflow-hidden rounded-2xl border border-gray-700 bg-gray-950">
                {hasNodes ? (
                  <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    fitView
                    fitViewOptions={{ padding: 0.25 }}
                    nodesDraggable={false}
                    nodesConnectable={false}
                    elementsSelectable
                  >
                    <MiniMap pannable zoomable />
                    <Controls />
                    <Background gap={18} size={1} />
                  </ReactFlow>
                ) : (
                  <div className="flex h-full items-center justify-center text-gray-400">
                    No hay datos para visualizar.
                  </div>
                )}
              </div>
            </section>

            <section className="grid gap-6 lg:grid-cols-2">
              <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
                <h3 className="text-lg font-semibold text-white">Buckets</h3>
                <div className="mt-4 max-h-80 space-y-2 overflow-auto pr-2">
                  {buckets.map((bucket) => (
                    <div key={bucket.bucketIndex} className="rounded-xl border border-gray-700 bg-gray-950 p-3 text-sm text-gray-300">
                      <div className="flex items-center justify-between">
                        <span className="font-mono font-semibold text-white">Bucket {bucket.bucketIndex}</span>
                        <span className={bucket.hasCollision ? "text-orange-300" : "text-gray-400"}>
                          {bucket.size} item{bucket.size === 1 ? "" : "s"}
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-gray-500">
                        {bucket.items.length > 0 ? bucket.items.map((item) => item.key).join(" → ") : "Vacío"}
                      </p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
                <h3 className="text-lg font-semibold text-white">Recorrido por buckets</h3>
                <p className="mt-3 rounded-xl border border-gray-700 bg-gray-950 p-3 text-sm text-gray-300">
                  {traversalSummary}
                </p>
                {traversal && (
                  <div className="mt-4 max-h-64 overflow-auto rounded-xl border border-gray-700 bg-gray-950 p-3">
                    {traversal.steps.map((step) => (
                      <p key={`${step.step}-${step.key}`} className="text-sm text-gray-300">
                        <span className="font-mono text-white">#{step.step}</span> · Bucket {step.bucketIndex} · {step.key} · Comparación visual
                      </p>
                    ))}
                  </div>
                )}
              </article>
            </section>
          </main>
        </div>
      </section>
    </MainLayout>
  );
};

export default HashPage;
