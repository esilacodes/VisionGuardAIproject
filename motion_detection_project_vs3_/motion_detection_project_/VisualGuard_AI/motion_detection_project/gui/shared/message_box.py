import customtkinter as ctk
from config.settings import color

class MessageBox:
    """Error/Başarı mesaj kutusu"""
    
    @staticmethod
    def show_error(parent, title, message):
        """Error mesajı göster"""
        MessageBox._show_message(parent, title, message, "error")
    
    @staticmethod
    def show_success(parent, title, message):
        """Başarı mesajı göster"""
        MessageBox._show_message(parent, title, message, "success")
    
    @staticmethod
    def _show_message(parent, title, message, msg_type):
        """Mesaj göster"""
        # Pop-up window
        popup = ctk.CTkToplevel(parent)
        popup.title(title)
        popup.geometry("400x150")
        popup.resizable(False, False)
        
        # Icon
        icon = "❌" if msg_type == "error" else "✅"
        icon_color = "#FF5C5C" if msg_type == "error" else "#45C46B"
        
        ctk.CTkLabel(
            popup,
            text=icon,
            font=('Arial', 32),
            text_color=icon_color
        ).pack(pady=(15, 5))
        
        # Message
        ctk.CTkLabel(
            popup,
            text=message,
            font=('Arial', 12),
            text_color=color['text'],
            wraplength=350
        ).pack(pady=(5, 15))
        
        # OK button
        ctk.CTkButton(
            popup,
            text="okey",
            width=100,
            height=35,
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=popup.destroy
        ).pack(pady=(0, 15))
        
        # Center window
        popup.transient(parent)
        popup.grab_set()