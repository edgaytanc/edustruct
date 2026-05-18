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
  deleteAVLValue,
  getAVLState,
  insertAVLValue,
  loadAVLDemo,
  resetAVLTree,
  searchAVLValue,
  traverseAVLTree,
} from "../api/avl";
import MainLayout from "../components/layout/MainLayout";

const traversalOptions = [
  { value: "levelorder", label: "Levelorder" },
  { value: "preorder", label: "Preorder" },
  { value: "inorder", label: "Inorder" },
  { value: "postorder", label: "Postorder" },
];

const animationSpeedOptions = [
  { value: 1200, label: "Lenta" },
  { value: 750, label: "Normal" },
  { value: 400, label: "Rápida" },
];

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

const getRawNodeLabel = (node) => {
  if (typeof node?.data?.rawLabel === "string") {
    return node.data.rawLabel;
  }

  if (typeof node?.data?.label === "string") {
    return node.data.label;
  }

  return String(node?.id || "Nodo");
};

const normalizeAVLNodes = (nodes = [], visualState = {}) => {
  const highlightedId = visualState.highlightedId || "";
  const pivotId = visualState.pivotId || "";
  const traversalOrder = visualState.traversalOrder || [];
  const traversalIndexById = new Map(
    traversalOrder.map((nodeId, index) => [String(nodeId), index + 1]),
  );

  return nodes.map((node) => {
    const nodeId = String(node.id);
    const rawLabel = getRawNodeLabel(node);
    const metadata = node?.data?.metadata || {};
    const direction = metadata.direction || "root";
    const balanceFactor = Number(metadata.balanceFactor ?? 0);
    const height = Number(metadata.height ?? 1);
    const visualHeight = Number(metadata.visualHeight ?? Math.max(height - 1, 0));
    const isUnbalanced = Boolean(metadata.isUnbalanced || Math.abs(balanceFactor) > 1);
    const isHighlighted = highlightedId && nodeId === String(highlightedId);
    const isPivot = pivotId && nodeId === String(pivotId);
    const traversalStep = traversalIndexById.get(nodeId);
    const isTraversalNode = Boolean(traversalStep);

    const borderColor = isUnbalanced
      ? "#ef4444"
      : isPivot
        ? "#f97316"
        : isHighlighted
          ? "#facc15"
          : isTraversalNode
            ? "#818cf8"
            : "#14b8a6";

    const backgroundColor = isUnbalanced
      ? "#450a0a"
      : isPivot
        ? "#431407"
        : isHighlighted
          ? "#713f12"
          : isTraversalNode
            ? "#312e81"
            : "#111827";

    return {
      ...node,
      draggable: false,
      data: {
        ...node.data,
        rawLabel,
        label: (
          <div className="min-w-32 text-center">
            <div className="flex items-start justify-center gap-2">
              <p className="text-lg font-bold leading-snug text-white">
                {rawLabel}
              </p>
              {traversalStep && (
                <span className="rounded-full bg-indigo-500 px-2 py-0.5 text-[10px] font-bold text-white">
                  {traversalStep}
                </span>
              )}
            </div>

            <div className="mt-2 flex items-center justify-center gap-2 text-[11px] font-semibold">
              <span className="rounded-full bg-gray-950 px-2 py-0.5 text-cyan-200">
                h={height}
              </span>
              <span
                className={`rounded-full px-2 py-0.5 ${
                  Math.abs(balanceFactor) > 1
                    ? "bg-red-700 text-white"
                    : "bg-emerald-700 text-white"
                }`}
              >
                BF={balanceFactor}
              </span>
            </div>

            <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-teal-200">
              {direction === "left" ? "Izquierda" : direction === "right" ? "Derecha" : "Raíz"}
            </p>
            <p className="mt-1 text-xs text-gray-300">
              Nivel {metadata.level ?? 0} · Altura visual {visualHeight}
            </p>
            {isPivot && (
              <p className="mt-1 text-[11px] font-bold uppercase tracking-wide text-orange-300">
                pivote
              </p>
            )}
            {isUnbalanced && (
              <p className="mt-1 text-[11px] font-bold uppercase tracking-wide text-red-300">
                desbalance
              </p>
            )}
          </div>
        ),
      },
      style: {
        border: `2px solid ${borderColor}`,
        borderRadius: "999px",
        background: backgroundColor,
        color: "#e5e7eb",
        padding: "12px",
        minWidth: "136px",
        minHeight: "116px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        boxShadow: `0 14px 34px ${borderColor}33`,
      },
    };
  });
};

