import { NextResponse } from 'next/server'

const USERS: Record<string, { password: string; role: string; id: number }> = {
  'diegogalmarini@gmail.com': { password: 'admin123', role: 'admin', id: 1 },
  'empleado@escribania.com': { password: 'empleado123', role: 'empleado', id: 2 },
}

function createToken(email: string, role: string) {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64')
  const payload = Buffer.from(JSON.stringify({ sub: email, role, exp: 9999999999 })).toString('base64')
  const signature = Buffer.from('mock_signature').toString('base64')
  return `${header}.${payload}.${signature}`
}

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const { email, password } = body || {}
    const user = email ? USERS[email] : undefined
    if (!user || user.password !== password) {
      return NextResponse.json({ detail: 'Credenciales inválidas' }, { status: 401 })
    }
    const token = createToken(email, user.role)
    return NextResponse.json({ access_token: token, token_type: 'bearer', role: user.role })
  } catch {
    return NextResponse.json({ detail: 'Datos inválidos' }, { status: 400 })
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
