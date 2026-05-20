import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getBTreeEndpoint = (path) => `${API_URL}/btree${path}`;
const extractResponseData = (response) => response.data;

export const getBTreeState = async () => {
  const response = await axios.get(getBTreeEndpoint("/state"));
  return extractResponseData(response);
};

export const configureBTree = async (order) => {
  const response = await axios.post(getBTreeEndpoint("/configure"), { order });
  return extractResponseData(response);
};

export const insertBTreeKey = async (key) => {
  const response = await axios.post(getBTreeEndpoint("/insert"), { key });
  return extractResponseData(response);
};

export const bulkInsertBTreeKeys = async (keys) => {
  const response = await axios.post(getBTreeEndpoint("/bulk-insert"), { keys });
  return extractResponseData(response);
};

export const searchBTreeKey = async (key) => {
  const response = await axios.get(getBTreeEndpoint("/search"), {
    params: { key },
  });
  return extractResponseData(response);
};

export const loadBTreeDemo = async () => {
  const response = await axios.post(getBTreeEndpoint("/demo/load"));
  return extractResponseData(response);
};

export const traverseBTree = async (type = "levelorder") => {
  const response = await axios.get(getBTreeEndpoint("/traverse"), {
    params: { type },
  });
  return extractResponseData(response);
};

export const getBTreeMetrics = async () => {
  const response = await axios.get(getBTreeEndpoint("/metrics"));
  return extractResponseData(response);
};

export const resetBTree = async () => {
  const response = await axios.post(getBTreeEndpoint("/reset"));
  return extractResponseData(response);
};
