import { useCallback, useEffect, useMemo, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MarkerType,
  MiniMap,
  useEdgesState,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";

import {
  addGraphEdge,
  addGraphNode,
  getGraphState,
  loadGraphDemo,
  resetGraph,
  runGraphBfs,
  runGraphDfs,
  searchGraphCourse,
} from "../api/graph";
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

const normalizeCourseId = (value) => String(value ?? "").trim();

const getCourseName = (metadata) => {
  const value = metadata?.value;

  if (value && typeof value === "object") {
    return value.name || value.label || value.course_name || "Curso sin nombre";
  }

  return String(value || metadata?.id || "Curso");
};

const getCourseCode = (metadata, fallbackId) => {
  const value = metadata?.value;

  if (value && typeof value === "object") {
    return value.code || value.id || fallbackId;
  }

  return fallbackId;
};

const createGraphLabel = ({ nodeId, metadata, visitOrder, isActive }) => {
  const code = getCourseCode(metadata, nodeId);
  const name = getCourseName(metadata);
  const inDegree = metadata?.inDegree ?? 0;
  const outDegree = metadata?.outDegree ?? metadata?.degree ?? 0;

  return (
    <div className="min-w-[190px] text-center">
      <div className="flex items-center justify-center gap-2">
        <span className="rounded-lg bg-slate-950 px-2 py-1 font-mono text-xs font-bold text-cyan-100">
          {code}
        </span>
        {visitOrder !== null && visitOrder !== undefined && (
          <span className="rounded-full border border-lime-300 bg-lime-500/20 px-2 py-1 text-[10px] font-bold text-lime-100">
            #{visitOrder + 1}
          </span>
        )}
      </div>
      <p className="mt-2 text-sm font-semibold leading-tight text-white">{name}</p>
      <p className="mt-2 text-[11px] uppercase tracking-wide text-gray-300">
        Entrada {inDegree} · Salida {outDegree}
      </p>
      {isActive && (
        <p className="mt-2 rounded-lg border border-yellow-300 bg-yellow-500/20 px-2 py-1 text-[10px] font-bold text-yellow-100">
          Visitando ahora
        </p>
      )}
    </div>
  );
};

const normalizeGraphNodes = (nodes = [], visualState = {}) => {
  const visitedIds = visualState.visitedIds || new Set();
  const activeNodeId = visualState.activeNodeId || "";
  const searchNodeId = visualState.searchNodeId || "";
  const visitIndex = visualState.visitIndex || new Map();

  return nodes.map((node) => {
    const nodeId = String(node.id);
    const metadata = node?.data?.metadata || {};
    const isVisited = visitedIds.has(nodeId);
    const isActive = activeNodeId === nodeId;
    const isSearchMatch = searchNodeId === nodeId;
    const category = node?.data?.category;

    const borderColor = isActive
      ? "#facc15"
      : isSearchMatch
        ? "#fb923c"
        : isVisited
          ? "#84cc16"
          : category === "source-course"
            ? "#22d3ee"
            : category === "terminal-course"
              ? "#a78bfa"
              : "#64748b";

    const backgroundColor = isActive
      ? "#713f12"
      : isSearchMatch
        ? "#431407"
        : isVisited
          ? "#1a2e05"
          : "#111827";

    return {
      ...node,
      draggable: false,
      data: {
        ...node.data,
        label: createGraphLabel({
          nodeId,
          metadata,
          visitOrder: visitIndex.get(nodeId),
          isActive,
        }),
      },
      style: {
        border: `2px solid ${borderColor}`,
        borderRadius: 18,
        background: backgroundColor,
        color: "#f8fafc",
        padding: 10,
        width: 230,
        boxShadow: isActive || isSearchMatch ? `0 0 0 4px ${borderColor}33` : "none",
      },
    };
  });
};

const normalizeGraphEdges = (edges = [], visualState = {}) => {
  const highlightedEdges = visualState.highlightedEdges || new Set();

  return edges.map((edge) => {
    const edgeKey = `${edge.source}->${edge.target}`;
    const isHighlighted = highlightedEdges.has(edgeKey);

    return {
      ...edge,
      animated: isHighlighted,
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: isHighlighted ? "#84cc16" : "#64748b",
      },
      style: {
        stroke: isHighlighted ? "#84cc16" : "#64748b",
        strokeWidth: isHighlighted ? 3 : 2,
      },
      label: edge?.label || edge?.data?.label || "habilita",
      labelStyle: {
        fill: isHighlighted ? "#bef264" : "#cbd5e1",
        fontWeight: 700,
      },
    };
  });
};

