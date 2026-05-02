const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <header className="border-b border-gray-700 bg-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-4">
          <h1 className="text-2xl font-bold text-cyan-400">EduStruct</h1>
          <p className="mt-1 text-sm text-gray-300">
            Visualizador Interactivo de Estructuras de Datos
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {children}
      </main>
    </div>
  );
};

export default MainLayout;