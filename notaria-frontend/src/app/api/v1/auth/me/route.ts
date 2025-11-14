import { NextResponse } from 'next/server'

const USERS: Record<string, { role: string; id: number }> = {
  'diegogalmarini@gmail.com': { role: 'admin', id: 1 },
  'empleado@escribania.com': { role: 'empleado', id: 2 },
}

export async function GET(req: Request) {
  const auth = (req.headers as any).get?.('authorization') || ''
  if (!auth.startsWith('Bearer ')) {
    return NextResponse.json({ detail: 'No autorizado' }, { status: 401 })
  }
  const token = auth.slice(7)
  const parts = token.split('.')
  if (parts.length !== 3) {
    return NextResponse.json({ detail: 'Token inválido' }, { status: 401 })
  }
  try {
    const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString())
    const email = payload.sub as string
    const user = USERS[email]
    if (!user) {
      return NextResponse.json({ detail: 'Usuario no encontrado' }, { status: 401 })
    }
    return NextResponse.json({ id: user.id, email, role: user.role })
  } catch {
    return NextResponse.json({ detail: 'Token inválido' }, { status: 401 })
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
