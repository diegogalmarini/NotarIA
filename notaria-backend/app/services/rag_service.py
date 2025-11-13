import httpx
import os
import re
from typing import Optional
from app.core.config import settings

async def get_tutor_response(prompt: str) -> str:
    """
    Get response from Gemini API based on the prompt and system instructions.
    If API fails, use manual content fallback.
    """
    
    def extract_user_question(text: str) -> str:
        marker = "Pregunta del usuario:"
        idx = text.rfind(marker)
        if idx != -1:
            return text[idx + len(marker):].strip()
        return text.strip()

    user_question = extract_user_question(prompt)

    if settings.GEMINI_API_KEY:
        # Gemini API implementation
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        return content
                    else:
                        return "No se recibió una respuesta válida del modelo."
                else:
                    return await get_manual_fallback_response(user_question)
                    
        except Exception as e:
            return await get_manual_fallback_response(user_question)
    
    elif settings.OPENAI_API_KEY:
        # OpenAI API fallback
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    return await get_manual_fallback_response(user_question)
                    
        except Exception as e:
            return await get_manual_fallback_response(user_question)
    
    # If no API key is configured, use manual fallback
    return await get_manual_fallback_response(user_question)

async def get_manual_fallback_response(prompt: str) -> str:
    """
    Fallback response using content from the manual.
    """
    try:
        # Read the knowledge base
        manual_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge-base.md')
        with open(manual_path, 'r', encoding='utf-8') as f:
            manual_content = f.read()
        
        # Extract relevant information based on keywords
        prompt_lower = prompt.lower()
        
        # Common Ingesis questions and their answers from the manual
        if 'acceso directo' in prompt_lower or 'accesos directos' in prompt_lower:
            return get_accesos_directos_response()
        elif 'ventana de edición' in prompt_lower or 'área de edición' in prompt_lower:
            return get_ventana_edicion_response()
        elif 'menú archivo' in prompt_lower or 'archivo' in prompt_lower:
            return get_menu_archivo_response()
        elif 'protocolw' in prompt_lower:
            return get_protocolw_response()
        elif 'exportar' in prompt_lower or 'csv' in prompt_lower or 'pdf' in prompt_lower:
            return get_exportar_response()
        elif 'índice' in prompt_lower or 'indice' in prompt_lower:
            return get_indice_response()
        else:
            # Generic response with manual reference
            return f"""Hola! Soy el Tutor Ingesis de la Escribanía Galmarini. 

Basándome en el manual oficial de Ingesis SRL, puedo ayudarte con dudas sobre:

✅ **ProtocolW** - Gestión de protocolo y escrituras
✅ **IngedatW** - Índices y datos de escrituras  
✅ **IngefactW** - Facturación
✅ **InterlineadorW** - Edición de documentos notariales
✅ **Módulos complementarios** - Exportación, caucionarios, etc.

Tu pregunta: "{prompt}"

⚠️ **Importante**: Solo puedo responder sobre lo que está documentado en el manual oficial. Para temas de instalación, configuración de red, o procedimientos técnicos no documentados, te recomiendo contactar al soporte técnico de Ingesis SRL.

¿Podés ser más específico sobre qué módulo o función de Ingesis necesitás ayuda?"""
            
    except Exception as e:
        return f"Estoy procesando el manual de Ingesis para poder ayudarte mejor. Por el momento, te recomiendo contactar al soporte técnico de Ingesis SRL para asistencia con: {prompt}"

def get_accesos_directos_response() -> str:
    """Response for desktop shortcuts question."""
    return """¡Hola! Según el manual oficial de Ingesis, te explico cómo crear accesos directos en el escritorio:

**Procedimiento para crear accesos directos en el escritorio de Windows:**

1. Hacé click en **Inicio** → **Todos los programas** → **Sistemas Notariales**
2. Hacé click derecho sobre el nombre del programa cuyo acceso directo querés crear
3. Seleccioná **Enviar a** → **Escritorio (crear acceso directo)**

✅ **Resultado**: Se creará un acceso directo en tu escritorio para acceder rápidamente a los módulos de Ingesis.

💡 **Tip**: Podés repetir este proceso para cada módulo que uses frecuentemente (ProtocolW, IngedatW, IngefactW, etc.).

¿Necesitás ayuda con algo más sobre la configuración de Ingesis?"""

def get_ventana_edicion_response() -> str:
    """Response for editing window question."""
    return """¡Perfecto! Te explico sobre la ventana de edición de ProtocolW según el manual oficial:

**Ventana de edición - Área de trabajo principal:**

📍 **Ubicación**: Zona central de la pantalla donde ProtocolW muestra los documentos.

**Funciones principales:**
✅ **Edición de texto** - Podés modificar documentos abiertos con "Abrir" o "Abrir modelo"
✅ **Menú contextual** - Click derecho para opciones de edición
✅ **Menú de formato** - MAYÚSCULAS + Click derecho para opciones de formato

**Comandos útiles:**
- **Click izquierdo**: Mueve el cursor o selecciona objetos
- **Doble click**: Selecciona palabras y convierte números a letras
- **Click y arrastrar**: Selecciona bloques de texto
- **MAYÚSCULAS + Click izquierdo**: Extiende la selección

**Atajos de teclado:**
- **INICIO/FIN**: Principio/final de línea
- **RE PÁG/AV PÁG**: Desplaza una página arriba/abajo
- **Flechas**: Movimiento básico del cursor

¿Querés saber sobre alguna función específica de edición?"""

