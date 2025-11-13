// Vercel Serverless Function - Backend simplificado para Tutor Ingesis
// Versión compatible con @vercel/node

// Mock database
const MOCK_USERS = {
  "diegogalmarini@gmail.com": {
    password: "admin123",
    role: "admin",
    id: 1
  },
  "empleado@escribania.com": {
    password: "empleado123", 
    role: "empleado",
    id: 2
  }
}

// Mock JWT token generation
function createMockToken(email, role) {
  const payload = {
    sub: email,
    role: role,
    exp: 9999999999
  }
  
  // Simple mock JWT (base64 encoded)
  const header = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString('base64')
  const payloadEncoded = Buffer.from(JSON.stringify(payload)).toString('base64')
  const signature = Buffer.from("mock_signature").toString('base64')
  
  return `${header}.${payloadEncoded}.${signature}`
}

// CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': 'https://traewk90lkpb.vercel.app',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Allow-Credentials': 'true',
}

module.exports = async (req, res) => {
  const { method, url } = req;
  const path = new URL(url, `https://${req.headers.host}`).pathname;
  
  console.log(`[Tutor Ingesis API] ${method} ${path}`);
  
  // Handle CORS preflight
  if (method === 'OPTIONS') {
    res.writeHead(200, corsHeaders);
    res.end();
    return;
  }
  
  try {
    // Health check endpoint
    if (path === '/api/health' && method === 'GET') {
      res.writeHead(200, { 
        ...corsHeaders, 
        'Content-Type': 'application/json' 
      });
      res.end(JSON.stringify({ 
        status: "healthy", 
        service: "Tutor Ingesis API - Serverless", 
        mode: "serverless" 
      }));
      return;
    }
    
    // API info endpoint
    if (path === '/api' && method === 'GET') {
      res.writeHead(200, { 
        ...corsHeaders, 
        'Content-Type': 'application/json' 
      });
      res.end(JSON.stringify({
        message: "Tutor Ingesis API - Escribanía Galmarini (Serverless)",
        version: "1.0.0",
        mode: "serverless",
        documentation: "/docs"
      }));
      return;
    }
    
    // Login endpoint
    if (path === '/api/v1/auth/login' && method === 'POST') {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      
      req.on('end', async () => {
        try {
          const { email, password } = JSON.parse(body);
          console.log(`Login attempt for: ${email}`);
          
          // Check if user exists
          const user = MOCK_USERS[email];
          if (!user) {
            res.writeHead(401, { 
              ...corsHeaders, 
              'Content-Type': 'application/json' 
            });
            res.end(JSON.stringify({ detail: "Credenciales inválidas" }));
            return;
          }
          
          // Check password
          if (user.password !== password) {
            res.writeHead(401, { 
              ...corsHeaders, 
              'Content-Type': 'application/json' 
            });
            res.end(JSON.stringify({ detail: "Credenciales inválidas" }));
            return;
          }
          
          // Create token
          const token = createMockToken(email, user.role);
          
          console.log(`Login successful for: ${email} with role: ${user.role}`);
          
          res.writeHead(200, { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          });
          res.end(JSON.stringify({
            access_token: token,
            token_type: "bearer",
            role: user.role
          }));
          
        } catch (error) {
          console.error('Login error:', error);
          res.writeHead(400, { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          });
          res.end(JSON.stringify({ detail: "Datos inválidos" }));
        }
      });
      return;
    }
    
    // User profile endpoint
    if (path === '/api/v1/auth/me' && method === 'GET') {
      const authHeader = req.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        res.writeHead(401, { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        });
        res.end(JSON.stringify({ detail: "No autorizado" }));
        return;
      }
      
      const token = authHeader.split(' ')[1];
      
      try {
        // Decode token (simple validation)
        const parts = token.split('.');
        if (parts.length !== 3) {
          throw new Error('Invalid token format');
        }
        
        const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());
        const email = payload.sub;
        const role = payload.role;
        
        if (!email || !MOCK_USERS[email]) {
          throw new Error('User not found');
        }
        
        res.writeHead(200, { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        });
        res.end(JSON.stringify({
          id: MOCK_USERS[email].id,
          email: email,
          role: role
        }));
        
      } catch (error) {
        console.error('Token validation error:', error);
        res.writeHead(401, { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        });
        res.end(JSON.stringify({ detail: "Token inválido" }));
      }
      return;
    }
    
    // Tutor chat endpoint
    if (path === '/api/v1/tutor/chat' && method === 'POST') {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      
      req.on('end', async () => {
        try {
          const { question } = JSON.parse(body);
          
          // Mock responses for Ingesis SRL questions
          const mockResponses = {
            "como usar ingesis": "Para usar Ingesis SRL, primero debes iniciar sesión con tus credenciales. Luego puedes acceder a los módulos de gestión de clientes, documentos y reportes.",
            "cliente": "En Ingesis SRL, puedes gestionar clientes desde el módulo 'Clientes'. Allí puedes agregar nuevos clientes, editar información existente y ver el historial.",
            "documento": "Para gestionar documentos en Ingesis SRL, ve al módulo 'Documentos'. Puedes subir archivos PDF, asignarlos a clientes y categorizarlos.",
            "reporte": "Los reportes en Ingesis SRL se generan desde el módulo 'Reportes'. Puedes crear reportes de clientes, documentos y actividades.",
            "configuracion": "La configuración de Ingesis SRL está en el menú 'Configuración'. Allí puedes modificar ajustes del sistema, usuarios y permisos."
          };
          
          // Find best matching response
          let bestMatch = "Soy el tutor de Ingesis SRL. Puedo ayudarte con preguntas sobre cómo usar el sistema. ¿Qué necesitas saber?"
          const questionLower = (question || "").toLowerCase();
          
          for (const [keyword, response] of Object.entries(mockResponses)) {
            if (questionLower.includes(keyword)) {
              bestMatch = response;
              break;
            }
          }
          
          res.writeHead(200, { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          });
          res.end(JSON.stringify({
            response: bestMatch,
            sources: ["Manual de Ingesis SRL"],
            confidence: 0.8
          }));
          
        } catch (error) {
          console.error('Chat error:', error);
          res.writeHead(400, { 
            ...corsHeaders, 
            'Content-Type': 'application/json' 
          });
          res.end(JSON.stringify({ detail: "Error en la solicitud" }));
        }
      });
      return;
    }
    
    // Admin init endpoint
    if (path === '/api/admin/init-db' && method === 'POST') {
      res.writeHead(200, { 
        ...corsHeaders, 
        'Content-Type': 'application/json' 
      });
      res.end(JSON.stringify({
        status: "success",
        message: "Mock database initialized",
        users_count: Object.keys(MOCK_USERS).length
      }));
      return;
    }
    
    // 404 for unknown routes
    res.writeHead(404, { 
      ...corsHeaders, 
      'Content-Type': 'application/json' 
    });
    res.end(JSON.stringify({ error: "Ruta no encontrada" }));
    
  } catch (error) {
    console.error('API Error:', error);
    res.writeHead(500, { 
      ...corsHeaders, 
      'Content-Type': 'application/json' 
    });
    res.end(JSON.stringify({ error: "Error interno del servidor" }));
  }
}