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
  deleteGeneralTreeNode,
  getGeneralTreeState,
  insertGeneralTreeNode,
  loadGeneralTreeDemo,
  resetGeneralTree,
  searchGeneralTreeNode,
  traverseGeneralTree,
} from "../api/tree";
import MainLayout from "../components/layout/MainLayout";

const initialForm = {
  id: "",
  label: "",
  parentId: "",
  category: "course",
  metadataCode: "",
};

const categoryOptions = [
  { value: "faculty", label: "Facultad" },
  { value: "career", label: "Carrera" },
  { value: "cycle", label: "Ciclo" },
  { value: "course", label: "Curso" },
  { value: "academic", label: "Académico" },
];

const traversalOptions = [
  { value: "levelorder", label: "Levelorder" },
  { value: "preorder", label: "Preorder" },
  { value: "postorder", label: "Postorder" },
];

const categoryBadgeClasses = {
  faculty: "border-purple-500 bg-purple-950 text-purple-100",
  career: "border-cyan-500 bg-cyan-950 text-cyan-100",
  cycle: "border-emerald-500 bg-emerald-950 text-emerald-100",
  course: "border-amber-500 bg-amber-950 text-amber-100",
  academic: "border-gray-500 bg-gray-950 text-gray-100",
};

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

const getRawNodeLabel = (node) => {
  if (typeof node?.data?.rawLabel === "string") {
    return node.data.rawLabel;
  }

  if (typeof node?.data?.label === "string") {
    return node.data.label;
  }

  return String(node?.id || "Nodo");
};

const normalizeNodes = (nodes = [], visualState = {}) => {
  const highlightedId = visualState.highlightedId || "";
  const traversalOrder = visualState.traversalOrder || [];
  const traversalIndexById = new Map(
    traversalOrder.map((nodeId, index) => [String(nodeId), index + 1]),
  );

  return nodes.map((node) => {
    const nodeId = String(node.id);
    const category = node?.data?.category || "academic";
    const rawLabel = getRawNodeLabel(node);
    const isHighlighted = highlightedId && nodeId === String(highlightedId);
    const traversalStep = traversalIndexById.get(nodeId);
    const isTraversalNode = Boolean(traversalStep);
    const badgeClass = categoryBadgeClasses[category] || categoryBadgeClasses.academic;

    return {
      ...node,
      draggable: false,
      data: {
        ...node.data,
        rawLabel,
        label: (
          <div className="min-w-40">
            <div className="flex items-start justify-between gap-2">
              <p className="text-sm font-semibold leading-snug text-white">
                {rawLabel}
              </p>
              {traversalStep && (
                <span className="rounded-full bg-indigo-500 px-2 py-0.5 text-[10px] font-bold text-white">
                  {traversalStep}
                </span>
              )}
            </div>
            <p className={`mt-2 inline-flex rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${badgeClass}`}>
              {category}
            </p>
            {node?.data?.metadata?.level !== undefined && (
              <p className="mt-2 text-xs text-gray-300">
                Nivel {node.data.metadata.level} · Hijos {node.data.metadata.childrenCount ?? 0}
              </p>
            )}
          </div>
        ),
      },
      style: {
        border: isHighlighted
          ? "2px solid #facc15"
          : isTraversalNode
            ? "2px solid #818cf8"
            : "1px solid #0891b2",
        borderRadius: "16px",
        background: isHighlighted ? "#713f12" : isTraversalNode ? "#312e81" : "#111827",
        color: "#e5e7eb",
        padding: "10px",
        minWidth: "170px",
        boxShadow: isHighlighted
          ? "0 14px 34px rgba(250, 204, 21, 0.24)"
          : isTraversalNode
            ? "0 14px 34px rgba(129, 140, 248, 0.22)"
            : "0 10px 25px rgba(8, 145, 178, 0.16)",
      },
    };
  });
};

const normalizeEdges = (edges = [], traversalOrder = []) => {
  const traversalPairs = new Set();

  for (let index = 0; index < traversalOrder.length - 1; index += 1) {
    traversalPairs.add(`${traversalOrder[index]}-${traversalOrder[index + 1]}`);
  }

  return edges.map((edge) => {
    const isTraversalEdge = traversalPairs.has(`${edge.source}-${edge.target}`);

    return {
      ...edge,
      animated: isTraversalEdge,
      style: {
        strokeWidth: isTraversalEdge ? 3 : 2,
        stroke: isTraversalEdge ? "#818cf8" : "#0891b2",
      },
    };
  });
};

const buildMetadata = (form) => {
  const metadata = {};

  if (form.metadataCode.trim()) {
    metadata.code = form.metadataCode.trim();
  }

  return metadata;
};

