

import customtkinter as ctk
from config.settings import color, layout
from gui.login.login_page import LoginPage
from gui.dashboard.dashboard_page import DashboardPage
from backend.database import db

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry(f"{layout['window_width']}x{layout['window_height']}")
        self.window.title("VisionGuard AI")
        self.window.configure(fg_color=color['background'])
        
        # Background effects
        left_bg = ctk.CTkFrame(
            self.window,
            width=500,
            height=500,
            corner_radius=250,
            fg_color="#b9d6ff"
        )
        left_bg.place(x=-180, y=650)
        
        right_bg = ctk.CTkFrame(
            self.window,
            width=450,
            height=450,
            corner_radius=225,
            fg_color="#d8e7ff"
        )
        right_bg.place(x=1100, y=720)
        
        # Pages
        self.login_page = None
        self.dashboard_page = None
        
        self.show_login()
        
        self.window.mainloop()
    
    def show_login(self):
        """Login sayfasını göster"""
        db.logout()
        
        if self.dashboard_page:
            self.dashboard_page.main_frame.pack_forget()
        
        self.login_page = LoginPage(self.window, self.go_to_dashboard)
        self.login_page.main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def go_to_dashboard(self):
        """Dashboard'a git"""
        if self.login_page:
            self.login_page.main_frame.place_forget()
        
        self.dashboard_page = DashboardPage(self.window, self.show_login)
        self.dashboard_page.main_frame.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = App()