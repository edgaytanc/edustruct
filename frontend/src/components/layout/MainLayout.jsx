import { Link } from "react-router-dom";

const navItems = [
  { to: "/", label: "Inicio" },
  { to: "/general-tree", label: "Árbol General" },
  { to: "/binary-tree", label: "Árbol Binario" },
  { to: "/avl", label: "AVL" },
  { to: "/btree", label: "Árbol B" },
  { to: "/hash", label: "Hash" },
  { to: "/graph", label: "Grafos" },
  { to: "/linear-structures", label: "Estructuras Lineales" },
];

const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <header className="border-b border-gray-700 bg-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-4">
          <h1 className="text-2xl font-bold text-cyan-400">EduStruct</h1>
          <p className="mt-1 text-sm text-gray-300">
            Visualizador Interactivo de Estructuras de Datos
          </p>

          <nav className="mt-4 flex flex-wrap gap-2">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="rounded-xl border border-gray-700 bg-gray-900 px-3 py-2 text-sm font-semibold text-gray-200 transition hover:border-cyan-500 hover:text-cyan-200"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {children}
      </main>
    </div>
  );
};

export default MainLayout;