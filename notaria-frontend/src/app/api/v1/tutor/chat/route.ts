import { NextResponse } from 'next/server'

const RESPONSES: Record<string, string> = {
  'como usar ingesis': 'Para usar Ingesis SRL, primero debes iniciar sesión con tus credenciales. Luego puedes acceder a los módulos de gestión de clientes, documentos y reportes.',
  cliente: "En Ingesis SRL, puedes gestionar clientes desde el módulo 'Clientes'. Allí puedes agregar nuevos clientes, editar información existente y ver el historial.",
  documento: "Para gestionar documentos en Ingesis SRL, ve al módulo 'Documentos'. Puedes subir archivos PDF, asignarlos a clientes y categorizarlos.",
  reporte: "Los reportes en Ingesis SRL se generan desde el módulo 'Reportes'. Puedes crear reportes de clientes, documentos y actividades.",
  configuracion: "La configuración de Ingesis SRL está en el menú 'Configuración'. Allí puedes modificar ajustes del sistema, usuarios y permisos.",
}

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const q = (body?.question || '').toLowerCase()
    let best = 'Soy el tutor de Ingesis SRL. ¿Qué necesitas saber?'
    for (const [k, v] of Object.entries(RESPONSES)) {
      if (q.includes(k)) { best = v; break }
    }
    return NextResponse.json({ response: best, sources: ['Manual de Ingesis SRL'], confidence: 0.8 })
  } catch {
    return NextResponse.json({ detail: 'Error en la solicitud' }, { status: 400 })
  }
}

export async function OPTIONS() {
  return new NextResponse(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