const normalizeAVLEdges = (edges = [], traversalOrder = []) => {
  const traversalPairs = new Set();

  for (let index = 0; index < traversalOrder.length - 1; index += 1) {
    traversalPairs.add(`${traversalOrder[index]}-${traversalOrder[index + 1]}`);
  }

  return edges.map((edge) => {
    const isTraversalEdge = traversalPairs.has(`${edge.source}-${edge.target}`);

    return {
      ...edge,
      animated: isTraversalEdge,
      label: edge.label || edge?.data?.relationship || "",
      style: {
        strokeWidth: isTraversalEdge ? 3 : 2,
        stroke: isTraversalEdge ? "#818cf8" : "#14b8a6",
      },
      labelStyle: {
        fill: "#cbd5e1",
        fontWeight: 700,
      },
    };
  });
};

const AVLPage = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [beforeNodes, setBeforeNodes] = useState([]);
  const [beforeEdges, setBeforeEdges] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [tree, setTree] = useState(null);
  const [insertValue, setInsertValue] = useState("");
  const [deleteValue, setDeleteValue] = useState("");
  const [searchValue, setSearchValue] = useState("");
  const [highlightedId, setHighlightedId] = useState("");
  const [pivotId, setPivotId] = useState("");
  const [traversalType, setTraversalType] = useState("levelorder");
  const [traversal, setTraversal] = useState(null);
  const [activeTraversalOrder, setActiveTraversalOrder] = useState([]);
  const [currentTraversalIndex, setCurrentTraversalIndex] = useState(-1);
  const [isAnimatingTraversal, setIsAnimatingTraversal] = useState(false);
  const [animationSpeed, setAnimationSpeed] = useState(750);
  const [rotationEvents, setRotationEvents] = useState([]);
  const [lastRotation, setLastRotation] = useState(null);
  const [activeView, setActiveView] = useState("after");
  const [status, setStatus] = useState({
    type: "info",
    message: "Cargando árbol AVL...",
  });
  const [isLoading, setIsLoading] = useState(false);

  const traversalOrder = useMemo(
    () => (traversal?.order || []).map((value) => String(value)),
    [traversal],
  );

  const currentTraversalNodeId = useMemo(() => {
    if (currentTraversalIndex < 0 || currentTraversalIndex >= traversalOrder.length) {
      return "";
    }

    return traversalOrder[currentTraversalIndex];
  }, [currentTraversalIndex, traversalOrder]);

  const traversalProgress = useMemo(() => {
    if (traversalOrder.length === 0 || currentTraversalIndex < 0) {
      return 0;
    }

    return Math.round(((currentTraversalIndex + 1) / traversalOrder.length) * 100);
  }, [currentTraversalIndex, traversalOrder.length]);

  const applyTreePayload = useCallback(
    (payload, visualState = {}) => {
      const normalizedTraversalOrder = (visualState.traversalOrder || []).map((value) => String(value));
      const normalizedHighlight = visualState.highlightedId ? String(visualState.highlightedId) : "";
      const normalizedPivot = visualState.pivotId ? String(visualState.pivotId) : "";
      const result = payload.result || payload;
      const before = result.before || null;
      const rotations = result.rotationEvents || [];
      const latestRotation = result.lastRotation || rotations[rotations.length - 1] || null;

      setNodes(
        normalizeAVLNodes(payload.nodes || result.nodes || [], {
          highlightedId: normalizedHighlight,
          pivotId: normalizedPivot,
          traversalOrder: normalizedTraversalOrder,
        }),
      );
      setEdges(normalizeAVLEdges(payload.edges || result.edges || [], normalizedTraversalOrder));
      setBeforeNodes(
        normalizeAVLNodes(before?.nodes || [], {
          highlightedId: normalizedHighlight,
          pivotId: normalizedPivot,
          traversalOrder: [],
        }),
      );
      setBeforeEdges(normalizeAVLEdges(before?.edges || [], []));
      setMetrics(payload.metrics || result.metrics || null);
      setTree(result.tree || payload.tree || null);
      setRotationEvents(rotations);
      setLastRotation(latestRotation);
      setActiveView(before?.nodes?.length ? "compare" : "after");
    },
    [setEdges, setNodes],
  );

  const refreshTree = useCallback(
    async (visualState = {}) => {
      const response = await getAVLState();
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
        const payload = await refreshTree({ highlightedId: "", pivotId: "", traversalOrder: [] });

        if ((payload.nodes || []).length === 0) {
          const demoResponse = await loadAVLDemo();
          const demoPayload = getPayload(demoResponse);
          applyTreePayload(demoPayload, { highlightedId: "", pivotId: "", traversalOrder: [] });
          setStatus({
            type: "success",
            message: "Dataset demo cargado para el árbol AVL.",
          });
          return;
        }

        setStatus({
          type: "success",
          message: "Estado del árbol AVL obtenido correctamente.",
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
      normalizeAVLNodes(currentNodes, {
        highlightedId: currentTraversalNodeId || highlightedId,
        pivotId,
        traversalOrder: activeTraversalOrder,
      }),
    );
    setEdges((currentEdges) => normalizeAVLEdges(currentEdges, activeTraversalOrder));
  }, [activeTraversalOrder, currentTraversalNodeId, highlightedId, pivotId, setEdges, setNodes]);

  useEffect(() => {
    if (!isAnimatingTraversal || traversalOrder.length === 0) {
      return undefined;
    }

    const timerId = window.setTimeout(() => {
      setCurrentTraversalIndex((currentIndex) => {
        const nextIndex = currentIndex + 1;

        if (nextIndex >= traversalOrder.length) {
          setIsAnimatingTraversal(false);
          setStatus({
            type: "success",
            message: `Animación ${traversal?.type || traversalType} finalizada correctamente.`,
          });
          return currentIndex;
        }

        const nextOrder = traversalOrder.slice(0, nextIndex + 1);
        setActiveTraversalOrder(nextOrder);

        if (nextIndex === traversalOrder.length - 1) {
          setIsAnimatingTraversal(false);
          setStatus({
            type: "success",
            message: `Animación ${traversal?.type || traversalType} finalizada correctamente.`,
          });
        }

        return nextIndex;
      });
    }, animationSpeed);

    return () => window.clearTimeout(timerId);
  }, [animationSpeed, isAnimatingTraversal, traversal, traversalOrder, traversalType]);

  const metricsCards = useMemo(
    () => [
      { label: "Nodos", value: metrics?.count ?? 0 },
      { label: "Altura", value: metrics?.height ?? 0 },
      { label: "Niveles", value: metrics?.levels ?? 0 },
      { label: "Balance raíz", value: metrics?.balanceFactor ?? 0 },
      { label: "Rotaciones", value: metrics?.rotationCount ?? rotationEvents.length },
      { label: "Balanceado", value: metrics?.isBalanced ? "Sí" : "No" },
    ],
    [metrics, rotationEvents.length],
  );

  const hasNodes = nodes.length > 0;
  const hasBeforeSnapshot = beforeNodes.length > 0;

  const rootLabel = useMemo(() => {
    if (!tree?.root) {
      return "Sin raíz";
    }

    return tree.root.label || String(tree.root.value);
  }, [tree]);

  const visibleFlow = useMemo(() => {
    if (activeView === "before") {
      return { title: "Antes de la operación", nodes: beforeNodes, edges: beforeEdges };
    }

    return { title: "Después de la operación", nodes, edges };
  }, [activeView, beforeEdges, beforeNodes, edges, nodes]);

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
    setPivotId("");
    setTraversal(null);
    setActiveTraversalOrder([]);
    setCurrentTraversalIndex(-1);
    setIsAnimatingTraversal(false);
  };

  const resetTraversalAnimation = () => {
    setActiveTraversalOrder([]);
    setCurrentTraversalIndex(-1);
    setIsAnimatingTraversal(false);
    setHighlightedId("");
  };

  const applyOperationVisuals = (payload, value, successMessage) => {
    const result = payload.result || {};
    const latestRotation = result.lastRotation || null;
    const nextPivotId = latestRotation?.pivot ? String(latestRotation.pivot) : "";
    const nextHighlight = value !== undefined && value !== null ? String(value) : "";
    const rotationMessage = latestRotation
      ? ` Rotación ${latestRotation.type} aplicada sobre pivote ${latestRotation.pivot}.`
      : " No fue necesaria rotación.";

    setHighlightedId(nextHighlight);
    setPivotId(nextPivotId);
    setTraversal(null);
    setActiveTraversalOrder([]);
    setCurrentTraversalIndex(-1);
    setIsAnimatingTraversal(false);
    applyTreePayload(payload, {
      highlightedId: nextHighlight,
      pivotId: nextPivotId,
      traversalOrder: [],
    });
    setStatus({
      type: "success",
      message: `${successMessage}${rotationMessage}`,
    });
  };

  const handleLoadDemo = () =>
    runAction(async () => {
      const response = await loadAVLDemo();
      const payload = getPayload(response);
      const result = payload.result || {};
      const latestRotation = result.lastRotation || null;

      clearVisualMarks();
      applyTreePayload(payload, {
        highlightedId: "",
        pivotId: latestRotation?.pivot ? String(latestRotation.pivot) : "",
        traversalOrder: [],
      });
      setPivotId(latestRotation?.pivot ? String(latestRotation.pivot) : "");
      setStatus({
        type: "success",
        message: `Dataset demo AVL cargado. Rotaciones registradas: ${(result.rotationEvents || []).length}.`,
      });
    });

  const handleReset = () =>
    runAction(async () => {
      const response = await resetAVLTree();
      const payload = getPayload(response);

      clearVisualMarks();
      applyTreePayload(payload, { highlightedId: "", pivotId: "", traversalOrder: [] });
      setInsertValue("");
      setDeleteValue("");
      setSearchValue("");
      setStatus({
        type: "success",
        message: "Árbol AVL reiniciado correctamente.",
      });
    });

  const handleInsert = (event) => {
    event.preventDefault();

    runAction(async () => {
      const value = coerceInputValue(insertValue);

      if (value === "") {
        setStatus({
          type: "error",
          message: "El valor a insertar es obligatorio.",
        });
        return;
      }

      const response = await insertAVLValue(value);
      const payload = getPayload(response);

      applyOperationVisuals(payload, value, `Valor ${String(value)} insertado correctamente.`);
      setInsertValue("");
    });
  };

  const handleDelete = (event) => {
    event.preventDefault();

    runAction(async () => {
      const value = coerceInputValue(deleteValue);

      if (value === "") {
        setStatus({
          type: "error",
          message: "Indica el valor que deseas eliminar.",
        });
        return;
      }

      const response = await deleteAVLValue(value);
      const payload = getPayload(response);

      applyOperationVisuals(payload, null, `Valor ${String(value)} eliminado correctamente.`);
      setDeleteValue("");
    });
  };

  const handleSearch = (event) => {
    event.preventDefault();

    runAction(async () => {
      const value = coerceInputValue(searchValue);

      if (value === "") {
        setStatus({
          type: "error",
          message: "Indica el valor que deseas buscar.",
        });
        return;
      }

      const response = await searchAVLValue(value);
      const payload = getPayload(response);
      const result = payload.result || {};
      const nextHighlight = result.found ? String(value) : "";

      setHighlightedId(nextHighlight);
      setPivotId("");
      setTraversal(null);
      setActiveTraversalOrder([]);
      setCurrentTraversalIndex(-1);
      setIsAnimatingTraversal(false);
      applyTreePayload(payload, { highlightedId: nextHighlight, pivotId: "", traversalOrder: [] });
      setStatus({
        type: result.found ? "success" : "error",
        message: result.found
          ? `Valor ${String(value)} encontrado en nivel ${result.level}.`
          : `El valor ${String(value)} no existe en el árbol AVL.`,
      });
    });
  };

  const handleTraversal = () =>
    runAction(async () => {
      const response = await traverseAVLTree(traversalType);
      const payload = getPayload(response);
      const nextTraversal = payload.traversal || payload.result?.traversal || null;

      setTraversal(nextTraversal);
      setHighlightedId("");
      setPivotId("");
      setActiveTraversalOrder([]);
      setCurrentTraversalIndex(-1);
      setIsAnimatingTraversal(Boolean(nextTraversal?.order?.length));
      applyTreePayload(payload, { highlightedId: "", pivotId: "", traversalOrder: [] });
      setStatus({
        type: "success",
        message: `Recorrido ${traversalType} listo. Iniciando animación paso a paso.`,
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
            <p className="text-sm font-semibold uppercase tracking-widest text-teal-400">
              Épica 7
            </p>
            <h2 className="mt-2 text-2xl font-bold text-white">
              Árbol AVL balanceado con rotaciones visibles
            </h2>
            <p className="mt-2 max-w-3xl text-gray-300">
              Inserta, elimina y busca IDs académicos en un árbol AVL. Cada operación
              actualiza altura, factor de balance y registra rotaciones LL, RR, LR o RL.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={handleLoadDemo}
              disabled={isLoading}
              className="rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white transition hover:bg-teal-500 disabled:cursor-not-allowed disabled:opacity-60"
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
              <h3 className="text-lg font-semibold text-white">Insertar ID</h3>
              <p className="mt-2 text-sm text-gray-400">
                El AVL mantiene búsqueda O(log n) mediante balanceo automático.
              </p>

              <form className="mt-4 space-y-3" onSubmit={handleInsert}>
                <input
                  value={insertValue}
                  onChange={(event) => setInsertValue(event.target.value)}
                  placeholder="ID, ej. 35"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-teal-500"
                />

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white transition hover:bg-teal-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Insertar
                </button>
              </form>
            </article>

            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Eliminar ID</h3>
              <p className="mt-2 text-sm text-gray-400">
                Después de eliminar, el árbol recalcula alturas y rebalancea si hace falta.
              </p>

              <form className="mt-4 space-y-3" onSubmit={handleDelete}>
                <input
                  value={deleteValue}
                  onChange={(event) => setDeleteValue(event.target.value)}
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
              <h3 className="text-lg font-semibold text-white">Buscar ID</h3>
              <p className="mt-2 text-sm text-gray-400">
                Si el ID existe, se resalta el nodo. En AVL el camino se mantiene corto.
              </p>

              <form className="mt-4 space-y-3" onSubmit={handleSearch}>
                <input
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
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
              <h3 className="text-lg font-semibold text-white">Recorridos animados</h3>
              <p className="mt-2 text-sm text-gray-400">
                Inorder confirma orden ascendente; levelorder expone niveles y balance.
              </p>

              <div className="mt-4 grid gap-3 sm:grid-cols-[1fr_auto]">
                <select
                  value={traversalType}
                  onChange={(event) => setTraversalType(event.target.value)}
                  disabled={isAnimatingTraversal}
                  className="min-w-0 rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-teal-500 disabled:cursor-not-allowed disabled:opacity-60"
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
                  disabled={isLoading || !hasNodes || isAnimatingTraversal}
                  className="rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white transition hover:bg-teal-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Ejecutar
                </button>
              </div>

              <div className="mt-3 grid gap-3 sm:grid-cols-2">
                <select
                  value={animationSpeed}
                  onChange={(event) => setAnimationSpeed(Number(event.target.value))}
                  className="rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-teal-500"
                >
                  {animationSpeedOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      Velocidad {option.label}
                    </option>
                  ))}
                </select>

                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setIsAnimatingTraversal((current) => !current)}
                    disabled={!traversal || traversalProgress >= 100}
                    className="rounded-xl border border-teal-700 px-4 py-2 text-sm font-semibold text-teal-200 transition hover:bg-teal-950 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isAnimatingTraversal ? "Pausar" : "Continuar"}
                  </button>

                  <button
                    type="button"
                    onClick={resetTraversalAnimation}
                    disabled={!traversal}
                    className="rounded-xl border border-gray-600 px-4 py-2 text-sm font-semibold text-gray-200 transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Reiniciar
                  </button>
                </div>
              </div>

              {traversal && (
                <div className="mt-4 rounded-xl border border-teal-800 bg-teal-950/40 p-3">
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-semibold text-teal-200">
                      {traversal.type} desde {traversal.start ?? "N/A"}
                    </p>
                    <span className="rounded-full bg-teal-700 px-3 py-1 text-xs font-bold text-white">
                      {traversalProgress}%
                    </span>
                  </div>

                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-gray-900">
                    <div
                      className="h-full rounded-full bg-teal-500 transition-all duration-300"
                      style={{ width: `${traversalProgress}%` }}
                    />
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {traversal.steps.map((step, index) => {
                      const wasVisited = index <= currentTraversalIndex;
                      const isCurrent = index === currentTraversalIndex;

                      return (
                        <span
                          key={`${step.step}-${step.id}`}
                          className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                            isCurrent
                              ? "bg-yellow-500 text-gray-950"
                              : wasVisited
                                ? "bg-teal-700 text-white"
                                : "bg-gray-900 text-gray-400"
                          }`}
                        >
                          {step.step}. {step.label} · BF {step.balanceFactor}
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}
            </article>

            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <h3 className="text-lg font-semibold text-white">Rotaciones registradas</h3>
              <p className="mt-2 text-sm text-gray-400">
                Cada evento expone tipo, pivote y snapshots antes/después para explicar el rebalanceo.
              </p>

              <div className="mt-4 space-y-3">
                {rotationEvents.length > 0 ? (
                  rotationEvents.map((event, index) => (
                    <div
                      key={`${event.type}-${event.pivot}-${index}`}
                      className="rounded-xl border border-orange-800 bg-orange-950/30 p-3"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span className="rounded-full bg-orange-600 px-3 py-1 text-xs font-bold text-white">
                          {event.type}
                        </span>
                        <span className="text-xs font-semibold text-orange-200">
                          pivote {String(event.pivot)}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="rounded-xl border border-gray-700 bg-gray-900 p-3 text-sm text-gray-400">
                    Aún no hay rotaciones en la última operación.
                  </p>
                )}
              </div>
            </article>
          </aside>

          <section className="space-y-6">
            <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-white">
                    Visualización React Flow AVL
                  </h3>
                  <p className="mt-1 text-sm text-gray-400">
                    Raíz actual: <span className="font-semibold text-teal-300">{rootLabel}</span>
                    {lastRotation && (
                      <span className="ml-2 text-orange-300">
                        Última rotación: {lastRotation.type} sobre {String(lastRotation.pivot)}
                      </span>
                    )}
                  </p>
                </div>

                <div className="flex flex-wrap gap-3">
                  {hasBeforeSnapshot && (
                    <>
                      <button
                        type="button"
                        onClick={() => setActiveView("before")}
                        className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                          activeView === "before"
                            ? "bg-orange-600 text-white"
                            : "border border-orange-700 text-orange-200 hover:bg-orange-950"
                        }`}
                      >
                        Antes
                      </button>
                      <button
                        type="button"
                        onClick={() => setActiveView("after")}
                        className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                          activeView === "after"
                            ? "bg-teal-600 text-white"
                            : "border border-teal-700 text-teal-200 hover:bg-teal-950"
                        }`}
                      >
                        Después
                      </button>
                    </>
                  )}

                  <button
                    type="button"
                    onClick={() => refreshTree({ highlightedId: currentTraversalNodeId || highlightedId, pivotId, traversalOrder: activeTraversalOrder })}
                    disabled={isLoading}
                    className="rounded-xl border border-gray-600 px-4 py-2 text-sm font-semibold text-gray-200 transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Refrescar
                  </button>

                  <button
                    type="button"
                    onClick={clearVisualMarks}
                    disabled={isLoading}
                    className="rounded-xl border border-cyan-700 px-4 py-2 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-950 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Limpiar marcas
                  </button>
                </div>
              </div>

              <p className="mt-3 text-sm font-semibold text-gray-300">
                Vista activa: {visibleFlow.title}
              </p>

              <div className="mt-4 h-[620px] overflow-hidden rounded-2xl border border-gray-700 bg-gray-950">
                {visibleFlow.nodes.length > 0 ? (
                  <ReactFlow
                    nodes={visibleFlow.nodes}
                    edges={visibleFlow.edges}
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
                        El árbol AVL está vacío.
                      </p>
                      <p className="mt-2 max-w-md text-gray-400">
                        Inserta una raíz o carga el dataset demo para iniciar la visualización.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </article>

            <div className="grid gap-6 xl:grid-cols-2">
              <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
                <h3 className="text-lg font-semibold text-white">Estado estructural AVL</h3>
                <p className="mt-2 text-sm text-gray-400">
                  JSON del árbol para validar raíz, alturas, factores de balance e hijos.
                </p>

                <pre className="mt-4 max-h-96 overflow-auto rounded-xl border border-gray-700 bg-gray-950 p-4 text-xs text-gray-200">
                  {JSON.stringify(tree || { root: null, size: 0 }, null, 2)}
                </pre>
              </article>

              <article className="rounded-2xl border border-gray-700 bg-gray-800 p-5 shadow-lg">
                <h3 className="text-lg font-semibold text-white">Última rotación</h3>
                <p className="mt-2 text-sm text-gray-400">
                  Snapshot técnico para explicar qué subárbol fue transformado.
                </p>

                <pre className="mt-4 max-h-96 overflow-auto rounded-xl border border-gray-700 bg-gray-950 p-4 text-xs text-gray-200">
                  {JSON.stringify(lastRotation || { type: null, pivot: null }, null, 2)}
                </pre>
              </article>
            </div>
          </section>
        </div>
      </section>
    </MainLayout>
  );
};

export default AVLPage;
