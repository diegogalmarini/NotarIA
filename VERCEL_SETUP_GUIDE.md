# Guía de Configuración de Variables de Entorno para Vercel

Esta guía te ayudará a configurar correctamente las variables de entorno necesarias para que el Tutor Ingesis funcione en producción.

## Paso 1: Acceder a la Configuración de Vercel

1. Ve a [Vercel Dashboard](https://vercel.com/dashboard)
2. Busca tu proyecto "notaria-sistema" o similar
3. Haz clic en el proyecto
4. Ve a la pestaña "Settings" (Configuración)
5. En el menú lateral, busca "Environment Variables"

## Paso 2: Agregar Variables de Entorno

Necesitarás agregar las siguientes variables de entorno:

### Variables Requeridas:

1. **NEXT_PUBLIC_API_URL**
   - Valor: `https://traewk90lkpb.vercel.app`
   - Esta es la URL de tu backend en producción

2. **DATABASE_URL**
   - Valor: `sqlite+aiosqlite:///./notaria.db`
   - Usamos SQLite para producción (más simple para Vercel)

3. **SECRET_KEY** (o **JWT_SECRET_KEY**)
   - Valor: `tu_clave_secreta_muy_segura_123456789`
   - Esta clave se usa para firmar los tokens JWT
   - **IMPORTANTE**: Usa una clave segura de al menos 32 caracteres

4. **GEMINI_API_KEY**
   - Valor: `AIzaSyBEMp01OWeFMP8r0G3S3cWqESZnkP6cOmM`
   - Esta es tu clave de API de Google Gemini

### Variables Opcionales (si las necesitas):

5. **ADMIN_EMAIL**
   - Valor: `diegogalmarini@gmail.com`
   - Email del administrador principal

6. **ADMIN_PASSWORD**
   - Valor: `admin123`
   - Contraseña del administrador (cámbiala después)

## Paso 3: Configuración de Variables

Para cada variable:

1. En "Name" (Nombre): escribe el nombre exacto de la variable (ej: `NEXT_PUBLIC_API_URL`)
2. En "Value" (Valor): escribe el valor correspondiente
3. En "Environment" (Entorno): selecciona "Production" y "Preview" si aparece
4. Haz clic en "Add" (Agregar)

## Paso 4: Verificar Configuración

Después de agregar todas las variables, verifica que estén correctamente configuradas:

```
✅ NEXT_PUBLIC_API_URL = https://traewk90lkpb.vercel.app
✅ DATABASE_URL = sqlite+aiosqlite:///./notaria.db
✅ SECRET_KEY = tu_clave_secreta_muy_segura_123456789
✅ GEMINI_API_KEY = AIzaSyBEMp01OWeFMP8r0G3S3cWqESZnkP6cOmM
```

## Paso 5: Reconstruir el Proyecto

1. Ve a la pestaña "Deployments" (Despliegues)
2. Verás el último despliegue con estado "Ready" o "Error"
3. Haz clic en el menú de tres puntos (⋯) del último despliegue
4. Selecciona "Redeploy" (Reconstruir)
5. **IMPORTANTE**: Marca la casilla "Use existing Build Cache" (Usar caché de construcción existente)
6. Haz clic en "Redeploy"

## Paso 6: Verificar el Despliegue

Después de que se complete la reconstrucción (2-3 minutos):

1. Abre tu aplicación: https://traewk90lkpb.vercel.app
2. Intenta iniciar sesión con las credenciales:
   - **Email**: diegogalmarini@gmail.com
   - **Contraseña**: admin123

## Solución de Problemas

### Si aún aparece "Credenciales inválidas":

1. **Verifica las variables de entorno**:
   - Asegúrate de que los nombres estén escritos correctamente (sensibles a mayúsculas)
   - Verifica que la URL de la API sea exactamente: `https://traewk90lkpb.vercel.app`

2. **Verifica el backend**:
   - Abre: https://traewk90lkpb.vercel.app/api/health
   - Deberías ver: `{"status":"ok","message":"Backend funcionando"}`

3. **Verifica la base de datos**:
   - Abre: https://traewk90lkpb.vercel.app/api/admin/init-db
   - Esto creará el usuario admin si no existe

4. **Verifica los logs**:
   - En Vercel, ve a "Deployments"
   - Haz clic en el despliegue más reciente
   - Ve a "Functions" → "api/index.py" para ver los logs del backend

### Comandos de Prueba:

Puedes probar el backend directamente:

```bash
# Test de salud del backend
curl https://traewk90lkpb.vercel.app/api/health

# Test de creación de usuario admin
curl -X POST https://traewk90lkpb.vercel.app/api/admin/init-db

# Test de login
curl -X POST https://traewk90lkpb.vercel.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"diegogalmarini@gmail.com","password":"admin123"}'
```

## Credenciales de Prueba

**Usuario Admin:**
- Email: diegogalmarini@gmail.com
- Contraseña: admin123
- Rol: admin (acceso completo)

**Usuario Empleado (de ejemplo):**
- Email: empleado@escribania.com
- Contraseña: empleado123
- Rol: empleado (acceso limitado)

## Notas Importantes

1. **Seguridad**: Después de que todo funcione, cambia la contraseña del admin
2. **Clave JWT**: Usa una clave más segura en producción real
3. **Base de datos**: SQLite es perfecta para empezar, pero considera PostgreSQL para producción
4. **Backup**: La base de datos SQLite se reinicia con cada despliegue en Vercel

## ¿Necesitas Ayuda?

Si después de seguir esta guía aún tienes problemas:

1. Verifica los logs en Vercel
2. Asegúrate de que todas las variables estén configuradas
3. Prueba los endpoints de prueba mencionados arriba
4. Si el problema persiste, dime exactamente qué error ves

¡Recuerda que el proyecto está correctamente configurado! Solo necesita las variables de entorno apropiadas para funcionar en producción.