
import customtkinter as ctk
from gui.dashboard.settings_tab import SettingsTab
from gui.shared.logs_viewer import LogsViewer
from config.settings import color

class SettingsPage:
    def __init__(self, master, on_logout=None):
        self.master = master
        self.on_logout = on_logout
        
        # Main frame
        self.frame = ctk.CTkFrame(master, fg_color=color['background'])
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            self.frame,
            text="⚙️ Settings",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            self.frame,
            text="System Settings & Logs",
            font=('Arial', 13),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(0, 20))
        
        # Tabs
        tabs_frame = ctk.CTkFrame(self.frame, fg_color='transparent')
        tabs_frame.pack(fill='x', pady=(0, 15))
        
        self.tab_var = ctk.StringVar(value="logs")
        
        self.logs_btn = ctk.CTkButton(
            tabs_frame,
            text="📋 Logs",
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['text'],
            command=lambda: self._switch_tab("logs", self.logs_btn)
        )
        self.logs_btn.pack(side='left', padx=5)
        
        self.account_btn = ctk.CTkButton(
            tabs_frame,
            text="👤 Account",
            fg_color='transparent',
            hover_color='#E8F4FF',
            text_color=color['text'],
            border_width=2,
            border_color=color['border'],
            command=lambda: self._switch_tab("account", self.account_btn)
        )
        self.account_btn.pack(side='left', padx=5)
        
        # Content frame
        self.content_frame = ctk.CTkFrame(
            self.frame,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        self.content_frame.pack(fill='both', expand=True)
        
        # Load logs by default
        self._show_logs()
    
    def _switch_tab(self, tab_name, button):
        """Sekmeyi değiştir"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update button colors
        if tab_name == "logs":
            self.logs_btn.configure(fg_color=color['primary'])
            self.account_btn.configure(fg_color='transparent')
            self._show_logs()
        else:
            self.logs_btn.configure(fg_color='transparent')
            self.account_btn.configure(fg_color=color['primary'])
            self._show_account()
    
    def _show_logs(self):
        """Logları göster"""
        LogsViewer(self.content_frame)
    
    def _show_account(self):
        """Hesap ayarlarını göster"""
        from gui.dashboard.settings_tab import SettingsTab
        SettingsTab(self.content_frame, self.on_logout)
