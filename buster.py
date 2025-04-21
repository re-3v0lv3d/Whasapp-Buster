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
from translations import translations

class WhatsAppBusterGUI:
    def __init__(self, root):
        self.root = root
        self.current_language = 'es'  # Idioma por defecto
        self.translations = translations
        self.update_ui()
        
    def update_ui(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title(self.translations[self.current_language]['title'])
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
        
        # Selector de idioma
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(lang_frame, text="Idioma / Language:").pack(side=tk.LEFT, padx=(0, 10))
        self.lang_var = tk.StringVar(value=self.current_language)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=['es', 'en'], state='readonly', width=5)
        lang_combo.pack(side=tk.LEFT)
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        title_label = ttk.Label(title_frame, text=self.translations[self.current_language]['title'], font=("Segoe UI", 24, "bold"))
        title_label.pack()
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text=self.translations[self.current_language]['config_title'], padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botón para abrir WhatsApp Web
        whatsapp_button = ttk.Button(config_frame, text=self.translations[self.current_language]['open_whatsapp'], command=self.open_whatsapp)
        whatsapp_button.pack(fill=tk.X, pady=(0, 15))
        
        # Campos de entrada
        input_frame = ttk.Frame(config_frame)
        input_frame.pack(fill=tk.X)
        
        # Número de teléfono
        phone_frame = ttk.Frame(input_frame)
        phone_frame.pack(fill=tk.X, pady=5)
        ttk.Label(phone_frame, text=self.translations[self.current_language]['phone_label']).pack(side=tk.LEFT, padx=(0, 10))
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_number, width=40)
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(phone_frame, text=self.translations[self.current_language]['phone_example'], font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Mensaje personalizado
        message_frame = ttk.Frame(input_frame)
        message_frame.pack(fill=tk.X, pady=5)
        ttk.Label(message_frame, text=self.translations[self.current_language]['message_label']).pack(side=tk.LEFT, padx=(0, 10))
        message_entry = ttk.Entry(message_frame, textvariable=self.custom_message, width=40)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Total de mensajes
        total_frame = ttk.Frame(input_frame)
        total_frame.pack(fill=tk.X, pady=5)
        ttk.Label(total_frame, text=self.translations[self.current_language]['total_label']).pack(side=tk.LEFT, padx=(0, 10))
        messages_entry = ttk.Entry(total_frame, textvariable=self.total_messages, width=40)
        messages_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Delay entre mensajes
        delay_frame = ttk.Frame(input_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        ttk.Label(delay_frame, text=self.translations[self.current_language]['delay_label']).pack(side=tk.LEFT, padx=(0, 10))
        delay_entry = ttk.Entry(delay_frame, textvariable=self.delay_between_messages, width=40)
        delay_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(delay_frame, text=self.translations[self.current_language]['delay_min'], font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_button = ttk.Button(button_frame, text=self.translations[self.current_language]['start_button'], command=self.start_buster)
        self.start_button.pack(side=tk.LEFT, expand=True, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text=self.translations[self.current_language]['stop_button'], command=self.stop_buster, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, expand=True, padx=(5, 0))
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text=self.translations[self.current_language]['log_title'], padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=15, width=50, font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para el log
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    def change_language(self, event):
        self.current_language = self.lang_var.get()
        self.update_ui()
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def open_whatsapp(self):
        if self.whatsapp_opened:
            self.log(self.translations[self.current_language]['whatsapp_ready'])
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
            self.log(self.translations[self.current_language]['scan_qr'])
            wait = WebDriverWait(self.driver, 600)
            
            # Esperar a que se cargue WhatsApp Web
            self.log(self.translations[self.current_language]['whatsapp_ready'])
            self.log(self.translations[self.current_language]['enter_phone'])
            
            self.whatsapp_opened = True
            
        except Exception as e:
            self.log(self.translations[self.current_language]['error_general'].format(str(e)))
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.whatsapp_opened = False
                    
    def buster_thread(self):
        if not self.whatsapp_opened:
            self.log(self.translations[self.current_language]['error_whatsapp'])
            self.stop_buster()
            return
            
        try:
            # Buscar el contacto por número
            self.log(self.translations[self.current_language]['searching'])
            wait = WebDriverWait(self.driver, 30)
            
            # Esperar a que el campo de búsqueda esté disponible
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
            self.log(self.translations[self.current_language]['search_found'])
            
            # Limpiar el campo de búsqueda y escribir el número
            search_box.clear()
            search_box.send_keys(self.phone_number.get() + Keys.ENTER)
            self.log(self.translations[self.current_language]['number_sent'])
            
            # Verificar que el chat está abierto
            try:
                # Esperar a que el campo de mensaje esté disponible y sea interactivo
                message_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
                self.log(self.translations[self.current_language]['chat_ready'])
                
                # Esperar 3 segundos antes de empezar a enviar mensajes
                self.log(self.translations[self.current_language]['waiting'])
                time.sleep(3)
                self.log(self.translations[self.current_language]['starting'])
                
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
                        self.log(self.translations[self.current_language]['message_sent'].format(i + 1))
                        
                        time.sleep(delay)
                        
                        if (i + 1) % 10 == 0:
                            elapsed_time = (datetime.now() - self.start_time).total_seconds()
                            remaining_time = (total_messages - (i + 1)) * delay
                            self.log(self.translations[self.current_language]['progress'].format(i + 1, total_messages))
                            self.log(self.translations[self.current_language]['successful'].format(self.successful_messages))
                            self.log(self.translations[self.current_language]['elapsed'].format(elapsed_time/60))
                            self.log(self.translations[self.current_language]['remaining'].format(remaining_time/60))
                            self.log("=" * 50)
                            
                    except Exception as e:
                        self.log(self.translations[self.current_language]['error_message_send'].format(i + 1, str(e)))
                        self.log(self.translations[self.current_language]['error_continue'])
                        time.sleep(2)
                        continue
                        
            except Exception as e:
                self.log(self.translations[self.current_language]['error_chat'].format(str(e)))
                self.log(self.translations[self.current_language]['error_chat_open'])
                self.stop_buster()
                return
                    
        except Exception as e:
            self.log(self.translations[self.current_language]['error_general'].format(str(e)))
            self.log(self.translations[self.current_language]['error_troubleshoot'])
            
        finally:
            self.stop_buster()
            
    def start_buster(self):
        if not self.phone_number.get():
            messagebox.showerror("Error", self.translations[self.current_language]['error_phone'])
            return
        if not self.custom_message.get():
            messagebox.showerror("Error", self.translations[self.current_language]['error_message'])
            return
        if not self.total_messages.get():
            messagebox.showerror("Error", self.translations[self.current_language]['error_total'])
            return
        if not self.delay_between_messages.get():
            messagebox.showerror("Error", self.translations[self.current_language]['error_delay'])
            return
            
        # Validar número de teléfono
        phone = self.phone_number.get().strip()
        if not phone.startswith('+'):
            messagebox.showerror("Error", self.translations[self.current_language]['error_invalid_phone'])
            return
            
        try:
            int(self.total_messages.get())
            float(self.delay_between_messages.get())
        except ValueError:
            messagebox.showerror("Error", self.translations[self.current_language]['error_invalid_numbers'])
            return
            
        if float(self.delay_between_messages.get()) < 0.05:
            messagebox.showerror("Error", self.translations[self.current_language]['error_min_delay'])
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
            self.log(self.translations[self.current_language]['summary'])
            self.log(self.translations[self.current_language]['summary_messages'].format(self.successful_messages, self.total_messages.get()))
            self.log(self.translations[self.current_language]['summary_time'].format(total_time/60))
            self.log(self.translations[self.current_language]['finished'])

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