const buildHighlightedEdges = (steps = [], visitedIds = new Set()) => {
  const edges = new Set();

  steps.forEach((step) => {
    const source = step?.edge?.source;
    const target = step?.edge?.target;

    if (source && target && visitedIds.has(String(source)) && visitedIds.has(String(target))) {
      edges.add(`${source}->${target}`);
    }
  });

  return edges;
};


const getGraphCourseOptions = (payload = {}) => {
  const optionsById = new Map();

  const addOption = (nodeId, value = {}) => {
    const normalizedId = normalizeCourseId(nodeId);
    if (!normalizedId || optionsById.has(normalizedId)) {
      return;
    }

    const metadata = { value };
    optionsById.set(normalizedId, {
      id: normalizedId,
      code: getCourseCode(metadata, normalizedId),
      name: getCourseName(metadata),
    });
  };

  (payload?.graph?.nodes || []).forEach((node) => {
    addOption(node?.id, node?.value);
  });

  (payload?.nodes || []).forEach((node) => {
    const metadata = node?.data?.metadata || {};
    const value = metadata?.value || {};
    addOption(node?.id, value);
  });

  return Array.from(optionsById.values()).sort((left, right) => left.id.localeCompare(right.id));
};

const GraphPage = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [graphPayload, setGraphPayload] = useState({});
  const [traversal, setTraversal] = useState(null);
  const [animationIndex, setAnimationIndex] = useState(-1);
  const [selectedStartNode, setSelectedStartNode] = useState("");
  const [searchValue, setSearchValue] = useState("");
  const [searchResult, setSearchResult] = useState(null);
  const [newNodeId, setNewNodeId] = useState("");
  const [newNodeName, setNewNodeName] = useState("");
  const [edgeSource, setEdgeSource] = useState("");
  const [edgeTarget, setEdgeTarget] = useState("");
  const [statusMessage, setStatusMessage] = useState("Cargando grafo...");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const courseOptions = useMemo(() => getGraphCourseOptions(graphPayload), [graphPayload]);
  const metrics = graphPayload?.metrics || {};

  const visitedIds = useMemo(() => {
    const order = traversal?.order || [];
    if (animationIndex < 0) {
      return new Set();
    }
    return new Set(order.slice(0, animationIndex + 1).map(String));
  }, [animationIndex, traversal]);

  const visitIndex = useMemo(() => {
    const order = traversal?.order || [];
    const indexMap = new Map();
    order.forEach((nodeId, index) => {
      if (animationIndex >= index) {
        indexMap.set(String(nodeId), index);
      }
    });
    return indexMap;
  }, [animationIndex, traversal]);

  const visualState = useMemo(() => ({
    visitedIds,
    activeNodeId: animationIndex >= 0 ? String(traversal?.order?.[animationIndex] || "") : "",
    searchNodeId: searchResult?.found ? String(searchResult?.nodeId || searchResult?.node?.id || "") : "",
    visitIndex,
    highlightedEdges: buildHighlightedEdges(traversal?.steps || [], visitedIds),
  }), [animationIndex, searchResult, traversal, visitIndex, visitedIds]);

  const hydrateGraph = useCallback((payload) => {
    setGraphPayload(payload);
    setNodes(normalizeGraphNodes(payload?.nodes || [], visualState));
    setEdges(normalizeGraphEdges(payload?.edges || [], visualState));

    const firstNodeId = getGraphCourseOptions(payload)[0]?.id;
    if (!selectedStartNode && firstNodeId) {
      setSelectedStartNode(String(firstNodeId));
    }
  }, [selectedStartNode, setEdges, setNodes, visualState]);

  useEffect(() => {
    setNodes(normalizeGraphNodes(graphPayload?.nodes || [], visualState));
    setEdges(normalizeGraphEdges(graphPayload?.edges || [], visualState));
  }, [graphPayload, setEdges, setNodes, visualState]);

  const executeRequest = useCallback(async (request, successMessage) => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await request();
      const payload = getPayload(response);
      hydrateGraph(payload);
      setStatusMessage(successMessage || response?.message || "Operación completada.");
      return payload;
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [hydrateGraph]);

  const loadState = useCallback(async () => {
    const payload = await executeRequest(getGraphState, "Estado del grafo cargado.");

    if (payload?.isEmpty) {
      await executeRequest(loadGraphDemo, "Dataset demo de prerrequisitos cargado.");
    }
  }, [executeRequest]);

  useEffect(() => {
    loadState();
  }, [loadState]);

  const handleLoadDemo = async () => {
    setTraversal(null);
    setAnimationIndex(-1);
    setSearchResult(null);
    await executeRequest(loadGraphDemo, "Dataset demo de prerrequisitos cargado.");
  };

  const handleReset = async () => {
    setTraversal(null);
    setAnimationIndex(-1);
    setSearchResult(null);
    await executeRequest(resetGraph, "Grafo reiniciado correctamente.");
  };

  const handleAddNode = async (event) => {
    event.preventDefault();
    const id = normalizeCourseId(newNodeId);

    if (!id) {
      setErrorMessage("Ingresa un código de curso válido.");
      return;
    }

    const value = {
      code: id,
      name: newNodeName.trim() || `Curso ${id}`,
    };

    const payload = await executeRequest(
      () => addGraphNode({ id, value }),
      `Nodo ${id} agregado al grafo.`
    );

    if (payload) {
      setNewNodeId("");
      setNewNodeName("");
      setTraversal(null);
      setAnimationIndex(-1);
    }
  };

  const handleAddEdge = async (event) => {
    event.preventDefault();
    const source = normalizeCourseId(edgeSource);
    const target = normalizeCourseId(edgeTarget);

    if (!source || !target) {
      setErrorMessage("Selecciona prerrequisito y curso destino.");
      return;
    }

    const payload = await executeRequest(
      () => addGraphEdge({ source, target }),
      `Relación ${source} -> ${target} agregada.`
    );

    if (payload) {
      setEdgeSource("");
      setEdgeTarget("");
      setTraversal(null);
      setAnimationIndex(-1);
    }
  };

  const runTraversal = async (algorithm) => {
    const startNodeId = normalizeCourseId(selectedStartNode);

    if (!startNodeId) {
      setErrorMessage("Selecciona un nodo inicial para ejecutar el recorrido.");
      return;
    }

    setSearchResult(null);
    const request = algorithm === "DFS" ? runGraphDfs : runGraphBfs;
    const payload = await executeRequest(
      () => request(startNodeId),
      `Recorrido ${algorithm} ejecutado desde ${startNodeId}.`
    );

    if (payload?.traversal) {
      setTraversal(payload.traversal);
      setAnimationIndex(0);
    }
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    const courseId = normalizeCourseId(searchValue);

    if (!courseId) {
      setErrorMessage("Ingresa el código del curso que deseas buscar.");
      return;
    }

    setTraversal(null);
    setAnimationIndex(-1);
    const payload = await executeRequest(
      () => searchGraphCourse(courseId),
      `Búsqueda de ${courseId} ejecutada.`
    );

    if (payload?.search) {
      setSearchResult(payload.search);
    }
  };

  const handlePreviousStep = () => {
    setAnimationIndex((current) => Math.max(0, current - 1));
  };

  const handleNextStep = () => {
    const maxIndex = (traversal?.order?.length || 1) - 1;
    setAnimationIndex((current) => Math.min(maxIndex, current + 1));
  };

  const handleResetVisual = () => {
    setTraversal(null);
    setAnimationIndex(-1);
    setSearchResult(null);
    setStatusMessage("Visualización reiniciada sin modificar el grafo.");
  };

  const traversalOrder = traversal?.order || [];
  const activeStep = traversal?.steps?.[animationIndex] || null;

  return (
    <MainLayout>
      <section className="space-y-6">
        <div className="rounded-2xl border border-gray-700 bg-gray-800 p-6 shadow-lg">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-cyan-300">
                Épica 10 — Grafos DFS/BFS
              </p>
              <h2 className="mt-2 text-2xl font-bold text-white">
                Mapa de prerrequisitos universitarios
              </h2>
              <p className="mt-3 max-w-3xl text-gray-300">
                Grafo dirigido implementado manualmente con lista de adyacencia. Cada arista indica que un curso prerrequisito habilita otro curso.
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
                onClick={handleResetVisual}
                disabled={isLoading}
                className="rounded-xl bg-slate-700 px-4 py-2 font-semibold text-white transition hover:bg-slate-600 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Reset visual
              </button>
              <button
                type="button"
                onClick={handleReset}
                disabled={isLoading}
                className="rounded-xl bg-red-700 px-4 py-2 font-semibold text-white transition hover:bg-red-600 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Vaciar grafo
              </button>
            </div>
          </div>

          <div className="mt-5 grid gap-3 md:grid-cols-5">
            <MetricCard label="Vértices" value={metrics.verticesCount ?? graphPayload.verticesCount ?? 0} />
            <MetricCard label="Aristas" value={metrics.edgesCount ?? graphPayload.edgesCount ?? 0} />
            <MetricCard label="Componentes" value={metrics.connectedComponents ?? 0} />
            <MetricCard label="Grado salida máx." value={metrics.maxOutDegree ?? 0} />
            <MetricCard label="Densidad" value={metrics.density ?? 0} />
          </div>

          {(statusMessage || errorMessage) && (
            <div className="mt-5 grid gap-3 lg:grid-cols-2">
              {statusMessage && (
                <p className="rounded-xl border border-cyan-700 bg-cyan-950/40 px-4 py-3 text-sm text-cyan-100">
                  {statusMessage}
                </p>
              )}
              {errorMessage && (
                <p className="rounded-xl border border-red-700 bg-red-950/40 px-4 py-3 text-sm font-semibold text-red-100">
                  {errorMessage}
                </p>
              )}
            </div>
          )}
        </div>

        <div className="grid gap-6 xl:grid-cols-[360px_1fr]">
          <aside className="space-y-6">
            <ControlPanel title="Recorridos DFS/BFS">
              <label className="block text-sm font-semibold text-gray-200" htmlFor="start-node">
                Nodo inicial
              </label>
              <select
                id="start-node"
                value={selectedStartNode}
                onChange={(event) => setSelectedStartNode(event.target.value)}
                className="mt-2 w-full rounded-xl border border-gray-600 bg-gray-950 px-3 py-2 text-white outline-none focus:border-cyan-400"
              >
                <option value="">Seleccionar curso</option>
                {courseOptions.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.code} — {course.name}
                  </option>
                ))}
              </select>

              <div className="mt-4 grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => runTraversal("DFS")}
                  disabled={isLoading || !selectedStartNode}
                  className="rounded-xl bg-lime-700 px-4 py-2 font-semibold text-white transition hover:bg-lime-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Ejecutar DFS
                </button>
                <button
                  type="button"
                  onClick={() => runTraversal("BFS")}
                  disabled={isLoading || !selectedStartNode}
                  className="rounded-xl bg-purple-700 px-4 py-2 font-semibold text-white transition hover:bg-purple-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Ejecutar BFS
                </button>
              </div>

              {traversalOrder.length > 0 && (
                <div className="mt-5 rounded-xl border border-gray-700 bg-gray-950 p-4">
                  <p className="text-sm font-semibold text-white">
                    Orden {traversal?.algorithm}: {traversalOrder.join(" → ")}
                  </p>
                  <p className="mt-2 text-xs text-gray-400">
                    Paso actual: {animationIndex + 1} de {traversalOrder.length}
                  </p>

                  {activeStep && (
                    <p className="mt-3 rounded-lg bg-gray-900 px-3 py-2 text-xs text-gray-200">
                      {activeStep.action || "visit"}: {activeStep.nodeId || traversalOrder[animationIndex]}
                    </p>
                  )}

                  <div className="mt-4 grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={handlePreviousStep}
                      disabled={animationIndex <= 0}
                      className="rounded-xl bg-gray-700 px-3 py-2 text-sm font-semibold text-white transition hover:bg-gray-600 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      Anterior
                    </button>
                    <button
                      type="button"
                      onClick={handleNextStep}
                      disabled={animationIndex >= traversalOrder.length - 1}
                      className="rounded-xl bg-gray-700 px-3 py-2 text-sm font-semibold text-white transition hover:bg-gray-600 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      Siguiente
                    </button>
                  </div>
                </div>
              )}
            </ControlPanel>

            <ControlPanel title="Buscar curso">
              <form onSubmit={handleSearch} className="space-y-3">
                <input
                  type="text"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="Ej. CS-301"
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-3 py-2 text-white outline-none focus:border-cyan-400"
                />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-xl bg-orange-700 px-4 py-2 font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Buscar
                </button>
              </form>

              {searchResult && (
                <p className={`mt-3 rounded-xl px-3 py-2 text-sm font-semibold ${searchResult.found ? "border border-orange-400 bg-orange-500/20 text-orange-100" : "border border-red-700 bg-red-950/40 text-red-100"}`}>
                  {searchResult.found ? `Curso encontrado: ${searchResult.nodeId}` : "Curso no encontrado"}
                </p>
              )}
            </ControlPanel>

            <ControlPanel title="Agregar nodo">
              <form onSubmit={handleAddNode} className="space-y-3">
                <input
                  type="text"
                  value={newNodeId}
                  onChange={(event) => setNewNodeId(event.target.value)}
                  placeholder="Código del curso"
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-3 py-2 text-white outline-none focus:border-cyan-400"
                />
                <input
                  type="text"
                  value={newNodeName}
                  onChange={(event) => setNewNodeName(event.target.value)}
                  placeholder="Nombre del curso"
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-3 py-2 text-white outline-none focus:border-cyan-400"
                />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-xl bg-cyan-700 px-4 py-2 font-semibold text-white transition hover:bg-cyan-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Agregar nodo
                </button>
              </form>
            </ControlPanel>

            <ControlPanel title="Agregar prerrequisito">
              <form onSubmit={handleAddEdge} className="space-y-3">
                <select
                  value={edgeSource}
                  onChange={(event) => setEdgeSource(event.target.value)}
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-3 py-2 text-white outline-none focus:border-cyan-400"
                >
                  <option value="">Curso prerrequisito</option>
                  {courseOptions.map((course) => (
                    <option key={`source-${course.id}`} value={course.id}>
                      {course.code} — {course.name}
                    </option>
                  ))}
                </select>
                <select
                  value={edgeTarget}
                  onChange={(event) => setEdgeTarget(event.target.value)}
                  className="w-full rounded-xl border border-gray-600 bg-gray-950 px-3 py-2 text-white outline-none focus:border-cyan-400"
                >
                  <option value="">Curso habilitado</option>
                  {courseOptions.map((course) => (
                    <option key={`target-${course.id}`} value={course.id}>
                      {course.code} — {course.name}
                    </option>
                  ))}
                </select>
                <button
                  type="submit"
                  disabled={isLoading || courseOptions.length < 2}
                  className="w-full rounded-xl bg-indigo-700 px-4 py-2 font-semibold text-white transition hover:bg-indigo-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Agregar arista
                </button>
              </form>
            </ControlPanel>
          </aside>

          <div className="min-h-[760px] rounded-2xl border border-gray-700 bg-gray-900 shadow-lg">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              fitView
              fitViewOptions={{ padding: 0.25 }}
              nodesDraggable={false}
            >
              <MiniMap pannable zoomable />
              <Controls />
              <Background gap={22} size={1} />
            </ReactFlow>
          </div>
        </div>
      </section>
    </MainLayout>
  );
};

const MetricCard = ({ label, value }) => (
  <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
    <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">{label}</p>
    <p className="mt-2 text-2xl font-bold text-white">{value}</p>
  </article>
);

const ControlPanel = ({ title, children }) => (
  <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
    <h3 className="text-lg font-semibold text-white">{title}</h3>
    <div className="mt-4">{children}</div>
  </article>
);

export default GraphPage;
