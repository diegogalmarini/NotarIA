export default function PanelPage() {
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Panel de Control
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Gestión y supervisión del sistema
        </p>
        
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Funcionalidad en Desarrollo
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>
                  Esta sección está en construcción. Próximamente podrás gestionar usuarios, ver estadísticas y administrar el sistema.
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Gestión de Usuarios
            </h3>
            <p className="text-gray-600 mb-4">
              Administra los usuarios del sistema.
            </p>
            <button className="bg-gray-400 text-white px-4 py-2 rounded-md cursor-not-allowed" disabled>
              Próximamente
            </button>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Estadísticas
            </h3>
            <p className="text-gray-600 mb-4">
              Visualiza estadísticas de uso del sistema.
            </p>
            <button className="bg-gray-400 text-white px-4 py-2 rounded-md cursor-not-allowed" disabled>
              Próximamente
            </button>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Configuración
            </h3>
            <p className="text-gray-600 mb-4">
              Configura los parámetros del sistema.
            </p>
            <button className="bg-gray-400 text-white px-4 py-2 rounded-md cursor-not-allowed" disabled>
              Próximamente
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}