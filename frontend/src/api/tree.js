import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getTreeEndpoint = (path) => `${API_URL}/tree${path}`;

const extractResponseData = (response) => response.data;

export const getGeneralTreeState = async () => {
  const response = await axios.get(getTreeEndpoint("/state"));
  return extractResponseData(response);
};

export const loadGeneralTreeDemo = async () => {
  const response = await axios.post(getTreeEndpoint("/demo/load"));
  return extractResponseData(response);
};

export const resetGeneralTree = async () => {
  const response = await axios.post(getTreeEndpoint("/reset"));
  return extractResponseData(response);
};

export const insertGeneralTreeNode = async ({
  id,
  label,
  parentId,
  category,
  metadata,
}) => {
  const response = await axios.post(getTreeEndpoint("/insert"), {
    id,
    label,
    parentId,
    category,
    metadata,
  });
  return extractResponseData(response);
};

export const deleteGeneralTreeNode = async (id) => {
  const response = await axios.delete(getTreeEndpoint("/delete"), {
    data: { id },
  });
  return extractResponseData(response);
};

export const searchGeneralTreeNode = async (id) => {
  const response = await axios.get(getTreeEndpoint("/search"), {
    params: { id },
  });
  return extractResponseData(response);
};

export const traverseGeneralTree = async (type = "levelorder") => {
  const response = await axios.get(getTreeEndpoint("/traverse"), {
    params: { type },
  });
  return extractResponseData(response);
};

export const getGeneralTreeMetrics = async () => {
  const response = await axios.get(getTreeEndpoint("/metrics"));
  return extractResponseData(response);
};
