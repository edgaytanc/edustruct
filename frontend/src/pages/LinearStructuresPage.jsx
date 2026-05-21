import { useCallback, useEffect, useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MarkerType, MiniMap, useEdgesState, useNodesState } from "reactflow";
import "reactflow/dist/style.css";

import {
    backStackNavigation,
    deleteListItem,
    dequeueAdvisoryTurn,
    enqueueQueueItem,
    getAdvisoryTurns,
    getListCourses,
    getQueueFront,
    insertListItem,
    loadAdvisoryQueue,
    loadListCourse,
    loadStackHistory,
    peekStack,
    popStackItem,
    pushStackItem,
    pushStackNavigation,
    resetList,
    resetQueue,
    resetStack,
    searchListItem,
    searchQueueItem,
    searchStackItem,
    traverseList,
    traverseQueue,
    traverseStack,
} from "../api/linearStructures";
import MainLayout from "../components/layout/MainLayout";

const tabs = [
    { id: "list", label: "Lista de inscritos" },
    { id: "queue", label: "Cola de asesoría" },
    { id: "stack", label: "Pila de historial" },
];

const getPayload = (response) => response?.data || {};
const getResult = (payload) => payload?.result || {};

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

const getMetricValue = (payload, result, key, fallback = "—") => {
    const value = payload?.metrics?.[key] ?? result?.[key];
    return value === null || value === undefined || value === "" ? fallback : value;
};

const getItems = (payload) => {
    const result = getResult(payload);
    const traversalOrder = payload?.traversal?.order || result?.traversal?.order;
    return result?.items || traversalOrder || [];
};

const getNodes = (payload) => payload?.nodes || getResult(payload)?.nodes || [];
const getEdges = (payload) => payload?.edges || getResult(payload)?.edges || [];

const createNodeLabel = (node, activeValues = new Set()) => {
    const metadata = node?.data?.metadata || {};
    const value = String(metadata?.value || node?.data?.label || "Nodo");
    const role = metadata?.role || node?.data?.category || "item";
    const isMarker = role.includes("marker");
    const isActive = activeValues.has(value) || activeValues.has(String(node.id));

    return (
        <div className="min-w-[170px] text-center">
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-cyan-200">{isMarker ? node?.data?.label : role}</p>
            {!isMarker && <p className="mt-2 text-sm font-semibold leading-tight text-white">{value}</p>}
            {isActive && <p className="mt-2 rounded-lg border border-lime-300 bg-lime-500/20 px-2 py-1 text-[10px] font-bold text-lime-100">Recorrido</p>}
        </div>
    );
};

const normalizeNodes = (nodes = [], activeValues = new Set()) =>
    nodes.map((node) => {
        const category = node?.data?.category;
        const metadata = node?.data?.metadata || {};
        const value = String(metadata?.value || node?.data?.label || node.id);
        const isActive = activeValues.has(value) || activeValues.has(String(node.id));
        const isMarker = metadata?.role?.includes("marker");
        const borderColor = isActive ? "#84cc16" : category?.includes("head") || category?.includes("front") || category?.includes("top") ? "#22d3ee" : category?.includes("tail") || category?.includes("rear") ? "#a78bfa" : "#64748b";

        return {
            ...node,
            draggable: false,
            data: { ...node.data, label: createNodeLabel(node, activeValues) },
            style: {
                border: `2px solid ${borderColor}`,
                borderRadius: 18,
                background: isMarker ? "#0f172a" : isActive ? "#1a2e05" : "#111827",
                color: "#f8fafc",
                padding: 10,
                width: 220,
                boxShadow: isActive ? `0 0 0 4px ${borderColor}33` : "none",
            },
        };
    });

const normalizeEdges = (edges = []) =>
    edges.map((edge) => ({
        ...edge,
        markerEnd: { type: MarkerType.ArrowClosed, color: "#64748b" },
        style: { stroke: "#64748b", strokeWidth: 2 },
        labelStyle: { fill: "#cbd5e1", fontWeight: 700 },
    }));

