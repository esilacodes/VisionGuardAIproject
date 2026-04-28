
# ui/main_panel.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from config import (
    BUTTON_FONT, BUTTON_COLOR, BUTTON_TEXT_COLOR,
    LABEL_FONT, TITLE_FONT, BUTTON_WIDTH
)
from ui.basewindow import BaseWindow

class MainPanel(BaseWindow):
    
    
    def __init__(self):
        super().__init__(title="Motion Detection - Main Panel", width=1000, height=700)
        self.is_running = False
        self.current_sensitivity = 50
        #camera  self.camera=None ,self.is_runnig=false

        self.create_widgets()
    
    def create_widgets(self):
    
        
        # main frame
        main_frame = tk.Frame(self, bg=self.background_color)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Başlık
        title_label = tk.Label(
            main_frame,
            text="Motion Detection System",
            font=TITLE_FONT,
            bg=self.background_color,
            fg="#333333"
        )
        title_label.pack(pady=10)
        
        # ============================================
        # ÜSTTEKI FRAME (camera + Log)
        # ============================================
        top_frame = tk.Frame(main_frame, bg=self.background_color)
        top_frame.pack(pady=5, padx=5, fill="both", expand=True)
        
        # ---- SOL TARAF: KAMERA FRAME ----
        camera_frame = tk.Frame(top_frame, bg="black", height=300)
        camera_frame.pack(side="left", pady=5, padx=5, fill="both", expand=True)
        camera_frame.pack_propagate(False)
        
        # Kamera label
        self.camera_label = tk.Label(
            camera_frame,
            text="Camera Feed Here",
            font=("Arial", 16),
            fg="white",
            bg="black"
        )
        self.camera_label.pack(expand=True)
        """
       
        """
        # ---- SAĞ TARAF: LOG PANEL ----
        log_frame = tk.Frame(top_frame, bg=self.background_color, width=280)
        log_frame.pack(side="right", pady=5, padx=5, fill="y")
        log_frame.pack_propagate(False)  # Width sabit kalsın

        log_label = tk.Label(
           log_frame,
           text="System Logs:",
           font=LABEL_FONT,
           bg=self.background_color,
           fg="#333333"
            )
        log_label.pack(anchor="w", padx=5, pady=2)

        # Log Text Widget
        self.log_text = tk.Text(
              log_frame,
                height=20,
         width=35,
           font=("Courier", 8),
           bg="white",
          fg="#333333"
         )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=2)

        self.display_log("System initialized...")
        # ============================================
        # ALTTAKİ FRAME (Butonlar + Slider)
        # ============================================
        control_frame = tk.Frame(main_frame, bg=self.background_color)
        control_frame.pack(pady=10, padx=5, fill="x")
        
        # Butonlar kısmı (solda)
        buttons_frame = tk.Frame(control_frame, bg=self.background_color)
        buttons_frame.pack(side="left", padx=5, pady=5)
        
        # Start Button
        self.start_button = tk.Button(
            buttons_frame,
            text="START",
            font=BUTTON_FONT,
            bg="#4CAF50",
            fg=BUTTON_TEXT_COLOR,
            width=10,
            height=2,
            command=self.on_start_button_clicked
        )
        self.start_button.pack(side="left", padx=5, pady=5)
        
        # Stop Button
        self.stop_button = tk.Button(
            buttons_frame,
            text="STOP",
            font=BUTTON_FONT,
            bg="#FF5252",
            fg=BUTTON_TEXT_COLOR,
            width=10,
            height=2,
            command=self.on_stop_button_clicked,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5, pady=5)
        
        # Slider kısmı (sağda)
        slider_frame = tk.Frame(control_frame, bg=self.background_color)
        slider_frame.pack(side="right", padx=20, pady=5, fill="x", expand=True)
        
        sensitivity_label = tk.Label(
            slider_frame,
            text="Sensitivity:",
            font=LABEL_FONT,
            bg=self.background_color,
            fg="#333333"
        )
        sensitivity_label.pack(anchor="w", padx=5, pady=2)
        
        self.sensitivity_slider = tk.Scale(
            slider_frame,
            from_=1,
            to=100,
            orient="horizontal",
            command=self.on_slider_changed,
            bg=self.background_color,
            fg="#333333",
            length=300
        )
        self.sensitivity_slider.set(self.current_sensitivity)
        self.sensitivity_slider.pack(fill="x", padx=5, pady=5)
    
    def on_start_button_clicked(self):
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.display_log("✓ Camera started...")
        #messagebox.showinfo("Kamera", "Kamera çalışıyor!")
    
    def on_stop_button_clicked(self):
        
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.display_log("✓ Camera stopped...")
        #messagebox.showinfo("Kamera", "Kamera durduruldu!")
    
    def on_slider_changed(self, value):
    
        self.current_sensitivity = int(value)
        self.display_log(f"→ Sensitivity: {self.current_sensitivity}")
    
    def display_log(self, message):
        """Log paneline mesaj ekle"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

"""
#cameryı bagladıktan sonra var sayalı 
 def on_start_button_clicked(self):
        Start butonuna tıklandığında
        try:
            self.camera = cv2.VideoCapture(0)  # Kamerayı aç
            
            if not self.camera.isOpened():
                messagebox.showerror("Hata", "Kamera açılamadı!")
                self.display_log("✗ Camera failed to open")
                return
            
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.display_log("✓ Camera started...")
            
            # Kamera frame'lerini göster
            self.show_camera_frame()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kamera hatası: {str(e)}")
            self.display_log(f"✗ Camera error: {str(e)}")
    
    def on_stop_button_clicked(self):
          Stop butonuna tıklandığında
        self.is_running = False
        
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.display_log("✓ Camera stopped...")
        
        # Label'ı sıfırla
        self.camera_label.config(text="Camera Feed Here", image="")
    
    def on_slider_changed(self, value):
        Slider değiştiğinde
        self.current_sensitivity = int(value)
        self.display_log(f"→ Sensitivity: {self.current_sensitivity}")
    
    def show_camera_frame(self):
        Kamera frame'ini göster (recursive)
        
        if not self.is_running or self.camera is None:
            return
        
        try:
            # Frame oku
            ret, frame = self.camera.read()
            
            if ret:
                # Frame'i küçült
                frame = cv2.resize(frame, (640, 480))
                
                # BGR'yi RGB'ye çevir
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # PIL Image'e çevir
                image = Image.fromarray(frame_rgb)
                
                # Tkinter PhotoImage'e çevir
                photo_image = ImageTk.PhotoImage(image=image)
                
                # Label'ı güncelle
                self.camera_label.config(image=photo_image, text="")
                self.camera_label.image = photo_image  # Referansı tut!
        
        except Exception as e:
            self.display_log(f"✗ Error: {str(e)}")
            self.is_running = False
            return
        
        # 30ms sonra tekrar çağır (30 FPS)
        if self.is_running:
            self.after(30, self.show_camera_frame)
    
    def display_log(self, message):
        Log paneline mesaj ekle
        log_entry = self.logger.log_message(message)
        self.log_text.insert("end", f"{log_entry}\n")
        self.log_text.see("end")

        

from PIL import Image, ImageTk
import cv2        
"""
