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

const normalizeNodes = (nodes = [], highlightedId = "") => {
  return nodes.map((node) => {
    const category = node?.data?.category || "academic";
    const isHighlighted = highlightedId && String(node.id) === String(highlightedId);

    return {
      ...node,
      draggable: false,
      data: {
        ...node.data,
        label: (
          <div className="min-w-36">
            <p className="text-sm font-semibold text-white">
              {node?.data?.label}
            </p>
            <p className="mt-1 text-xs uppercase tracking-wide text-cyan-200">
              {category}
            </p>
          </div>
        ),
      },
      style: {
        border: isHighlighted ? "2px solid #facc15" : "1px solid #0891b2",
        borderRadius: "14px",
        background: isHighlighted ? "#713f12" : "#111827",
        color: "#e5e7eb",
        padding: "10px",
        boxShadow: isHighlighted
          ? "0 12px 30px rgba(250, 204, 21, 0.20)"
          : "0 10px 25px rgba(8, 145, 178, 0.16)",
      },
    };
  });
};

const getResponseData = (response) => response?.data || {};

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

  const refreshTree = useCallback(
    async (highlightId = highlightedId) => {
      const response = await getGeneralTreeState();
      const payload = getResponseData(response);
      setNodes(normalizeNodes(payload.nodes, highlightId));
      setEdges(payload.edges || []);
      setMetrics(payload.metrics || null);
      setTree(payload.result?.tree || payload.result || null);
      return payload;
    },
    [highlightedId, setEdges, setNodes],
  );

  useEffect(() => {
    const loadInitialState = async () => {
      try {
        const payload = await refreshTree("");
        if ((payload.nodes || []).length === 0) {
          const demoResponse = await loadGeneralTreeDemo();
          const demoPayload = getResponseData(demoResponse);
          setNodes(normalizeNodes(demoPayload.nodes, ""));
          setEdges(demoPayload.edges || []);
          setMetrics(demoPayload.metrics || null);
          setTree(demoPayload.result?.tree || demoPayload.result || null);
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
          message:
            error?.response?.data?.message ||
            "No se pudo cargar el árbol general desde el backend.",
        });
      }
    };

    loadInitialState();
  }, [refreshTree, setEdges, setNodes]);

  useEffect(() => {
    setNodes((currentNodes) => normalizeNodes(currentNodes, highlightedId));
  }, [highlightedId, setNodes]);

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
        message:
          error?.response?.data?.message ||
          error?.message ||
          "No se pudo completar la operación.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadDemo = () =>
    runAction(async () => {
      const response = await loadGeneralTreeDemo();
      const payload = getResponseData(response);
      setHighlightedId("");
      setNodes(normalizeNodes(payload.nodes, ""));
      setEdges(payload.edges || []);
      setMetrics(payload.metrics || null);
      setTree(payload.result?.tree || payload.result || null);
      setTraversal(null);
      setStatus({
        type: "success",
        message: "Dataset demo cargado correctamente.",
      });
    });

  const handleReset = () =>
    runAction(async () => {
      const response = await resetGeneralTree();
      const payload = getResponseData(response);
      setHighlightedId("");
      setNodes([]);
      setEdges([]);
      setMetrics(payload.metrics || null);
      setTree(null);
      setTraversal(null);
      setStatus({
        type: "success",
        message: "Árbol general reiniciado correctamente.",
      });
    });

  const handleInsert = (event) => {
    event.preventDefault();

    runAction(async () => {
      const metadata = form.metadataCode
        ? { code: form.metadataCode }
        : {};

      const response = await insertGeneralTreeNode({
        id: form.id,
        label: form.label,
        parentId: form.parentId || null,
        category: form.category,
        metadata,
      });
      const payload = getResponseData(response);

      setHighlightedId(form.id);
      setNodes(normalizeNodes(payload.nodes, form.id));
      setEdges(payload.edges || []);
      setMetrics(payload.metrics || null);
      setTree(payload.result?.tree || payload.result || null);
      setForm(initialForm);
      setTraversal(null);
      setStatus({
        type: "success",
        message: "Nodo insertado correctamente.",
      });
    });
  };

  const handleDelete = (event) => {
    event.preventDefault();

    runAction(async () => {
      const response = await deleteGeneralTreeNode(deleteId);
      const payload = getResponseData(response);

      setHighlightedId("");
      setNodes(normalizeNodes(payload.nodes, ""));
      setEdges(payload.edges || []);
      setMetrics(payload.metrics || null);
      setTree(payload.result?.tree || payload.result || null);
      setDeleteId("");
      setTraversal(null);
      setStatus({
        type: "success",
        message: "Nodo eliminado correctamente.",
      });
    });
  };

  const handleSearch = (event) => {
    event.preventDefault();

    runAction(async () => {
      const response = await searchGeneralTreeNode(searchId);
      const payload = getResponseData(response);
      const result = payload.result || {};

      setHighlightedId(result.found ? searchId : "");
      await refreshTree(result.found ? searchId : "");
      setStatus({
        type: result.found ? "success" : "error",
        message: result.found
          ? `Nodo encontrado en nivel ${result.level}.`
          : "El nodo no existe en el árbol.",
      });
    });
  };

  const handleTraversal = () =>
    runAction(async () => {
      const response = await traverseGeneralTree(traversalType);
      const payload = getResponseData(response);
      setTraversal(payload.traversal || payload.result?.traversal || null);
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
              Visualiza una jerarquía Facultad → Carrera → Ciclos → Cursos,
              usando React Flow y operaciones servidas por Flask.
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
              className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              Reiniciar
            </button>
          </div>
        </div>

        <div className={`rounded-xl border p-4 ${statusClass}`}>
          {status.message}
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
          {metricsCards.map((item) => (
            <article
              key={item.label}
              className="rounded-2xl border border-gray-700 bg-gray-800 p-4"
            >
              <p className="text-sm text-gray-400">{item.label}</p>
              <p className="mt-2 text-2xl font-bold text-white">{item.value}</p>
            </article>
          ))}
        </div>

        <div className="grid gap-6 xl:grid-cols-[380px_1fr]">
          <aside className="space-y-6">
            <form
              onSubmit={handleInsert}
              className="rounded-2xl border border-gray-700 bg-gray-800 p-5"
            >
              <h3 className="text-lg font-semibold text-white">
                Insertar nodo
              </h3>

              <div className="mt-4 space-y-3">
                <input
                  name="id"
                  value={form.id}
                  onChange={handleFormChange}
                  placeholder="ID único, ej. curso-progra-i"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <input
                  name="label"
                  value={form.label}
                  onChange={handleFormChange}
                  placeholder="Etiqueta, ej. Programación I"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <input
                  name="parentId"
                  value={form.parentId}
                  onChange={handleFormChange}
                  placeholder="ID padre, vacío solo si el árbol está vacío"
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
                  placeholder="Código opcional, ej. SIS-101"
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Insertar
                </button>
              </div>
            </form>

            <form
              onSubmit={handleDelete}
              className="rounded-2xl border border-gray-700 bg-gray-800 p-5"
            >
              <h3 className="text-lg font-semibold text-white">
                Eliminar nodo
              </h3>

              <div className="mt-4 flex gap-3">
                <input
                  value={deleteId}
                  onChange={(event) => setDeleteId(event.target.value)}
                  placeholder="ID del nodo"
                  className="min-w-0 flex-1 rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="rounded-xl bg-red-600 px-4 py-2 font-semibold text-white transition hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Eliminar
                </button>
              </div>
            </form>

            <form
              onSubmit={handleSearch}
              className="rounded-2xl border border-gray-700 bg-gray-800 p-5"
            >
              <h3 className="text-lg font-semibold text-white">
                Buscar nodo
              </h3>

              <div className="mt-4 flex gap-3">
                <input
                  value={searchId}
                  onChange={(event) => setSearchId(event.target.value)}
                  placeholder="ID del nodo"
                  className="min-w-0 flex-1 rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="rounded-xl bg-yellow-600 px-4 py-2 font-semibold text-white transition hover:bg-yellow-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Buscar
                </button>
              </div>
            </form>

            <div className="rounded-2xl border border-gray-700 bg-gray-800 p-5">
              <h3 className="text-lg font-semibold text-white">
                Recorridos
              </h3>

              <div className="mt-4 flex gap-3">
                <select
                  value={traversalType}
                  onChange={(event) => setTraversalType(event.target.value)}
                  className="min-w-0 flex-1 rounded-xl border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 outline-none focus:border-cyan-500"
                >
                  <option value="levelorder">Levelorder</option>
                  <option value="preorder">Preorder</option>
                  <option value="postorder">Postorder</option>
                </select>
                <button
                  type="button"
                  onClick={handleTraversal}
                  disabled={isLoading}
                  className="rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Ver
                </button>
              </div>

              {traversal?.order?.length > 0 && (
                <div className="mt-4 rounded-xl border border-gray-700 bg-gray-900 p-4">
                  <p className="text-sm text-gray-400">
                    Orden ({traversal.type})
                  </p>
                  <p className="mt-2 break-words text-sm text-cyan-200">
                    {traversal.order.join(" → ")}
                  </p>
                </div>
              )}
            </div>
          </aside>

          <div className="min-h-[720px] rounded-2xl border border-gray-700 bg-gray-950">
            {nodes.length > 0 ? (
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                fitView
              >
                <Background />
                <Controls />
                <MiniMap pannable zoomable />
              </ReactFlow>
            ) : (
              <div className="flex h-full min-h-[720px] items-center justify-center p-8 text-center text-gray-400">
                No hay nodos en el árbol. Carga el demo o inserta una raíz.
              </div>
            )}
          </div>
        </div>

        {tree && (
          <details className="rounded-2xl border border-gray-700 bg-gray-800 p-5">
            <summary className="cursor-pointer font-semibold text-white">
              Ver estructura JSON del árbol
            </summary>
            <pre className="mt-4 max-h-96 overflow-auto rounded-xl bg-gray-950 p-4 text-xs text-gray-300">
              {JSON.stringify(tree, null, 2)}
            </pre>
          </details>
        )}
      </section>
    </MainLayout>
  );
};

export default GeneralTreePage;