const FlowPanel = ({ payload, emptyMessage, activeValues }) => {
    const visualNodes = useMemo(() => normalizeNodes(getNodes(payload), activeValues), [payload, activeValues]);
    const visualEdges = useMemo(() => normalizeEdges(getEdges(payload)), [payload]);
    const [nodes, setNodes, onNodesChange] = useNodesState(visualNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(visualEdges);

    useEffect(() => setNodes(visualNodes), [setNodes, visualNodes]);
    useEffect(() => setEdges(visualEdges), [setEdges, visualEdges]);

    if (visualNodes.length === 0) {
        return <div className="flex h-[420px] items-center justify-center rounded-2xl border border-dashed border-gray-700 bg-gray-950 text-gray-400">{emptyMessage}</div>;
    }

    return (
        <div className="h-[480px] overflow-hidden rounded-2xl border border-gray-700 bg-gray-950">
            <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} fitView fitViewOptions={{ padding: 0.25 }} nodesDraggable={false}>
                <MiniMap pannable zoomable />
                <Controls />
                <Background gap={24} size={1} />
            </ReactFlow>
        </div>
    );
};

const MetricCard = ({ label, value }) => (
    <article className="rounded-xl border border-gray-700 bg-gray-900 p-4">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-gray-400">{label}</p>
        <p className="mt-2 break-words text-lg font-semibold text-white">{value}</p>
    </article>
);

const ItemsList = ({ title, items, emptyText }) => (
    <section className="rounded-2xl border border-gray-700 bg-gray-800 p-5">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        {items.length === 0 ? (
            <p className="mt-3 text-gray-400">{emptyText}</p>
        ) : (
            <ol className="mt-4 max-h-72 space-y-2 overflow-auto pr-2 text-sm text-gray-200">
                {items.map((item, index) => (
                    <li key={`${item}-${index}`} className="rounded-xl border border-gray-700 bg-gray-900 px-3 py-2">
                        <span className="mr-2 font-mono text-cyan-300">#{index + 1}</span>{item}
                    </li>
                ))}
            </ol>
        )}
    </section>
);

