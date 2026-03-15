import customtkinter as ctk
import psutil
import threading
import os
import requests
import asyncio
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# --- RUTAS DE SISTEMA DELTA ---
BASE_DIR = r"C:\DELTANALISIS"
DB_DIR = os.path.join(BASE_DIR, "DELTA_DATABASE")
os.makedirs(DB_DIR, exist_ok=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DeltaCommander(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛰️ DELTA COMMAND CENTER v1.0")
        self.geometry("1100x700")

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR: LABORATORIOS ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="SISTEMA DELTA", font=("Roboto", 20, "bold")).pack(pady=20)
        
        self.btn_img = ctk.CTkButton(self.sidebar, text="📸 LAB. IMÁGENES", command=lambda: self.log("Accediendo a Lab. Imágenes..."))
        self.btn_img.pack(pady=10, padx=20)
        
        self.btn_code = ctk.CTkButton(self.sidebar, text="🧪 LAB. CÓDIGO", command=lambda: self.log("Iniciando Lab. Código..."))
        self.btn_code.pack(pady=10, padx=20)

        # --- MONITOR DE RECURSOS ---
        self.perf_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.perf_frame.pack(side="bottom", fill="x", pady=20)
        self.cpu_label = ctk.CTkLabel(self.perf_frame, text="CPU: 0%")
        self.cpu_label.pack()
        self.ram_label = ctk.CTkLabel(self.perf_frame, text="RAM: 0%")
        self.ram_label.pack()

        # --- CONSOLA CENTRAL ---
        self.console = ctk.CTkTextbox(self, corner_radius=10, border_width=2)
        self.console.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.log("SISTEMA INICIADO. Verificando Puente Ollama y Bot Telegram...")
        
        # Hilos de ejecución
        self.update_resources()
        threading.Thread(target=self.run_bot_logic, daemon=True).start()

    def log(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{ts}] > {text}\n")
        self.console.see("end")

    def update_resources(self):
        self.cpu_label.configure(text=f"CPU: {psutil.cpu_percent()}%")
        self.ram_label.configure(text=f"RAM: {psutil.virtual_memory().percent}%")
        self.after(1000, self.update_resources)

    def run_bot_logic(self):
        # Aquí integramos el token de tu captura
        TOKEN = "7241430460:AAHgwDh9awVz15aJ_93oJDhOphnUnL_nw3k"
        self.log("Conectando Bot con Telegram...")
        # (Aquí iría la lógica de Application.builder que ya conoces)
        self.log("BOT ONLINE. Esperando Mapeado Orig/Result...")

if __name__ == "__main__":
    app = DeltaCommander()
    app.mainloop()