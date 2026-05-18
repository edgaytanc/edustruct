import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getAVLEndpoint = (path) => `${API_URL}/avl${path}`;

const extractResponseData = (response) => response.data;

export const getAVLState = async () => {
  const response = await axios.get(getAVLEndpoint("/state"));
  return extractResponseData(response);
};

export const loadAVLDemo = async () => {
  const response = await axios.post(getAVLEndpoint("/demo/load"));
  return extractResponseData(response);
};

export const resetAVLTree = async () => {
  const response = await axios.post(getAVLEndpoint("/reset"));
  return extractResponseData(response);
};

export const insertAVLValue = async (value) => {
  const response = await axios.post(getAVLEndpoint("/insert"), {
    value,
  });
  return extractResponseData(response);
};

export const deleteAVLValue = async (value) => {
  const response = await axios.delete(getAVLEndpoint("/delete"), {
    data: { value },
  });
  return extractResponseData(response);
};

export const searchAVLValue = async (value) => {
  const response = await axios.get(getAVLEndpoint("/search"), {
    params: { value },
  });
  return extractResponseData(response);
};

export const traverseAVLTree = async (type = "levelorder") => {
  const response = await axios.get(getAVLEndpoint("/traverse"), {
    params: { type },
  });
  return extractResponseData(response);
};

export const getAVLMetrics = async () => {
  const response = await axios.get(getAVLEndpoint("/metrics"));
  return extractResponseData(response);
};
