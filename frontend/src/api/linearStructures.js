import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

const getEndpoint = (structure, path) => `${API_URL}/${structure}${path}`;
const extractResponseData = (response) => response.data;

export const getListCourses = async () => {
    const response = await axios.get(getEndpoint("list", "/courses"));
    return extractResponseData(response);
};

export const loadListCourse = async (courseId) => {
    const response = await axios.post(getEndpoint("list", "/demo/load-course"), { courseId });
    return extractResponseData(response);
};

export const getListState = async () => {
    const response = await axios.get(getEndpoint("list", "/state"));
    return extractResponseData(response);
};

export const insertListItem = async (value, position = "tail") => {
    const response = await axios.post(getEndpoint("list", "/insert"), { value, position });
    return extractResponseData(response);
};

export const deleteListItem = async (value) => {
    const response = await axios.delete(getEndpoint("list", "/delete"), { data: { value } });
    return extractResponseData(response);
};

export const searchListItem = async (value) => {
    const response = await axios.get(getEndpoint("list", "/search"), { params: { value } });
    return extractResponseData(response);
};

export const resetList = async () => {
    const response = await axios.post(getEndpoint("list", "/reset"));
    return extractResponseData(response);
};

export const traverseList = async () => {
    const response = await axios.get(getEndpoint("list", "/traverse"));
    return extractResponseData(response);
};

export const getAdvisoryTurns = async () => {
    const response = await axios.get(getEndpoint("queue", "/advisory-turns"));
    return extractResponseData(response);
};

export const loadAdvisoryQueue = async () => {
    const response = await axios.post(getEndpoint("queue", "/demo/load-advisory"));
    return extractResponseData(response);
};

export const getQueueFront = async () => {
    const response = await axios.get(getEndpoint("queue", "/front"));
    return extractResponseData(response);
};

export const enqueueQueueItem = async (value) => {
    const response = await axios.post(getEndpoint("queue", "/insert"), { value });
    return extractResponseData(response);
};

export const searchQueueItem = async (value) => {
    const response = await axios.get(getEndpoint("queue", "/search"), { params: { value } });
    return extractResponseData(response);
};

export const resetQueue = async () => {
    const response = await axios.post(getEndpoint("queue", "/reset"));
    return extractResponseData(response);
};

export const dequeueAdvisoryTurn = async () => {
    const response = await axios.delete(getEndpoint("queue", "/delete"));
    return extractResponseData(response);
};

export const traverseQueue = async () => {
    const response = await axios.get(getEndpoint("queue", "/traverse"));
    return extractResponseData(response);
};

export const loadStackHistory = async () => {
    const response = await axios.post(getEndpoint("stack", "/demo/load-history"));
    return extractResponseData(response);
};

export const pushStackNavigation = async (module) => {
    const response = await axios.post(getEndpoint("stack", "/navigation/push"), { module });
    return extractResponseData(response);
};

export const backStackNavigation = async () => {
    const response = await axios.delete(getEndpoint("stack", "/navigation/back"));
    return extractResponseData(response);
};

export const peekStack = async () => {
    const response = await axios.get(getEndpoint("stack", "/peek"));
    return extractResponseData(response);
};

export const pushStackItem = async (value) => {
    const response = await axios.post(getEndpoint("stack", "/insert"), { value });
    return extractResponseData(response);
};

export const popStackItem = async () => {
    const response = await axios.delete(getEndpoint("stack", "/delete"));
    return extractResponseData(response);
};

export const searchStackItem = async (value) => {
    const response = await axios.get(getEndpoint("stack", "/search"), { params: { value } });
    return extractResponseData(response);
};

export const resetStack = async () => {
    const response = await axios.post(getEndpoint("stack", "/reset"));
    return extractResponseData(response);
};

export const traverseStack = async () => {
    const response = await axios.get(getEndpoint("stack", "/traverse"));
    return extractResponseData(response);
};
