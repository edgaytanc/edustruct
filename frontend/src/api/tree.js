import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const getTreeEndpoint = (path) => `${API_URL}/tree${path}`;

export const getGeneralTreeState = async () => {
  const response = await axios.get(getTreeEndpoint("/state"));
  return response.data;
};

export const loadGeneralTreeDemo = async () => {
  const response = await axios.post(getTreeEndpoint("/demo/load"));
  return response.data;
};

export const resetGeneralTree = async () => {
  const response = await axios.post(getTreeEndpoint("/reset"));
  return response.data;
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
  return response.data;
};

export const deleteGeneralTreeNode = async (id) => {
  const response = await axios.delete(getTreeEndpoint("/delete"), {
    data: { id },
  });
  return response.data;
};

export const searchGeneralTreeNode = async (id) => {
  const response = await axios.get(getTreeEndpoint("/search"), {
    params: { id },
  });
  return response.data;
};

export const traverseGeneralTree = async (type = "levelorder") => {
  const response = await axios.get(getTreeEndpoint("/traverse"), {
    params: { type },
  });
  return response.data;
};
