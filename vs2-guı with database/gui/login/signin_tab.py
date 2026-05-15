

import customtkinter as ctk
from gui.shared.components import TextInputField, Button
from gui.shared.message_box import MessageBox
from backend.database import db
from config.settings import color, font

class SignInTab:
    def __init__(self, master):
        # Main frame
        self.frame = ctk.CTkFrame(master, fg_color=color['white'])
        
        # Scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color=color['white'],
            label_text=""
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=50, pady=(15, 20))
        
        # Title
        ctk.CTkLabel(
            self.scroll_frame,
            text="Sign Up",
            font=('Arial', 34, 'bold'),
            text_color=color['primary']
        ).pack(pady=(0, 15), anchor='w')
        
        # Description
        ctk.CTkLabel(
            self.scroll_frame,
            text="“Fill out the form to create a new account",
            font=font['label'],
            text_color=color['text_light']
        ).pack(pady=(0, 15), anchor='w')
        
        # Inputs
        self.name = TextInputField(self.scroll_frame, "your yousername", icon_text="👤")
        self.email = TextInputField(self.scroll_frame, " e-mail", icon_text="✉")
        self.password = TextInputField(self.scroll_frame, "password", show="*", icon_text="🔒")
        self.password2 = TextInputField(self.scroll_frame, "Please re-enter your password.", show="*", icon_text="🔒")
        
        # Button
        self.signup_btn = Button(self.scroll_frame, "Sign Up", command=self._handle_signup)
        
        # Spacing
        ctk.CTkFrame(self.scroll_frame, fg_color=color['white'], height=50).pack()
    
    def _handle_signup(self):
        """Signup button tıklandığında"""
        username = self.name.get_value()
        email = self.email.get_value()
        password = self.password.get_value()
        password2 = self.password2.get_value()
        
        # Validasyon
        if not username or not email or not password or not password2:
            MessageBox.show_error(
                self.frame.winfo_toplevel(),
                "error",
                "Please fill in all fields."
                #"Tüm alanları doldurunuz"
            )
            return
        
        if password != password2:
            MessageBox.show_error(
                self.frame.winfo_toplevel(),
                "error",
                "the passworrd id not match"
            )
            return
        
        # Database'e kaydet
        success, message = db.register_user(username, email, password)
        
        if success:
            MessageBox.show_success(
                self.frame.winfo_toplevel(),
                "success",
                message
            )
            # Input'ları temizle
            self.name.clear()
            self.email.clear()
            self.password.clear()
            self.password2.clear()
        else:
            MessageBox.show_error(
                self.frame.winfo_toplevel(),
                "error",
                message
            )
