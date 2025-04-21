import tkinter as tk
from tkinter import ttk, messagebox
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

class WhatsAppBusterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Buster")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        self.root.iconbitmap("buster.ico")
        
        # Estilo
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TLabelframe", background="#f0f0f0", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", background="#f0f0f0", font=("Segoe UI", 10, "bold"))
        
        # Variables
        self.phone_number = tk.StringVar()
        self.total_messages = tk.StringVar(value="100")
        self.delay_between_messages = tk.StringVar(value="0.05")
        self.custom_message = tk.StringVar(value="Mensaje de broma")
        self.is_running = False
        self.successful_messages = 0
        self.start_time = None
        self.driver = None
        self.whatsapp_opened = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        title_label = ttk.Label(title_frame, text="WhatsApp Buster", font=("Segoe UI", 24, "bold"))
        title_label.pack()
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botón para abrir WhatsApp Web
        whatsapp_button = ttk.Button(config_frame, text="Abrir WhatsApp Web", command=self.open_whatsapp)
        whatsapp_button.pack(fill=tk.X, pady=(0, 15))
        
        # Campos de entrada
        input_frame = ttk.Frame(config_frame)
        input_frame.pack(fill=tk.X)
        
        # Número de teléfono
        phone_frame = ttk.Frame(input_frame)
        phone_frame.pack(fill=tk.X, pady=5)
        ttk.Label(phone_frame, text="Número de teléfono:").pack(side=tk.LEFT, padx=(0, 10))
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_number, width=40)
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(phone_frame, text="(Ejemplo: +34123456789)", font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Mensaje personalizado
        message_frame = ttk.Frame(input_frame)
        message_frame.pack(fill=tk.X, pady=5)
        ttk.Label(message_frame, text="Mensaje:").pack(side=tk.LEFT, padx=(0, 10))
        message_entry = ttk.Entry(message_frame, textvariable=self.custom_message, width=40)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Total de mensajes
        total_frame = ttk.Frame(input_frame)
        total_frame.pack(fill=tk.X, pady=5)
        ttk.Label(total_frame, text="Total de mensajes:").pack(side=tk.LEFT, padx=(0, 10))
        messages_entry = ttk.Entry(total_frame, textvariable=self.total_messages, width=40)
        messages_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Delay entre mensajes
        delay_frame = ttk.Frame(input_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        ttk.Label(delay_frame, text="Delay de mensajes (segundos):").pack(side=tk.LEFT, padx=(0, 10))
        delay_entry = ttk.Entry(delay_frame, textvariable=self.delay_between_messages, width=40)
        delay_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(delay_frame, text="(Mínimo: 0.05)", font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_button = ttk.Button(button_frame, text="Iniciar", command=self.start_buster)
        self.start_button.pack(side=tk.LEFT, expand=True, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Detener", command=self.stop_buster, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, expand=True, padx=(5, 0))
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Registro de actividad", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=15, width=50, font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para el log
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def open_whatsapp(self):
        if self.whatsapp_opened:
            self.log("WhatsApp Web ya está abierto")
            return
            
        try:
            # Configurar el navegador
            options = webdriver.ChromeOptions()
            options.add_argument('--user-data-dir=C:/Users/Public/WhatsAppBuster')
            options.add_argument('--profile-directory=Default')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.get("https://web.whatsapp.com/")
            
            # Esperar a que el usuario escanee el QR
            self.log("Esperando a que escanees el código QR...")
            wait = WebDriverWait(self.driver, 600)
            
            # Esperar a que se cargue WhatsApp Web
            self.log("WhatsApp Web está listo")
            self.log("Escribe el número de teléfono con código de país")
            self.log("(Ejemplo: +34123456789)")
            
            self.whatsapp_opened = True
            
        except Exception as e:
            self.log(f"Error al abrir WhatsApp Web: {str(e)}")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.whatsapp_opened = False
                    
    def buster_thread(self):
        if not self.whatsapp_opened:
            self.log("Error: WhatsApp Web no está abierto")
            self.stop_buster()
            return
            
        try:
            # Buscar el contacto por número
            self.log("Buscando el número...")
            wait = WebDriverWait(self.driver, 30)
            
            # Esperar a que el campo de búsqueda esté disponible
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
            self.log("Campo de búsqueda encontrado")
            
            # Limpiar el campo de búsqueda y escribir el número
            search_box.clear()
            search_box.send_keys(self.phone_number.get() + Keys.ENTER)
            self.log("Número enviado")
            
            # Verificar que el chat está abierto
            try:
                # Esperar a que el campo de mensaje esté disponible y sea interactivo
                message_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
                self.log("Chat abierto y listo para enviar mensajes")
                
                # Esperar 3 segundos antes de empezar a enviar mensajes
                self.log("Esperando 3 segundos antes de empezar...")
                time.sleep(3)
                self.log("Comenzando envío de mensajes...")
                
                # Enviar mensajes
                total_messages = int(self.total_messages.get())
                delay = float(self.delay_between_messages.get())
                
                for i in range(total_messages):
                    if not self.is_running:
                        break
                        
                    # Usar el mensaje personalizado sin número
                    message = self.custom_message.get()
                    
                    try:
                        # Verificar que el campo de mensaje sigue disponible
                        message_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
                        message_box.send_keys(message)
                        message_box.send_keys(Keys.ENTER)
                        
                        self.successful_messages += 1
                        self.log(f"Mensaje {i + 1} enviado")
                        
                        time.sleep(delay)
                        
                        if (i + 1) % 10 == 0:
                            elapsed_time = (datetime.now() - self.start_time).total_seconds()
                            remaining_time = (total_messages - (i + 1)) * delay
                            self.log(f"\nProgreso: {i + 1}/{total_messages} mensajes")
                            self.log(f"Exitosos: {self.successful_messages}")
                            self.log(f"Tiempo transcurrido: {elapsed_time/60:.2f} minutos")
                            self.log(f"Tiempo restante: {remaining_time/60:.2f} minutos")
                            self.log("=" * 50)
                            
                    except Exception as e:
                        self.log(f"Error al enviar mensaje {i + 1}: {str(e)}")
                        self.log("Intentando continuar con el siguiente mensaje...")
                        time.sleep(2)
                        continue
                        
            except Exception as e:
                self.log(f"Error al verificar el chat: {str(e)}")
                self.log("El chat no se pudo abrir correctamente")
                self.stop_buster()
                return
                    
        except Exception as e:
            self.log(f"Error: {str(e)}")
            self.log("Si el problema persiste, intenta:")
            self.log("1. Cerrar WhatsApp Web y volver a abrirlo")
            self.log("2. Verificar que el número es correcto")
            self.log("3. Asegurarte de que el contacto existe en WhatsApp")
            
        finally:
            self.stop_buster()
            
    def start_buster(self):
        if not self.phone_number.get() or not self.total_messages.get() or not self.delay_between_messages.get() or not self.custom_message.get():
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
            
        # Validar número de teléfono
        phone = self.phone_number.get().strip()
        if not phone.startswith('+'):
            messagebox.showerror("Error", "El número debe empezar con + y código de país")
            return
            
        try:
            int(self.total_messages.get())
            float(self.delay_between_messages.get())
        except ValueError:
            messagebox.showerror("Error", "El número de mensajes debe ser entero y el delay puede ser decimal")
            return
            
        if float(self.delay_between_messages.get()) < 0.05:
            messagebox.showerror("Error", "El delay mínimo es 0.05 segundos")
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.successful_messages = 0
        self.start_time = datetime.now()
        
        self.log("Iniciando WhatsApp Buster...")
        self.log(f"Número objetivo: {self.phone_number.get()}")
        self.log(f"Mensaje: {self.custom_message.get()}")
        self.log(f"Total de mensajes a enviar: {self.total_messages.get()}")
        self.log("Tiempo estimado: {:.2f} minutos".format(
            (int(self.total_messages.get()) * float(self.delay_between_messages.get())) / 60))
        self.log("=" * 50)
        
        # Iniciar el thread del buster
        threading.Thread(target=self.buster_thread, daemon=True).start()
        
    def stop_buster(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.whatsapp_opened = False
                
        if self.start_time:
            total_time = (datetime.now() - self.start_time).total_seconds()
            self.log("\n" + "=" * 50)
            self.log("Resumen final:")
            self.log(f"Mensajes enviados exitosamente: {self.successful_messages}/{self.total_messages.get()}")
            self.log(f"Tiempo total: {total_time/60:.2f} minutos")
            self.log("Programa finalizado")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = WhatsAppBusterGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print("Error al iniciar la aplicación:")
        print(traceback.format_exc())
        input("Presiona Enter para salir...")