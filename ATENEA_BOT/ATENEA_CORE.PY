import logging
from logging.handlers import RotatingFileHandler
import datetime
import requests
import subprocess
import sys
import pkg_resources
import caja_fuerte as cf

# CONFIGURACIÓN DEL LOG ROTATIVO (50MB)
LOG_FILENAME = "atenea_bridge.log"
MAX_BYTES = 50 * 1024 * 1024 
BACKUP_COUNT = 100

rotator = RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotator.setFormatter(formatter)

logger = logging.getLogger("AteneaCore")
logger.setLevel(logging.INFO)
logger.addHandler(rotator)

def registrar_arranque():
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("="*60)
    logger.info(f"ARRANQUE SISTEMA ATENEA - SESIÓN: {ahora}")
    logger.info(f"PROYECTO: {cf.PROJECT_NAME} | AGENTE: {cf.AGENT_NAME}")
    logger.info("="*60)

# ==========================================
# MÓDULO DE AUTO-REPARACIÓN (INSTALADOR)
# ==========================================
def instalar_libreria(libreria):
    """Instala una librería automáticamente si falta."""
    try:
        logger.warning(f"Librería faltante detectada: {libreria}. Iniciando auto-instalación...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
        logger.info(f"Librería {libreria} instalada con éxito.")
        return True
    except Exception as e:
        logger.error(f"Error crítico al intentar instalar {libreria}: {e}")
        return False

def importar_dinamico(nombre_modulo, nombre_pip=None):
    """Intenta importar y si falla, instala."""
    if nombre_pip is None:
        nombre_pip = nombre_modulo
    try:
        return __import__(nombre_modulo)
    except ImportError:
        if instalar_libreria(nombre_pip):
            return __import__(nombre_modulo)
        else:
            raise

# ==========================================
# MOTOR DE CONSULTA
# ==========================================
def consultar_atenea(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{cf.MODEL_NAME}:generateContent?key={cf.GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        # Ejemplo de uso del auto-instalador: Si ATENEA decidiera usar 'pandas' de repente
        # importar_dinamico("pandas") 
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()
        
        texto = res_json['candidates'][0]['content']['parts'][0]['text']
        uso = res_json.get('usageMetadata', {})
        
        logger.info(f"CONSUMO -> Prompt: {uso.get('promptTokenCount', 0)} | Total: {uso.get('totalTokenCount', 0)}")
        return texto
    except Exception as e:
        logger.error(f"ERROR EN MOTOR ATENEA: {e}")
        return "Socio, algo ha fallado en el motor. He registrado el error en el log para revisarlo."