def get_menu_archivo_response() -> str:
    """Response for file menu question."""
    return """¡Hola! Te explico el menú **Archivo** de ProtocolW según el manual oficial:

**Menú principal - Archivo:**

**📄 Nuevo**: Crea un documento vacío con formato predeterminado
- Asigna nombre automático: S-NombreX (X = 1, 2, 3...)
- Aplica el "Formato inicial" configurado
- Para escribanías: usa formato de foja de protocolo de tu jurisdicción

**📂 Abrir**: Accede a documentos existentes
- Diálogo standard de Windows
- Permite cambiar carpetas y crear nuevas
- Soporta múltiples formatos: .prw, .rtf, .txt, .doc, .html

**👁️ Abrir para ver**: Solo lectura sin riesgo de modificar
- Fondo de color distinto indica modo solo lectura
- Perfecto para consultar y copiar sin alterar

**💾 Guardar/Guardar como**: Almacena tus documentos
- Mantiene formato original del documento
- Permite cambiar nombre y ubicación

**📋 Abrir modelo**: Acceso rápido a documentos modelo
- Usa carpeta de modelos configurada
- Ideal para plantillas repetitivas

¿Necesitás ayuda con alguna función específica del menú Archivo?"""

def get_protocolw_response() -> str:
    """Response for ProtocolW specific questions."""
    return """¡Buena elección! ProtocolW es el módulo principal de Ingesis para gestión de protocolo y escrituras.

**¿Qué es ProtocolW?**
Es el sistema de edición y gestión de documentos notariales y de protocolo de Ingesis SRL.

**Funciones principales:**
✅ **Edición avanzada de textos** con formato profesional
✅ **Gestión de documentos** (.prw, .rtf, .txt, .doc, .html)
✅ **Conversión automática** números a letras con doble click
✅ **Plantillas y modelos** para documentos repetitivos
✅ **Menús contextuales** para edición y formato rápido

**Formatos soportados:**
- **.prw** (ProtocolW nativo)
- **.rtf** (Rich Text Format)
- **.txt** (texto plano)
- **.doc/.docx** (Microsoft Word)
- **.html** (páginas web)

**Características especiales:**
- Conversión de números a letras automática
- Formatos predefinidos por jurisdicción
- Compatibilidad con sistemas DOS antiguos
- Importación desde Ingecert (versión DOS)

¿Sobre qué aspecto de ProtocolW necesitás información específica?"""

def get_exportar_response() -> str:
    """Response for export questions."""
    return """¡Excelente pregunta sobre exportación! Según el manual oficial de Ingesis:

**Opciones de exportación en Ingesis:**

✅ **SÍ tiene exportación** (pero con limitaciones):
- **Reportes a CSV y PDF** desde la vista previa de reportes
- **Diseñador de reportes** para personalizar salidas
- **Filtrado por** para seleccionar registros específicos

❌ **NO tiene exportación general**:
- No existe exportación masiva de toda la base de datos
- No hay acceso directo a tablas para exportación
- No se pueden exportar datos sin pasar por los reportes

**Procedimiento para exportar reportes:**
1. **Generá el reporte** que necesitás usando los reportes estándar
2. **En la vista previa**, usá el botón **"Exportar"**
3. **Seleccioná formato**: CSV o PDF
4. **Personalizá** (opcional): Usá el botón **"Configurar"** para acceder al diseñador

⚠️ **Importante**: Si necesitás exportación masiva de datos o un reporte específico no documentado, contactá al soporte técnico de Ingesis.

¿Qué tipo de información necesitás exportar?"""

def get_indice_response() -> str:
    """Response for index questions."""
    return """¡Entiendo! Sobre los índices en Ingesis, te cuento lo que dice el manual oficial:

**Índices en Ingesis SRL:**

📋 **Funciones disponibles:**
✅ **Verificar índice** antes de imprimir
✅ **Regenerar índice** desde IngedatW
✅ **Consultar índices históricos** importados de DOS

**Migración de DOS:**
- El sistema puede consultar índices de la versión DOS antigua (Ingecert)
- Estos índices se importan y están disponibles para consulta

⚠️ **Limitaciones importantes:**
- **NO** se documentan procedimientos para borrar índices manualmente
- **NO** se mencionan comandos DOS para gestión de índices
- **NO** se especifican archivos de índice individuales

**Recomendación:**
Para operaciones técnicas de mantenimiento de índices o si tenés problemas específicos, te sugiero contactar al soporte técnico de Ingesis SRL, ya que estas tareas requieren conocimiento especializado.

¿Tenés un problema específico con los índices o necesitás hacer alguna operación en particular?"""
