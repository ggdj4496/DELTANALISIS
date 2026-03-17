import os
import logging
from logging.handlers import RotatingFileHandler
import requests
import datetime

# ==========================================
# CONFIGURACIÓN DE LA CAJA FUERTE
# ==========================================
API_KEY = "AIzaSyBvdZun08h7sjwrLUtmWZ5s475IY5ekEi0"
MODEL_NAME = "gemini-1.5-flash-latest"
PROJECT_NAME = "ATENEA PROYECT"
AGENT_NAME = "ATENEA AGENT"

# ==========================================
# CONFIGURACIÓN DEL LOG ROTATIVO (50MB)
# ==========================================
LOG_FILENAME = "atenea_bridge.log"
MAX_BYTES = 50 * 1024 * 1024  # 50 Megabytes
BACKUP_COUNT = 100            # Guardará hasta 100 archivos de 50MB (Casi infinito)

# Creamos el handler rotativo
rotator = RotatingFileHandler(
    LOG_FILENAME, 
    maxBytes=MAX_BYTES, 
    backupCount=BACKUP_COUNT,
    encoding='utf-8'
)

# Formato del log: Fecha - Nivel - Mensaje
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotator.setFormatter(formatter)

# Configuramos el logger principal
logger = logging.getLogger("AteneaBridge")
logger.setLevel(logging.INFO)
logger.addHandler(rotator)

# También mostramos por pantalla para que lo veas en tiempo real
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ==========================================
# MARCA DE ARRANQUE
# ==========================================
ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info("="*60)
logger.info(f"NUEVO ARRANQUE DEL SISTEMA - FECHA: {ahora}")
logger.info(f"PROYECTO: {PROJECT_NAME} | AGENTE: {AGENT_NAME}")
logger.info("="*60)

class AteneaBot:
    def __init__(self):
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
        self.headers = {'Content-Type': 'application/json'}

    def preguntar(self, prompt):
        """Envía petición y registra consumo en el log rotativo."""
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            resultado = response.json()
            
            texto_respuesta = resultado['candidates'][0]['content']['parts'][0]['text']
            
            # Extraer metadatos de consumo de tokens
            uso = resultado.get('usageMetadata', {})
            p_tokens = uso.get('promptTokenCount', 0)
            c_tokens = uso.get('candidatesTokenCount', 0)
            
            # Guardamos el rastro en el log de 50MB
            logger.info(f"CONSUMO -> Prompt: {p_tokens} | Respuesta: {c_tokens} | Total: {p_tokens + c_tokens}")
            
            return texto_respuesta

        except Exception as e:
            logger.error(f"ERROR EN EL PUENTE: {e}")
            return "Socio, hay un problema con el puente. Mira el log."

# ==========================================
# BUCLE DE CONTROL
# ==========================================
if __name__ == "__main__":
    atenea = AteneaBot()
    print(f"\nSocio, ATENEA está escuchando... (Escribe 'salir' para cerrar)")
    
    while True:
        user_input = input("\n>>> ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            logger.info("Cierre de sesión solicitado por el usuario.")
            break
            
        respuesta = atenea.preguntar(user_input)
        print(f"\nATENEA: {respuesta}")