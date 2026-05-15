
import customtkinter as ctk
from gui.dashboard.settings_tab import SettingsTab
from config.settings import color

class SettingsPage:
    def __init__(self, master, on_logout=None):
        self.master = master
        self.on_logout = on_logout
        
        # Main frame
        self.frame = ctk.CTkFrame(master, fg_color=color['background'])
        self.frame.pack(fill='both', expand=True)
        
        # Settings tab
        self.settings_tab = SettingsTab(self.frame, on_logout)