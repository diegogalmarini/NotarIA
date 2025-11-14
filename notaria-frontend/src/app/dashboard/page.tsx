import Link from 'next/link'

export default function DashboardPage() {
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Bienvenido a Escribanía Galmarini
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Sistema de gestión notarial inteligente
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Tutor Ingesis
            </h3>
            <p className="text-gray-600 mb-4">
              Consulta con nuestro asistente de IA especializado en derecho notarial.
            </p>
            <Link
              href="/dashboard/tutor"
              className="inline-block bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition duration-200"
            >
              Ir al Tutor
            </Link>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Panel de Control
            </h3>
            <p className="text-gray-600 mb-4">
              Gestiona y supervisa las operaciones del sistema.
            </p>
            <Link
              href="/dashboard/panel"
              className="inline-block bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition duration-200"
            >
              Ver Panel
            </Link>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Documentación
            </h3>
            <p className="text-gray-600 mb-4">
              Accede a guías y manuales del sistema.
            </p>
            <button
              className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition duration-200 cursor-not-allowed"
              disabled
            >
              Próximamente
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
