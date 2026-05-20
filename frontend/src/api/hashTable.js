import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getHashEndpoint = (path) => `${API_URL}/hash${path}`;
const extractResponseData = (response) => response.data;

export const getHashTableState = async () => {
  const response = await axios.get(getHashEndpoint("/state"));
  return extractResponseData(response);
};

export const configureHashTable = async (capacity) => {
  const response = await axios.post(getHashEndpoint("/configure"), { capacity });
  return extractResponseData(response);
};

export const insertHashEntry = async (key, value) => {
  const response = await axios.post(getHashEndpoint("/insert"), { key, value });
  return extractResponseData(response);
};

export const bulkInsertHashEntries = async (entries) => {
  const response = await axios.post(getHashEndpoint("/bulk-insert"), { entries });
  return extractResponseData(response);
};

export const searchHashKey = async (key) => {
  const response = await axios.get(getHashEndpoint("/search"), {
    params: { key },
  });
  return extractResponseData(response);
};

export const deleteHashKey = async (key) => {
  const response = await axios.delete(getHashEndpoint("/delete"), {
    params: { key },
  });
  return extractResponseData(response);
};

export const loadHashDemo = async () => {
  const response = await axios.post(getHashEndpoint("/demo/load"));
  return extractResponseData(response);
};

export const traverseHashBuckets = async () => {
  const response = await axios.get(getHashEndpoint("/traverse"));
  return extractResponseData(response);
};

export const getHashMetrics = async () => {
  const response = await axios.get(getHashEndpoint("/metrics"));
  return extractResponseData(response);
};

export const resetHashTable = async () => {
  const response = await axios.post(getHashEndpoint("/reset"));
  return extractResponseData(response);
};
