
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from gui.login.login_tab import LoginTab
from gui.login.signin_tab import SignInTab
from config.settings import color, font, layout
from gui.shared.message_box import MessageBox

class LoginPage:
    def __init__(self, master, on_login_success=None):
        self.master = master
        self.on_login_success = on_login_success
        
        # Main card
        self.main_frame = ctk.CTkFrame(
            master,
            width=950,
            height=760,
            fg_color=color['white'],
            corner_radius=layout['border_radius'],
            border_width=1,
            border_color=color['border']
        )
        
        # Logo
        try:
            from customtkinter import CTkImage
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            logo_img = Image.open(logo_path).resize((120, 120), Image.Resampling.LANCZOS)
            logo_photo = CTkImage(light_image=logo_img, dark_image=logo_img, size=(120, 120))
            
            logo_label = ctk.CTkLabel(
                self.main_frame,
                image=logo_photo,
                text=""
            )
            logo_label.image = logo_photo
            logo_label.place(x=415, y=35)
        except:
            logo_frame = ctk.CTkFrame(
                self.main_frame,
                width=120,
                height=120,
                corner_radius=60,
                fg_color=color['primary']
            )
            logo_frame.place(x=415, y=35)
        
        # Title
        ctk.CTkLabel(
            self.main_frame,
            text="VisionGuard AI",
            font=font['title'],
            text_color=color['text']
        ).place(x=210, y=180)
        
        # Form frame
        self.form_frame = ctk.CTkFrame(
            self.main_frame,
            width=760,
            height=750,
            fg_color=color['white'],
            corner_radius=25,
            border_width=1,
            border_color=color['border']
        )
        self.form_frame.place(x=95, y=260)
        
        # Tab frame
        self.tab_frame = ctk.CTkFrame(
            self.form_frame,
            width=760,
            height=85,
            fg_color=color['tab_bg'],
            corner_radius=18,
            border_width=1,
            border_color=color['border']
        )
        self.tab_frame.pack(fill='x', padx=0, pady=(0, 0))
        
        # Tabs
        self.login_tab = LoginTab(self.form_frame, self.on_login_success)
        self.signin_tab = SignInTab(self.form_frame)
        
        self.login_tab.frame.pack(fill='both', expand=True)
        self.signin_tab.frame.pack_forget()
        
        # Login button
        self.login_btn = ctk.CTkButton(
            self.tab_frame,
            text="Login",
            width=380,
            height=85,
            fg_color=color['tab_bg'],
            hover_color=color['tab_bg'],
            text_color=color['primary'],
            font=font['form_title'],
            corner_radius=18,
            command=self._show_login,
            border_width=0
        )
        self.login_btn.place(x=380, y=0)
        
        # Signin button
        self.signin_btn = ctk.CTkButton(
            self.tab_frame,
            text="Sign up",
            width=380,
            height=85,
            fg_color=color['tab_bg'],
            hover_color=color['tab_bg'],
            text_color=color['text_light'],
            font=font['form_title'],
            corner_radius=18,
            command=self._show_signin,
            border_width=0
        )
        self.signin_btn.place(x=0, y=0)
        
        # Link command
        self.login_tab.signup_link.bind("<Button-1>", lambda e: self._show_signin())
    
    def _show_login(self):
        """Login tab göster"""
        self.login_tab.frame.pack(fill='both', expand=True)
        self.signin_tab.frame.pack_forget()
        
        self.login_btn.configure(text_color=color['primary'])
        self.signin_btn.configure(text_color=color['text_light'])
    
    def _show_signin(self):
        """Signin tab göster"""
        self.login_tab.frame.pack_forget()
        self.signin_tab.frame.pack(fill='both', expand=True)
        
        self.signin_btn.configure(text_color=color['primary'])
        self.login_btn.configure(text_color=color['text_light'])