const GeneralTreePage = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [metrics, setMetrics] = useState(null);
  const [tree, setTree] = useState(null);
  const [form, setForm] = useState(initialForm);
  const [deleteId, setDeleteId] = useState("");
  const [searchId, setSearchId] = useState("");
  const [highlightedId, setHighlightedId] = useState("");
  const [traversalType, setTraversalType] = useState("levelorder");
  const [traversal, setTraversal] = useState(null);
  const [status, setStatus] = useState({
    type: "info",
    message: "Cargando árbol general...",
  });
  const [isLoading, setIsLoading] = useState(false);

  const traversalOrder = useMemo(() => traversal?.order || [], [traversal]);

  const applyTreePayload = useCallback(
    (payload, visualState = {}) => {
      const normalizedTraversalOrder = visualState.traversalOrder || [];
      const normalizedHighlight = visualState.highlightedId || "";

      setNodes(
        normalizeNodes(payload.nodes || [], {
          highlightedId: normalizedHighlight,
          traversalOrder: normalizedTraversalOrder,
        }),
      );
      setEdges(normalizeEdges(payload.edges || [], normalizedTraversalOrder));
      setMetrics(payload.metrics || null);
      setTree(payload.result?.tree || payload.tree || null);
    },
    [setEdges, setNodes],
  );

  const refreshTree = useCallback(
    async (visualState = {}) => {
      const response = await getGeneralTreeState();
      const payload = getPayload(response);
      applyTreePayload(payload, visualState);
      return payload;
    },
    [applyTreePayload],
  );

  useEffect(() => {
    const loadInitialState = async () => {
      setIsLoading(true);

      try {
        const payload = await refreshTree({ highlightedId: "", traversalOrder: [] });

        if ((payload.nodes || []).length === 0) {
          const demoResponse = await loadGeneralTreeDemo();
          const demoPayload = getPayload(demoResponse);
          applyTreePayload(demoPayload, { highlightedId: "", traversalOrder: [] });
          setStatus({
            type: "success",
            message: "Dataset demo cargado para el árbol general.",
          });
          return;
        }

        setStatus({
          type: "success",
          message: "Estado del árbol general obtenido correctamente.",
        });
      } catch (error) {
        setStatus({
          type: "error",
          message: getApiErrorMessage(error),
        });
      } finally {
        setIsLoading(false);
      }
    };

    loadInitialState();
  }, [applyTreePayload, refreshTree]);

  useEffect(() => {
    setNodes((currentNodes) =>
      normalizeNodes(currentNodes, {
        highlightedId,
        traversalOrder,
      }),
    );
    setEdges((currentEdges) => normalizeEdges(currentEdges, traversalOrder));
  }, [highlightedId, setEdges, setNodes, traversalOrder]);

  const metricsCards = useMemo(
    () => [
      { label: "Nodos", value: metrics?.count ?? 0 },
      { label: "Altura", value: metrics?.height ?? 0 },
      { label: "Niveles", value: metrics?.levels ?? 0 },
      { label: "Hojas", value: metrics?.leafCount ?? 0 },
      { label: "Máx. hijos", value: metrics?.maxChildren ?? 0 },
      { label: "Aristas", value: metrics?.edgesCount ?? 0 },
    ],
    [metrics],
  );

  const hasNodes = nodes.length > 0;

  const rootLabel = useMemo(() => {
    if (!tree?.root) {
      return "Sin raíz";
    }

    return tree.root.label || tree.root.id;
  }, [tree]);

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const runAction = async (action) => {
    setIsLoading(true);

    try {
      await action();
    } catch (error) {
      setStatus({
        type: "error",
        message: getApiErrorMessage(error),
      });
    } finally {
      setIsLoading(false);
    }
  };

  const clearVisualMarks = () => {
    setHighlightedId("");
    setTraversal(null);
  };

  const handleLoadDemo = () =>
    runAction(async () => {
      const response = await loadGeneralTreeDemo();
      const payload = getPayload(response);

      clearVisualMarks();
      applyTreePayload(payload, { highlightedId: "", traversalOrder: [] });
      setStatus({
        type: "success",
        message: "Dataset demo cargado correctamente.",
      });
    });

  const handleReset = () =>
    runAction(async () => {
      const response = await resetGeneralTree();
      const payload = getPayload(response);

      clearVisualMarks();
      applyTreePayload(payload, { highlightedId: "", traversalOrder: [] });
      setForm(initialForm);
      setDeleteId("");
      setSearchId("");
      setStatus({
        type: "success",
        message: "Árbol general reiniciado correctamente.",
      });
    });

  const handleInsert = (event) => {
    event.preventDefault();

    runAction(async () => {
      const nodeId = form.id.trim();
      const label = form.label.trim();
      const parentId = form.parentId.trim();

      if (!nodeId || !label) {
        setStatus({
          type: "error",
          message: "El ID y la etiqueta del nodo son obligatorios.",
        });
        return;
      }

      const response = await insertGeneralTreeNode({
        id: nodeId,
        label,
        parentId: parentId || null,
        category: form.category,
        metadata: buildMetadata(form),
      });
      const payload = getPayload(response);

      setHighlightedId(nodeId);
      setTraversal(null);
      applyTreePayload(payload, { highlightedId: nodeId, traversalOrder: [] });
      setForm(initialForm);
      setStatus({
        type: "success",
        message: `Nodo ${nodeId} insertado correctamente.`,
      });
    });
  };

  const handleDelete = (event) => {
    event.preventDefault();

    runAction(async () => {
      const nodeId = deleteId.trim();

      if (!nodeId) {
        setStatus({
          type: "error",
          message: "Indica el ID del nodo que deseas eliminar.",
        });
        return;
      }

      const response = await deleteGeneralTreeNode(nodeId);
      const payload = getPayload(response);

      clearVisualMarks();
      applyTreePayload(payload, { highlightedId: "", traversalOrder: [] });
      setDeleteId("");
      setStatus({
        type: "success",
        message: `Nodo ${nodeId} eliminado junto con su subárbol.`,
      });
    });
  };

  const handleSearch = (event) => {
    event.preventDefault();

    runAction(async () => {
      const nodeId = searchId.trim();

      if (!nodeId) {
        setStatus({
          type: "error",
          message: "Indica el ID del nodo que deseas buscar.",
        });
        return;
      }

      const response = await searchGeneralTreeNode(nodeId);
      const payload = getPayload(response);
      const result = payload.result || {};
      const nextHighlight = result.found ? nodeId : "";

      setHighlightedId(nextHighlight);
      setTraversal(null);
      applyTreePayload(payload, { highlightedId: nextHighlight, traversalOrder: [] });
      setStatus({
        type: result.found ? "success" : "error",
        message: result.found
          ? `Nodo ${nodeId} encontrado en nivel ${result.level}.`
          : `El nodo ${nodeId} no existe en el árbol.`,
      });
    });
  };

  const handleTraversal = () =>
    runAction(async () => {
      const response = await traverseGeneralTree(traversalType);
      const payload = getPayload(response);
      const nextTraversal = payload.traversal || payload.result?.traversal || null;
      const nextOrder = nextTraversal?.order || [];

      setTraversal(nextTraversal);
      setHighlightedId("");
      applyTreePayload(payload, { highlightedId: "", traversalOrder: nextOrder });
      setStatus({
        type: "success",
        message: `Recorrido ${traversalType} obtenido correctamente.`,
      });
    });

  const statusClass =
    status.type === "error"
      ? "border-red-800 bg-red-950 text-red-200"
      : status.type === "success"
        ? "border-green-800 bg-green-950 text-green-200"
        : "border-cyan-800 bg-cyan-950 text-cyan-200";

  return (
    <MainLayout>
      <section className="space-y-6">
        <div className="flex flex-col gap-4 rounded-2xl border border-gray-700 bg-gray-800 p-6 shadow-lg lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-widest text-cyan-400">
              Épica 5
            </p>
            <h2 className="mt-2 text-2xl font-bold text-white">
              Árbol General del Pensum Académico
            </h2>
            <p className="mt-2 max-w-3xl text-gray-300">
              Visualiza y manipula la jerarquía Facultad → Carrera → Ciclos → Cursos
              usando Flask, Python puro y React Flow.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={handleLoadDemo}
              disabled={isLoading}
              className="rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              Cargar demo
            </button>
            <button
              type="button"
              onClick={handleReset}
              disabled={isLoading}
              className="rounded-xl border border-red-700 px-4 py-2 font-semibold text-red-200 transition hover:bg-red-950 disabled:cursor-not-allowed disabled:opacity-60"
            >
              Reiniciar
            </button>
          </div>
        </div>

        <div className={`rounded-xl border px-4 py-3 text-sm ${statusClass}`}>
          {isLoading ? "Procesando operación..." : status.message}
        </div>

        <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
          {metricsCards.map((metric) => (
            <article
              key={metric.label}
              className="rounded-2xl border border-gray-700 bg-gray-800 p-4 shadow-lg"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">
                {metric.label}
              </p>
              <p className="mt-2 text-2xl font-bold text-white">
                {metric.value}
              </p>
            </article>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
          <aside className="space-y-6">
            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Insertar nodo</h3>
              <p className="mt-2 text-sm text-gray-400">
                Usa parentId para colgar el nodo de un padre existente. Déjalo vacío
                solo cuando el árbol esté vacío y vayas a crear la raíz.
              </p>

              <form className="mt-4 space-y-3" onSubmit={handleInsert}>
                <input
                  name="id"
                  value={form.id}
                  onChange={handleFormChange}
                  placeholder="ID, ej. programming-2"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <input
                  name="label"
                  value={form.label}
                  onChange={handleFormChange}
                  placeholder="Etiqueta, ej. Programación II"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <input
                  name="parentId"
                  value={form.parentId}
                  onChange={handleFormChange}
                  placeholder="ID padre, ej. cycle-2"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <select
                  name="category"
                  value={form.category}
                  onChange={handleFormChange}
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                >
                  {categoryOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>

                <input
                  name="metadataCode"
                  value={form.metadataCode}
                  onChange={handleFormChange}
                  placeholder="Código opcional, ej. SIS-202"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Insertar
                </button>
              </form>
            </article>

            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Eliminar nodo</h3>
              <p className="mt-2 text-sm text-gray-400">
                La eliminación remueve el nodo y todo su subárbol.
              </p>

              <form className="mt-4 space-y-3" onSubmit={handleDelete}>
                <input
                  value={deleteId}
                  onChange={(event) => setDeleteId(event.target.value)}
                  placeholder="ID a eliminar"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-red-500"
                />

                <button
                  type="submit"
                  disabled={isLoading || !hasNodes}
                  className="w-full rounded-xl bg-red-700 px-4 py-2 font-semibold text-white transition hover:bg-red-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Eliminar
                </button>
              </form>
            </article>

            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Buscar nodo</h3>
              <p className="mt-2 text-sm text-gray-400">
                Si el nodo existe, se resalta en amarillo sobre React Flow.
              </p>

              <form className="mt-4 space-y-3" onSubmit={handleSearch}>
                <input
                  value={searchId}
                  onChange={(event) => setSearchId(event.target.value)}
                  placeholder="ID a buscar"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-yellow-500"
                />

                <button
                  type="submit"
                  disabled={isLoading || !hasNodes}
                  className="w-full rounded-xl bg-yellow-600 px-4 py-2 font-semibold text-white transition hover:bg-yellow-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Buscar
                </button>
              </form>
            </article>

            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Recorridos</h3>
              <p className="mt-2 text-sm text-gray-400">
                Levelorder usa la Queue manual del backend.
              </p>

              <div className="mt-4 flex gap-3">
                <select
                  value={traversalType}
                  onChange={(event) => setTraversalType(event.target.value)}
                  className="min-w-0 flex-1 rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-indigo-500"
                >
                  {traversalOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>

                <button
                  type="button"
                  onClick={handleTraversal}
                  disabled={isLoading || !hasNodes}
                  className="rounded-xl bg-indigo-600 px-4 py-2 font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Ver
                </button>
              </div>

              {traversal && (
                <div className="mt-4 rounded-xl border border-indigo-800 bg-indigo-950/40 p-3">
                  <p className="text-sm font-semibold text-indigo-200">
                    {traversal.type} desde {traversal.start || "N/A"}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {traversal.steps.map((step) => (
                      <span
                        key={`${step.step}-${step.id}`}
                        className="rounded-full bg-indigo-700 px-3 py-1 text-xs font-semibold text-white"
                      >
                        {step.step}. {step.label}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </article>
          </aside>

          <section className="space-y-6">
            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-white">
                    Visualización React Flow
                  </h3>
                  <p className="mt-1 text-sm text-gray-400">
                    Raíz actual: <span className="font-semibold text-cyan-300">{rootLabel}</span>
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => refreshTree({ highlightedId, traversalOrder })}
                  disabled={isLoading}
                  className="rounded-xl border border-gray-600 px-4 py-2 text-sm font-semibold text-gray-200 transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Refrescar
                </button>
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
                  <div className="flex h-full items-center justify-center p-8 text-center">
                    <div>
                      <p className="text-lg font-semibold text-white">
                        El árbol está vacío.
                      </p>
                      <p className="mt-2 max-w-md text-gray-400">
                        Inserta un nodo raíz o carga el dataset demo para iniciar la visualización.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </article>

            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Estado estructural</h3>
              <p className="mt-2 text-sm text-gray-400">
                Representación JSON del árbol para validar la jerarquía académica sin depender de la vista.
              </p>

              <pre className="mt-4 max-h-80 overflow-auto rounded-xl border border-gray-700 bg-gray-950 p-4 text-xs text-gray-200">
                {JSON.stringify(tree || { root: null, size: 0 }, null, 2)}
              </pre>
            </article>
          </section>
        </div>
      </section>
    </MainLayout>
  );
};

export default GeneralTreePage;
