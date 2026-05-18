import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getBinaryTreeEndpoint = (path) => `${API_URL}/binary-tree${path}`;

const extractResponseData = (response) => response.data;

export const getBinaryTreeState = async () => {
  const response = await axios.get(getBinaryTreeEndpoint("/state"));
  return extractResponseData(response);
};

export const loadBinaryTreeDemo = async () => {
  const response = await axios.post(getBinaryTreeEndpoint("/demo/load"));
  return extractResponseData(response);
};

export const resetBinaryTree = async () => {
  const response = await axios.post(getBinaryTreeEndpoint("/reset"));
  return extractResponseData(response);
};

export const insertBinaryTreeValue = async (value) => {
  const response = await axios.post(getBinaryTreeEndpoint("/insert"), {
    value,
  });
  return extractResponseData(response);
};

export const deleteBinaryTreeValue = async (value) => {
  const response = await axios.delete(getBinaryTreeEndpoint("/delete"), {
    data: { value },
  });
  return extractResponseData(response);
};

export const searchBinaryTreeValue = async (value) => {
  const response = await axios.get(getBinaryTreeEndpoint("/search"), {
    params: { value },
  });
  return extractResponseData(response);
};

export const traverseBinaryTree = async (type = "levelorder") => {
  const response = await axios.get(getBinaryTreeEndpoint("/traverse"), {
    params: { type },
  });
  return extractResponseData(response);
};

export const getBinaryTreeMetrics = async () => {
  const response = await axios.get(getBinaryTreeEndpoint("/metrics"));
  return extractResponseData(response);
};
