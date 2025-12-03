import os
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Obtenemos las variables del entorno (definidas en docker-compose.yml)
EVOLUTION_URL = os.getenv('EVOLUTION_URL', 'http://evolution_api:8080')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configurar Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Usamos el modelo flash por ser rápido y económico
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("⚠️ ADVERTENCIA: No se detectó GOOGLE_API_KEY.")

def enviar_mensaje_whatsapp(instance_name, numero, texto):
    """Envía la respuesta de vuelta a WhatsApp vía Evolution API"""
    if not EVOLUTION_URL or not EVOLUTION_API_KEY:
        print("❌ Error: Faltan credenciales de Evolution API")
        return

    url = f"{EVOLUTION_URL}/message/sendText/{instance_name}"
    
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "number": numero,
        "text": texto
    }
    
    try:
        # Enviamos la petición POST a Evolution
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200: # 201 es Created, 200 OK
            print(f"✅ Respuesta enviada a {numero}")
        else:
            print(f"❌ Error enviando mensaje: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Excepción de red: {e}")

@app.route('/', methods=['GET'])
def health_check():
    return "🧠 El Cerebro Python está ACTIVO y escuchando.", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recibe los eventos de Evolution API"""
    try:
        body = request.json
        
        # 1. Validamos que sea un mensaje nuevo (MESSAGES_UPSERT)
        event = body.get('event')
        if event != 'messages.upsert':
            return jsonify({"status": "ignored", "reason": "not_upsert"}), 200
            
        # 2. Extraemos datos clave
        instance_name = body.get('instance')
        data = body.get('data', {})
        key = data.get('key', {})
        
        # 3. FILTRO CRÍTICO: Ignorar mensajes enviados por mí mismo (evita bucles infinitos)
        if key.get('fromMe'):
            return jsonify({"status": "ignored", "reason": "from_me"}), 200

        # 4. Obtener quién envió el mensaje
        remote_jid = key.get('remoteJid')
        if not remote_jid:
             return jsonify({"status": "error", "reason": "no_jid"}), 200
             
        # Limpiamos el número (viene como 12345@s.whatsapp.net -> 12345)
        numero_usuario = remote_jid.split('@')[0]
        
        # 5. Extraer el texto del mensaje (Baileys tiene varias estructuras)
        mensaje_texto = ""
        msg_content = data.get('message', {})
        
        if 'conversation' in msg_content:
            mensaje_texto = msg_content['conversation']
        elif 'extendedTextMessage' in msg_content:
            mensaje_texto = msg_content['extendedTextMessage'].get('text', '')
            
        if not mensaje_texto:
            return jsonify({"status": "ignored", "reason": "no_text"}), 200

        print(f"📩 Mensaje de {numero_usuario}: {mensaje_texto}")

        # 6. INTELIGENCIA ARTIFICIAL (Gemini)
        if GOOGLE_API_KEY:
            try:
                # Personaliza aquí cómo quieres que se comporte tu bot
                prompt_sistema = (
                    "Eres un asistente virtual amable y profesional. "
                    "Responde de manera concisa y útil al siguiente mensaje de WhatsApp: "
                )
                
                full_prompt = f"{prompt_sistema} {mensaje_texto}"
                
                ai_response = model.generate_content(full_prompt)
                respuesta_final = ai_response.text
                
                # 7. Enviar respuesta al usuario
                enviar_mensaje_whatsapp(instance_name, numero_usuario, respuesta_final)
                
            except Exception as e:
                print(f"❌ Error con Gemini: {e}")
                enviar_mensaje_whatsapp(instance_name, numero_usuario, "Lo siento, tuve un error procesando tu solicitud.")
        
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"❌ Error general en webhook: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    # Ejecución local (para pruebas sin Docker, aunque Docker usa Gunicorn)
    app.run(host='0.0.0.0', port=8000)