const LinearStructuresPage = () => {
    const [activeTab, setActiveTab] = useState("list");
    const [courses, setCourses] = useState([]);
    const [selectedCourseId, setSelectedCourseId] = useState("");
    const [listPayload, setListPayload] = useState(null);
    const [queuePayload, setQueuePayload] = useState(null);
    const [stackPayload, setStackPayload] = useState(null);
    const [advisorySummary, setAdvisorySummary] = useState(null);
    const [navigationModule, setNavigationModule] = useState("Curso CUR-013");
    const [manualListValue, setManualListValue] = useState("Estudiante manual 2026001 - Ana López");
    const [manualListPosition, setManualListPosition] = useState("tail");
    const [manualListSearch, setManualListSearch] = useState("");
    const [manualQueueValue, setManualQueueValue] = useState("Turno manual - Asesoría de pensum");
    const [manualQueueSearch, setManualQueueSearch] = useState("");
    const [manualStackValue, setManualStackValue] = useState("Módulo manual - Consulta de notas");
    const [manualStackSearch, setManualStackSearch] = useState("");
    const [activeValues, setActiveValues] = useState(new Set());
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const runAction = useCallback(async (action, onSuccess) => {
        setLoading(true);
        setError("");
        setMessage("");
        setActiveValues(new Set());

        try {
            const response = await action();
            onSuccess(response);
            setMessage(response?.message || "Operación ejecutada correctamente.");
        } catch (err) {
            setError(getApiErrorMessage(err));
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        runAction(async () => {
            const [coursesResponse, turnsResponse] = await Promise.all([getListCourses(), getAdvisoryTurns()]);
            return { coursesResponse, turnsResponse };
        }, ({ coursesResponse, turnsResponse }) => {
            const courseList = getResult(getPayload(coursesResponse))?.courses || getPayload(coursesResponse)?.result?.courses || [];
            setCourses(courseList);
            setSelectedCourseId(courseList[0]?.courseId || "");
            setAdvisorySummary(getResult(getPayload(turnsResponse)) || getPayload(turnsResponse)?.result || null);
            setMessage("Catálogos académicos cargados correctamente.");
        });
    }, [runAction]);

    const currentPayload = activeTab === "list" ? listPayload : activeTab === "queue" ? queuePayload : stackPayload;
    const currentResult = getResult(currentPayload || {});
    const currentItems = getItems(currentPayload || {});

    const loadSelectedCourse = () => {
        if (!selectedCourseId) {
            setError("Selecciona un curso antes de cargar la lista.");
            return;
        }

        runAction(() => loadListCourse(selectedCourseId), (response) => setListPayload(getPayload(response)));
    };

    const loadQueue = () => runAction(loadAdvisoryQueue, (response) => setQueuePayload(getPayload(response)));
    const loadHistory = () => runAction(loadStackHistory, (response) => setStackPayload(getPayload(response)));

    const showTraversal = () => {
        const action = activeTab === "list" ? traverseList : activeTab === "queue" ? traverseQueue : traverseStack;
        runAction(action, (response) => {
            const payload = getPayload(response);
            const order = payload?.traversal?.order || getResult(payload)?.traversal?.order || [];
            setActiveValues(new Set(order.map(String)));
            if (activeTab === "list") setListPayload(payload);
            if (activeTab === "queue") setQueuePayload(payload);
            if (activeTab === "stack") setStackPayload(payload);
        });
    };

    const showQueueFront = () => runAction(getQueueFront, (response) => {
        const payload = getPayload(response);
        setQueuePayload(payload);
        const front = getResult(payload)?.front;
        setActiveValues(new Set(front ? [String(front)] : []));
    });

    const validateManualValue = (value, label) => {
        if (!value.trim()) {
            setError(`Ingresa un valor para ${label}.`);
            return null;
        }

        return value.trim();
    };

    const createEmptyList = () => runAction(resetList, (response) => setListPayload(getPayload(response)));

    const addManualListNode = () => {
        const value = validateManualValue(manualListValue, "la lista");
        if (!value) return;

        runAction(() => insertListItem(value, manualListPosition), (response) => {
            setListPayload(getPayload(response));
            setActiveValues(new Set([value]));
        });
    };

    const removeManualListNode = () => {
        const value = validateManualValue(manualListSearch || manualListValue, "el nodo que deseas eliminar");
        if (!value) return;

        runAction(() => deleteListItem(value), (response) => setListPayload(getPayload(response)));
    };

    const findManualListNode = () => {
        const value = validateManualValue(manualListSearch, "la búsqueda en lista");
        if (!value) return;

        runAction(() => searchListItem(value), (response) => {
            const payload = getPayload(response);
            setListPayload(payload);
            const result = getResult(payload);
            setActiveValues(new Set(result?.found ? [String(result.query)] : []));
        });
    };

    const createEmptyQueue = () => runAction(resetQueue, (response) => setQueuePayload(getPayload(response)));

    const addManualQueueNode = () => {
        const value = validateManualValue(manualQueueValue, "la cola");
        if (!value) return;

        runAction(() => enqueueQueueItem(value), (response) => {
            setQueuePayload(getPayload(response));
            setActiveValues(new Set([value]));
        });
    };

    const findManualQueueNode = () => {
        const value = validateManualValue(manualQueueSearch, "la búsqueda en cola");
        if (!value) return;

        runAction(() => searchQueueItem(value), (response) => {
            const payload = getPayload(response);
            setQueuePayload(payload);
            const result = getResult(payload);
            setActiveValues(new Set(result?.found ? [String(result.query)] : []));
        });
    };

    const createEmptyStack = () => runAction(resetStack, (response) => setStackPayload(getPayload(response)));

    const addManualStackNode = () => {
        const value = validateManualValue(manualStackValue, "la pila");
        if (!value) return;

        runAction(() => pushStackItem(value), (response) => {
            setStackPayload(getPayload(response));
            setActiveValues(new Set([value]));
        });
    };

    const findManualStackNode = () => {
        const value = validateManualValue(manualStackSearch, "la búsqueda en pila");
        if (!value) return;

        runAction(() => searchStackItem(value), (response) => {
            const payload = getPayload(response);
            setStackPayload(payload);
            const result = getResult(payload);
            setActiveValues(new Set(result?.found ? [String(result.query)] : []));
        });
    };

    const popManualStackNode = () => runAction(popStackItem, (response) => setStackPayload(getPayload(response)));

    const dequeueQueue = () => runAction(dequeueAdvisoryTurn, (response) => setQueuePayload(getPayload(response)));

    const pushNavigation = () => {
        const module = navigationModule.trim();
        if (!module) {
            setError("Ingresa el módulo académico que se agregará a la pila.");
            return;
        }

        runAction(() => pushStackNavigation(module), (response) => setStackPayload(getPayload(response)));
    };

    const backNavigation = () => runAction(backStackNavigation, (response) => setStackPayload(getPayload(response)));

    const showStackTop = () => runAction(peekStack, (response) => {
        const payload = getPayload(response);
        setStackPayload(payload);
        const top = getResult(payload)?.peek || getResult(payload)?.top;
        setActiveValues(new Set(top ? [String(top)] : []));
    });

    return (
        <MainLayout>
            <section className="rounded-2xl border border-gray-700 bg-gray-800 p-6 shadow-lg">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                    <div>
                        <p className="text-sm font-bold uppercase tracking-[0.25em] text-cyan-300">Épica 12</p>
                        <h2 className="mt-2 text-2xl font-bold text-white">Estructuras lineales contextualizadas</h2>
                        <p className="mt-3 max-w-3xl text-gray-300">Lista, cola y pila se visualizan en un solo módulo para explicar casos universitarios reales: inscritos por curso, turnos de asesoría e historial LIFO.</p>
                    </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-2">
                    {tabs.map((tab) => (
                        <button key={tab.id} type="button" onClick={() => { setActiveTab(tab.id); setActiveValues(new Set()); }} className={`rounded-xl px-4 py-2 font-semibold transition ${activeTab === tab.id ? "bg-cyan-600 text-white" : "border border-gray-700 bg-gray-900 text-gray-300 hover:border-cyan-500"}`}>
                            {tab.label}
                        </button>
                    ))}
                </div>

                {(message || error) && (
                    <div className={`mt-5 rounded-xl border px-4 py-3 text-sm ${error ? "border-red-700 bg-red-950/50 text-red-200" : "border-green-700 bg-green-950/40 text-green-200"}`}>
                        {error || message}
                    </div>
                )}

                <div className="mt-6 grid gap-4 lg:grid-cols-4">
                    <MetricCard label="Cantidad" value={getMetricValue(currentPayload, currentResult, "count", currentResult?.size ?? 0)} />
                    <MetricCard label="Aristas" value={getMetricValue(currentPayload, currentResult, "edgesCount", getEdges(currentPayload || {}).length)} />
                    <MetricCard label={activeTab === "list" ? "Head / Front" : activeTab === "queue" ? "Front" : "Top"} value={activeTab === "list" ? currentResult?.head || "—" : activeTab === "queue" ? currentResult?.front || "—" : currentResult?.top || "—"} />
                    <MetricCard label={activeTab === "list" ? "Tail" : activeTab === "queue" ? "Rear" : "Política"} value={activeTab === "list" ? currentResult?.tail || "—" : activeTab === "queue" ? currentResult?.rear || "—" : currentResult?.navigationPolicy || "LIFO"} />
                </div>

                <div className="mt-6 grid gap-6 xl:grid-cols-[2fr_1fr]">
                    <div className="space-y-4">
                        {activeTab === "list" && (
                            <section className="rounded-2xl border border-gray-700 bg-gray-900 p-5">
                                <h3 className="text-lg font-semibold text-white">Lista enlazada: estudiantes inscritos por curso</h3>
                                <p className="mt-2 text-sm text-gray-300">Cada nodo representa un estudiante real inscrito. El enlace indica el recorrido desde HEAD hasta TAIL.</p>
                                <div className="mt-4 flex flex-col gap-3 md:flex-row">
                                    <select value={selectedCourseId} onChange={(event) => setSelectedCourseId(event.target.value)} className="min-h-11 flex-1 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500">
                                        {courses.map((course) => <option key={course.courseId} value={course.courseId}>{course.label || course.courseId} ({course.studentsCount ?? course.enrolledCount ?? 0})</option>)}
                                    </select>
                                    <button type="button" disabled={loading} onClick={loadSelectedCourse} className="rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60">Cargar inscritos</button>
                                    <button type="button" disabled={loading || !listPayload} onClick={showTraversal} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-lime-400 disabled:cursor-not-allowed disabled:opacity-60">Ver recorrido</button>
                                </div>
                                <div className="mt-5 rounded-2xl border border-cyan-900/60 bg-cyan-950/20 p-4">
                                    <p className="text-sm font-semibold text-cyan-100">Modo libre: crea tu lista desde cero o agrega nodos manuales a la estructura actual.</p>
                                    <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_auto_auto]">
                                        <input value={manualListValue} onChange={(event) => setManualListValue(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Valor del nuevo nodo" />
                                        <select value={manualListPosition} onChange={(event) => setManualListPosition(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500">
                                            <option value="tail">Insertar al final / tail</option>
                                            <option value="head">Insertar al inicio / head</option>
                                        </select>
                                        <button type="button" disabled={loading} onClick={addManualListNode} className="rounded-xl border border-cyan-500 px-4 py-2 font-semibold text-cyan-100 transition hover:bg-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-60">Agregar nodo</button>
                                    </div>
                                    <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_auto_auto_auto]">
                                        <input value={manualListSearch} onChange={(event) => setManualListSearch(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Valor exacto para buscar o eliminar" />
                                        <button type="button" disabled={loading || !listPayload} onClick={findManualListNode} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-lime-400 disabled:cursor-not-allowed disabled:opacity-60">Buscar</button>
                                        <button type="button" disabled={loading || !listPayload} onClick={removeManualListNode} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-orange-400 disabled:cursor-not-allowed disabled:opacity-60">Eliminar</button>
                                        <button type="button" disabled={loading} onClick={createEmptyList} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-red-400 disabled:cursor-not-allowed disabled:opacity-60">Crear lista vacía</button>
                                    </div>
                                </div>
                            </section>
                        )}

                        {activeTab === "queue" && (
                            <section className="rounded-2xl border border-gray-700 bg-gray-900 p-5">
                                <h3 className="text-lg font-semibold text-white">Cola FIFO: turnos de asesoría académica</h3>
                                <p className="mt-2 text-sm text-gray-300">El primer estudiante en llegar queda en FRONT y será atendido primero. Sin magia negra: FIFO puro.</p>
                                {advisorySummary && <p className="mt-2 text-xs text-gray-400">Turnos disponibles en dataset: {advisorySummary.count || advisorySummary.size || 0}</p>}
                                <div className="mt-4 flex flex-wrap gap-3">
                                    <button type="button" disabled={loading} onClick={loadQueue} className="rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60">Cargar turnos</button>
                                    <button type="button" disabled={loading || !queuePayload} onClick={showQueueFront} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-60">Consultar front</button>
                                    <button type="button" disabled={loading || !queuePayload} onClick={dequeueQueue} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-orange-400 disabled:cursor-not-allowed disabled:opacity-60">Atender / dequeue</button>
                                    <button type="button" disabled={loading || !queuePayload} onClick={showTraversal} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-lime-400 disabled:cursor-not-allowed disabled:opacity-60">Ver recorrido</button>
                                </div>
                                <div className="mt-5 rounded-2xl border border-cyan-900/60 bg-cyan-950/20 p-4">
                                    <p className="text-sm font-semibold text-cyan-100">Modo libre: crea una cola desde cero y encola turnos manuales al rear.</p>
                                    <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_auto_auto]">
                                        <input value={manualQueueValue} onChange={(event) => setManualQueueValue(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Valor del nuevo turno" />
                                        <button type="button" disabled={loading} onClick={addManualQueueNode} className="rounded-xl border border-cyan-500 px-4 py-2 font-semibold text-cyan-100 transition hover:bg-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-60">Encolar nodo</button>
                                        <button type="button" disabled={loading} onClick={createEmptyQueue} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-red-400 disabled:cursor-not-allowed disabled:opacity-60">Crear cola vacía</button>
                                    </div>
                                    <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_auto]">
                                        <input value={manualQueueSearch} onChange={(event) => setManualQueueSearch(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Valor exacto para buscar" />
                                        <button type="button" disabled={loading || !queuePayload} onClick={findManualQueueNode} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-lime-400 disabled:cursor-not-allowed disabled:opacity-60">Buscar</button>
                                    </div>
                                </div>
                            </section>
                        )}

                        {activeTab === "stack" && (
                            <section className="rounded-2xl border border-gray-700 bg-gray-900 p-5">
                                <h3 className="text-lg font-semibold text-white">Pila LIFO: historial académico</h3>
                                <p className="mt-2 text-sm text-gray-300">El módulo más reciente queda en TOP. El botón atrás desapila el historial, como navegador académico con toga.</p>
                                <div className="mt-4 flex flex-col gap-3 md:flex-row">
                                    <input value={navigationModule} onChange={(event) => setNavigationModule(event.target.value)} className="min-h-11 flex-1 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Ej. Curso CUR-013" />
                                    <button type="button" disabled={loading} onClick={loadHistory} className="rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60">Cargar historial</button>
                                </div>
                                <div className="mt-3 flex flex-wrap gap-3">
                                    <button type="button" disabled={loading} onClick={pushNavigation} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-60">Agregar navegación</button>
                                    <button type="button" disabled={loading || !stackPayload} onClick={backNavigation} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-orange-400 disabled:cursor-not-allowed disabled:opacity-60">Volver atrás</button>
                                    <button type="button" disabled={loading || !stackPayload} onClick={showStackTop} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-60">Consultar top</button>
                                    <button type="button" disabled={loading || !stackPayload} onClick={showTraversal} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-lime-400 disabled:cursor-not-allowed disabled:opacity-60">Ver recorrido</button>
                                </div>
                                <div className="mt-5 rounded-2xl border border-cyan-900/60 bg-cyan-950/20 p-4">
                                    <p className="text-sm font-semibold text-cyan-100">Modo libre: crea una pila desde cero y apila nodos manuales al TOP.</p>
                                    <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_auto_auto_auto]">
                                        <input value={manualStackValue} onChange={(event) => setManualStackValue(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Valor del nuevo nodo" />
                                        <button type="button" disabled={loading} onClick={addManualStackNode} className="rounded-xl border border-cyan-500 px-4 py-2 font-semibold text-cyan-100 transition hover:bg-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-60">Apilar nodo</button>
                                        <button type="button" disabled={loading || !stackPayload} onClick={popManualStackNode} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-orange-400 disabled:cursor-not-allowed disabled:opacity-60">Desapilar</button>
                                        <button type="button" disabled={loading} onClick={createEmptyStack} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-red-400 disabled:cursor-not-allowed disabled:opacity-60">Crear pila vacía</button>
                                    </div>
                                    <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_auto]">
                                        <input value={manualStackSearch} onChange={(event) => setManualStackSearch(event.target.value)} className="min-h-11 rounded-xl border border-gray-700 bg-gray-950 px-3 py-2 text-gray-100 outline-none focus:border-cyan-500" placeholder="Valor exacto para buscar" />
                                        <button type="button" disabled={loading || !stackPayload} onClick={findManualStackNode} className="rounded-xl border border-gray-600 px-4 py-2 font-semibold text-gray-100 transition hover:border-lime-400 disabled:cursor-not-allowed disabled:opacity-60">Buscar</button>
                                    </div>
                                </div>
                            </section>
                        )}

                        <FlowPanel payload={currentPayload || {}} activeValues={activeValues} emptyMessage="Carga una demo o crea una estructura vacía para empezar a agregar nodos manuales." />
                    </div>

                    <ItemsList title={activeTab === "list" ? "Recorrido de inscritos" : activeTab === "queue" ? "Orden FIFO" : "Orden desde TOP"} items={currentItems} emptyText="Aún no hay elementos cargados para esta estructura." />
                </div>
            </section>
        </MainLayout>
    );
};

export default LinearStructuresPage;
