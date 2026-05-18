import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage";
import GeneralTreePage from "../pages/GeneralTreePage";
import BinaryTreePage from "../pages/BinaryTreePage";

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/general-tree" element={<GeneralTreePage />} />
        <Route path="/binary-tree" element={<BinaryTreePage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
