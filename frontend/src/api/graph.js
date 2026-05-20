import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getGraphEndpoint = (path) => `${API_URL}/graph${path}`;
const extractResponseData = (response) => response.data;

export const getGraphState = async () => {
  const response = await axios.get(getGraphEndpoint("/state"));
  return extractResponseData(response);
};

export const addGraphNode = async ({ id, value }) => {
  const response = await axios.post(getGraphEndpoint("/nodes"), { id, value });
  return extractResponseData(response);
};

export const addGraphEdge = async ({ source, target }) => {
  const response = await axios.post(getGraphEndpoint("/edges"), { source, target });
  return extractResponseData(response);
};

export const searchGraphCourse = async (courseId) => {
  const response = await axios.get(getGraphEndpoint("/search"), {
    params: { courseId },
  });
  return extractResponseData(response);
};

export const loadGraphDemo = async () => {
  const response = await axios.post(getGraphEndpoint("/demo/load"));
  return extractResponseData(response);
};

export const traverseGraph = async ({ algorithm, startNodeId }) => {
  const response = await axios.get(getGraphEndpoint("/traverse"), {
    params: { algorithm, startNodeId },
  });
  return extractResponseData(response);
};

export const runGraphDfs = async (startNodeId) => {
  const response = await axios.get(getGraphEndpoint("/dfs"), {
    params: { startNodeId },
  });
  return extractResponseData(response);
};

export const runGraphBfs = async (startNodeId) => {
  const response = await axios.get(getGraphEndpoint("/bfs"), {
    params: { startNodeId },
  });
  return extractResponseData(response);
};

export const getGraphMetrics = async () => {
  const response = await axios.get(getGraphEndpoint("/metrics"));
  return extractResponseData(response);
};

export const resetGraph = async () => {
  const response = await axios.post(getGraphEndpoint("/reset"));
  return extractResponseData(response);
};
