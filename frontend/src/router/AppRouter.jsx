import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage";
import GeneralTreePage from "../pages/GeneralTreePage";

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/general-tree" element={<GeneralTreePage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
