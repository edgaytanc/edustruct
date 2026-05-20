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
  bulkInsertBTreeKeys,
  configureBTree,
  getBTreeState,
  insertBTreeKey,
  loadBTreeDemo,
  resetBTree,
  searchBTreeKey,
  traverseBTree,
} from "../api/btree";
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

const coerceInputValue = (rawValue) => {
  const normalized = String(rawValue ?? "").trim();

  if (!normalized) {
    return "";
  }

  const numericValue = Number(normalized);
  return Number.isNaN(numericValue) ? normalized : numericValue;
};

const coerceKeysList = (rawValue) => String(rawValue ?? "")
  .split(/[\n,;\s]+/)
  .map((value) => value.trim())
  .filter(Boolean)
  .map(coerceInputValue);

const createBTreeLabel = ({ keys, metadata, visualState }) => {
  const nodeId = String(metadata?.id || "");
  const isHighlighted = visualState.highlightedId && nodeId === String(visualState.highlightedId);
  const isSearchPath = visualState.searchPath.includes(nodeId);
  const splitNodes = visualState.splitNodeIds;
  const isSplitNode = splitNodes.has(nodeId);

  return (
    <div className="min-w-[150px] rounded-xl text-center">
      <div className="mb-2 flex items-center justify-center gap-1">
        {keys.map((key) => (
          <span
            key={`${nodeId}-${key}`}
            className={`rounded-lg border px-2 py-1 font-mono text-sm font-bold ${
              isHighlighted
                ? "border-yellow-300 bg-yellow-500/20 text-yellow-100"
                : isSplitNode
                  ? "border-orange-300 bg-orange-500/20 text-orange-100"
                  : "border-sky-400 bg-sky-500/10 text-sky-100"
            }`}
          >
            {key}
          </span>
        ))}
      </div>
      <div className="text-[10px] uppercase tracking-wide text-gray-300">
        Nivel {metadata?.level ?? 0} · {metadata?.leaf ? "Hoja" : "Interno"}
      </div>
      {isSearchPath && (
        <div className="mt-1 text-[10px] font-semibold text-lime-300">Ruta de búsqueda</div>
      )}
    </div>
  );
};

const normalizeBTreeNodes = (nodes = [], visualState = {}) => {
  const highlightedId = visualState.highlightedId || "";
  const searchPath = visualState.searchPath || [];
  const splitNodeIds = visualState.splitNodeIds || new Set();
  const normalizedVisualState = { highlightedId, searchPath, splitNodeIds };

  return nodes.map((node) => {
    const metadata = node?.data?.metadata || {};
    const keys = metadata.keys || [];
    const nodeId = String(node.id);
    const isHighlighted = highlightedId && nodeId === String(highlightedId);
    const isSearchPath = searchPath.includes(nodeId);
    const isSplitNode = splitNodeIds.has(nodeId);
    const isRoot = node?.data?.category === "root";

    const borderColor = isHighlighted
      ? "#facc15"
      : isSplitNode
        ? "#fb923c"
        : isSearchPath
          ? "#84cc16"
          : isRoot
            ? "#38bdf8"
            : "#64748b";

    const backgroundColor = isHighlighted
      ? "#713f12"
      : isSplitNode
        ? "#431407"
        : isSearchPath
          ? "#1a2e05"
          : "#111827";

    return {
      ...node,
      draggable: false,
      data: {
        ...node.data,
        label: createBTreeLabel({
          keys,
          metadata: { ...metadata, id: nodeId },
          visualState: normalizedVisualState,
        }),
      },
      style: {
        minWidth: Math.max(150, keys.length * 58),
        border: `2px solid ${borderColor}`,
        borderRadius: 16,
        background: backgroundColor,
        color: "#f8fafc",
        padding: 10,
        boxShadow: isHighlighted || isSplitNode ? `0 0 0 4px ${borderColor}33` : "none",
      },
    };
  });
};

const normalizeBTreeEdges = (edges = [], visualState = {}) => {
  const searchPath = visualState.searchPath || [];

  return edges.map((edge) => {
    const isSearchEdge = searchPath.includes(String(edge.source)) && searchPath.includes(String(edge.target));

    return {
      ...edge,
      animated: isSearchEdge,
      style: {
        stroke: isSearchEdge ? "#84cc16" : "#64748b",
        strokeWidth: isSearchEdge ? 3 : 2,
      },
      labelStyle: {
        fill: "#e5e7eb",
        fontWeight: 700,
      },
    };
  });
};

