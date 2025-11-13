// Serverless Function colocada dentro del proyecto Next.js
const MOCK_USERS = {
  "diegogalmarini@gmail.com": { password: "admin123", role: "admin", id: 1 },
  "empleado@escribania.com": { password: "empleado123", role: "empleado", id: 2 },
}

function createMockToken(email, role) {
  const payload = { sub: email, role, exp: 9999999999 }
  const header = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString('base64')
  const payloadEncoded = Buffer.from(JSON.stringify(payload)).toString('base64')
  const signature = Buffer.from("mock_signature").toString('base64')
  return `${header}.${payloadEncoded}.${signature}`
}

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

module.exports = async (req, res) => {
  const { method, url } = req
  if (method === 'OPTIONS') { res.writeHead(200, corsHeaders); res.end(); return }
  try {
    const path = (url || '/').split('?')[0]
    if (path === '/api/health' && method === 'GET') {
      res.writeHead(200, { ...corsHeaders, 'Content-Type': 'application/json' })
      res.end(JSON.stringify({ status: 'healthy', service: 'Tutor Ingesis API - Serverless', mode: 'serverless' }))
      return
    }
    if (path === '/api/v1/auth/login' && method === 'POST') {
      let body = ''
      req.on('data', c => body += c.toString())
      req.on('end', () => {
        try {
          if (!body.trim()) { res.writeHead(400, { ...corsHeaders, 'Content-Type': 'application/json' }); res.end(JSON.stringify({ detail: 'Cuerpo vacío' })); return }
          const { email, password } = JSON.parse(body)
          const user = MOCK_USERS[email]
          if (!user || user.password !== password) { res.writeHead(401, { ...corsHeaders, 'Content-Type': 'application/json' }); res.end(JSON.stringify({ detail: 'Credenciales inválidas' })); return }
          const token = createMockToken(email, user.role)
          res.writeHead(200, { ...corsHeaders, 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ access_token: token, token_type: 'bearer', role: user.role }))
        } catch (e) {
          res.writeHead(400, { ...corsHeaders, 'Content-Type': 'application/json' }); res.end(JSON.stringify({ detail: 'Datos inválidos' }))
        }
      })
      return
    }
    if (path === '/api/v1/auth/me' && method === 'GET') {
      const authHeader = req.headers.authorization
      if (!authHeader || !authHeader.startsWith('Bearer ')) { res.writeHead(401, { ...corsHeaders, 'Content-Type': 'application/json' }); res.end(JSON.stringify({ detail: 'No autorizado' })); return }
      const token = authHeader.split(' ')[1]
      const parts = token.split('.')
      if (parts.length !== 3) { res.writeHead(401, { ...corsHeaders, 'Content-Type': 'application/json' }); res.end(JSON.stringify({ detail: 'Token inválido' })); return }
      const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString())
      const email = payload.sub
      const user = MOCK_USERS[email]
      if (!user) { res.writeHead(401, { ...corsHeaders, 'Content-Type': 'application/json' }); res.end(JSON.stringify({ detail: 'Usuario no encontrado' })); return }
      res.writeHead(200, { ...corsHeaders, 'Content-Type': 'application/json' })
      res.end(JSON.stringify({ id: user.id, email: email, role: user.role }))
      return
    }
    res.writeHead(404, { ...corsHeaders, 'Content-Type': 'application/json' })
    res.end(JSON.stringify({ error: 'Ruta no encontrada' }))
  } catch (error) {
    res.writeHead(500, { ...corsHeaders, 'Content-Type': 'application/json' })
    res.end(JSON.stringify({ error: 'Error interno del servidor' }))
  }
}