const MetricCard = ({ label, value, helper }) => (
  <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
    <p className="text-sm text-gray-400">{label}</p>
    <p className="mt-2 text-2xl font-bold text-white">{value}</p>
    {helper && <p className="mt-1 text-xs text-gray-500">{helper}</p>}
  </article>
);

const BTreePage = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [tree, setTree] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [keyInput, setKeyInput] = useState("");
  const [bulkInput, setBulkInput] = useState("2024008, 2024016, 2024024, 2024032, 2024040");
  const [searchInput, setSearchInput] = useState("");
  const [orderInput, setOrderInput] = useState("4");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [searchResult, setSearchResult] = useState(null);
  const [traversal, setTraversal] = useState(null);
  const [splitEvents, setSplitEvents] = useState([]);
  const [visualState, setVisualState] = useState({
    highlightedId: "",
    searchPath: [],
    splitNodeIds: new Set(),
  });

  const applyPayload = useCallback((payload, nextVisualState = {}) => {
    const splitNodeIds = new Set(
      (payload.splitEvents || [])
        .flatMap((event) => [event.parentId, event.leftId, event.rightId])
        .filter(Boolean)
        .map(String),
    );
    const mergedVisualState = {
      highlightedId: nextVisualState.highlightedId || "",
      searchPath: nextVisualState.searchPath || [],
      splitNodeIds: nextVisualState.splitNodeIds || splitNodeIds,
    };

    setTree(payload.tree || null);
    setMetrics(payload.metrics || null);
    setSplitEvents(payload.splitEvents || []);
    setVisualState(mergedVisualState);
    setNodes(normalizeBTreeNodes(payload.nodes || [], mergedVisualState));
    setEdges(normalizeBTreeEdges(payload.edges || [], mergedVisualState));
  }, [setEdges, setNodes]);

  const runOperation = useCallback(async (operation, successMessage, options = {}) => {
    setError("");
    setMessage("");

    try {
      const response = await operation();
      const payload = getPayload(response);
      applyPayload(payload, options.visualState || {});
      setMessage(successMessage || response?.message || "Operación completada correctamente.");
      return payload;
    } catch (err) {
      setError(getApiErrorMessage(err));
      return null;
    }
  }, [applyPayload]);

  const loadState = useCallback(async () => {
    await runOperation(getBTreeState, "Estado del Árbol B cargado.");
  }, [runOperation]);

  useEffect(() => {
    loadState();
  }, [loadState]);

  const handleConfigure = async (event) => {
    event.preventDefault();
    const order = Number(orderInput);
    await runOperation(
      () => configureBTree(order),
      `Árbol B configurado con orden ${order}.`,
    );
    setSearchResult(null);
    setTraversal(null);
  };

  const handleInsert = async (event) => {
    event.preventDefault();
    const key = coerceInputValue(keyInput);
    const payload = await runOperation(
      () => insertBTreeKey(key),
      `Clave ${key} insertada en el índice académico.`,
    );

    if (payload) {
      setKeyInput("");
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleBulkInsert = async () => {
    const keys = coerceKeysList(bulkInput);
    const payload = await runOperation(
      () => bulkInsertBTreeKeys(keys),
      `${keys.length} claves insertadas en lote.`,
    );

    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    const key = coerceInputValue(searchInput);

    setError("");
    setMessage("");

    try {
      const response = await searchBTreeKey(key);
      const payload = getPayload(response);
      const path = payload?.search?.pathNodeIds || [];
      const foundNodeId = payload?.search?.nodeId || "";
      const nextVisualState = {
        highlightedId: foundNodeId,
        searchPath: path.map(String),
        splitNodeIds: new Set(),
      };

      applyPayload(payload, nextVisualState);
      setSearchResult(payload.search || null);
      setTraversal(null);
      setMessage(payload.found ? `Clave ${key} encontrada.` : `Clave ${key} no encontrada.`);
    } catch (err) {
      setError(getApiErrorMessage(err));
    }
  };

  const handleLoadDemo = async () => {
    const payload = await runOperation(loadBTreeDemo, "Dataset demo de expedientes cargado.");
    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const handleTraverse = async (type = "levelorder") => {
    setError("");
    setMessage("");

    try {
      const response = await traverseBTree(type);
      const payload = getPayload(response);
      applyPayload(payload);
      setTraversal(payload.traversal || null);
      setSearchResult(null);
      setMessage(`Recorrido ${type} generado correctamente.`);
    } catch (err) {
      setError(getApiErrorMessage(err));
    }
  };

  const handleReset = async () => {
    const payload = await runOperation(resetBTree, "Árbol B reiniciado.");
    if (payload) {
      setSearchResult(null);
      setTraversal(null);
    }
  };

  const hasNodes = nodes.length > 0;
  const lastSplit = splitEvents.length > 0 ? splitEvents[splitEvents.length - 1] : null;

  const traversalSummary = useMemo(() => {
    if (!traversal) {
      return "Sin recorrido ejecutado.";
    }

    if (traversal.type === "inorder") {
      return traversal.order.join(" → ");
    }

    return traversal.steps
      .map((step) => `[${(step.keys || []).join(" | ")}]`)
      .join(" → ");
  }, [traversal]);

  return (
    <MainLayout>
      <section className="space-y-6">
        <header className="rounded-2xl border border-gray-700 bg-gray-800 p-6 shadow-lg">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-widest text-sky-400">
                Épica 8 · Árbol B
              </p>
              <h2 className="mt-2 text-2xl font-bold text-white">
                Índice académico de expedientes universitarios
              </h2>
              <p className="mt-3 max-w-3xl text-gray-300">
                Simula un índice balanceado con múltiples claves por nodo, splits visibles,
                búsqueda eficiente y recorrido por niveles. En otras palabras: menos drama que buscar
                expedientes en una pila de papeles.
              </p>
            </div>

            <div className="rounded-xl border border-sky-700 bg-sky-950/50 p-4 text-sm text-sky-100">
              <p className="font-semibold">Decisión técnica</p>
              <p className="mt-1">Se implementa Árbol B por claridad visual, menor complejidad y mejor defensa pedagógica.</p>
            </div>
          </div>
        </header>

        <div className="grid gap-4 lg:grid-cols-5">
          <MetricCard label="Claves" value={metrics?.count ?? 0} helper="Expedientes indexados" />
          <MetricCard label="Altura" value={metrics?.height ?? 0} helper="Niveles desde raíz" />
          <MetricCard label="Orden" value={metrics?.order ?? 4} helper="Máximo de hijos por nodo" />
          <MetricCard label="Nodos" value={metrics?.nodeCount ?? 0} helper="Bloques del índice" />
          <MetricCard label="Splits" value={metrics?.splitCount ?? 0} helper="Divisiones acumuladas" />
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
              <label className="mt-4 block text-sm font-medium text-gray-300" htmlFor="btree-order">
                Orden del Árbol B
              </label>
              <div className="mt-2 flex gap-2">
                <input
                  id="btree-order"
                  min="3"
                  type="number"
                  value={orderInput}
                  onChange={(event) => setOrderInput(event.target.value)}
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-sky-400"
                />
                <button className="rounded-xl bg-sky-600 px-4 py-2 font-semibold text-white transition hover:bg-sky-500" type="submit">
                  Aplicar
                </button>
              </div>
              <p className="mt-2 text-xs text-gray-400">Reconfigurar reinicia el árbol para conservar invariantes.</p>
            </form>

            <form onSubmit={handleInsert} className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Insertar expediente</h3>
              <input
                value={keyInput}
                onChange={(event) => setKeyInput(event.target.value)}
                placeholder="Ej. 2024096"
                className="mt-4 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-sky-400"
              />
              <button className="mt-3 w-full rounded-xl bg-indigo-600 px-4 py-2 font-semibold text-white transition hover:bg-indigo-500" type="submit">
                Insertar clave
              </button>
            </form>

            <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Carga rápida</h3>
              <textarea
                value={bulkInput}
                onChange={(event) => setBulkInput(event.target.value)}
                rows="4"
                className="mt-4 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-sm text-white outline-none focus:border-sky-400"
              />
              <div className="mt-3 grid grid-cols-2 gap-2">
                <button onClick={handleBulkInsert} className="rounded-xl bg-violet-600 px-4 py-2 font-semibold text-white transition hover:bg-violet-500" type="button">
                  Insertar lote
                </button>
                <button onClick={handleLoadDemo} className="rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white transition hover:bg-teal-500" type="button">
                  Cargar demo
                </button>
              </div>
            </section>

            <form onSubmit={handleSearch} className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Buscar expediente</h3>
              <input
                value={searchInput}
                onChange={(event) => setSearchInput(event.target.value)}
                placeholder="Clave a buscar"
                className="mt-4 w-full rounded-xl border border-gray-600 bg-gray-950 px-4 py-2 text-white outline-none focus:border-lime-400"
              />
              <button className="mt-3 w-full rounded-xl bg-lime-700 px-4 py-2 font-semibold text-white transition hover:bg-lime-600" type="submit">
                Buscar clave
              </button>
              {searchResult && (
                <div className="mt-4 rounded-xl border border-gray-700 bg-gray-950 p-3 text-sm text-gray-300">
                  <p><span className="font-semibold text-white">Resultado:</span> {searchResult.found ? "Encontrado" : "No encontrado"}</p>
                  <p><span className="font-semibold text-white">Nivel:</span> {searchResult.level ?? "N/A"}</p>
                  <p><span className="font-semibold text-white">Pasos:</span> {searchResult.steps?.length ?? 0}</p>
                </div>
              )}
            </form>

            <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Recorridos y estado</h3>
              <div className="mt-4 grid grid-cols-2 gap-2">
                <button onClick={() => handleTraverse("levelorder")} className="rounded-xl bg-gray-700 px-4 py-2 font-semibold text-white transition hover:bg-gray-600" type="button">
                  Level-order
                </button>
                <button onClick={() => handleTraverse("inorder")} className="rounded-xl bg-gray-700 px-4 py-2 font-semibold text-white transition hover:bg-gray-600" type="button">
                  Inorder
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
                  <p className="mt-1 text-sm text-gray-400">Cada nodo representa un bloque multi-clave del índice.</p>
                </div>
                <div className="text-sm text-gray-300">
                  Válido: <span className={metrics?.isValid ? "text-green-400" : "text-red-400"}>{String(metrics?.isValid ?? true)}</span>
                </div>
              </div>

              <div className="mt-4 h-[560px] overflow-hidden rounded-2xl border border-gray-700 bg-gray-950">
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
                  <div className="flex h-full items-center justify-center p-8 text-center">
                    <div>
                      <p className="text-lg font-semibold text-white">El Árbol B está vacío.</p>
                      <p className="mt-2 max-w-md text-gray-400">Inserta claves o carga el dataset demo para visualizar splits y niveles.</p>
                    </div>
                  </div>
                )}
              </div>
            </section>

            <div className="grid gap-6 lg:grid-cols-2">
              <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
                <h3 className="text-lg font-semibold text-white">Splits visibles</h3>
                {lastSplit ? (
                  <div className="mt-4 rounded-xl border border-orange-700 bg-orange-950/40 p-4 text-sm text-orange-100">
                    <p><span className="font-semibold">Mediana promovida:</span> {String(lastSplit.promotedKey)}</p>
                    <p><span className="font-semibold">Nodo izquierdo:</span> {(lastSplit.leftKeys || []).join(" | ")}</p>
                    <p><span className="font-semibold">Nodo derecho:</span> {(lastSplit.rightKeys || []).join(" | ")}</p>
                    <p><span className="font-semibold">Total splits:</span> {splitEvents.length}</p>
                  </div>
                ) : (
                  <p className="mt-4 text-sm text-gray-400">Aún no hay splits registrados.</p>
                )}
              </section>

              <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
                <h3 className="text-lg font-semibold text-white">Recorrido</h3>
                <p className="mt-4 rounded-xl border border-gray-700 bg-gray-950 p-4 text-sm text-gray-200">
                  {traversalSummary}
                </p>
              </section>
            </div>

            <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Estado estructural</h3>
              <p className="mt-2 text-sm text-gray-400">JSON del Árbol B para validar claves, hijos e invariantes.</p>
              <pre className="mt-4 max-h-96 overflow-auto rounded-xl border border-gray-700 bg-gray-950 p-4 text-xs text-gray-200">
                {JSON.stringify(tree || { root: null, size: 0 }, null, 2)}
              </pre>
            </section>
          </main>
        </div>
      </section>
    </MainLayout>
  );
};

export default BTreePage;
