

import customtkinter as ctk
from config.settings import color, font, layout

class DashboardPage:
    def __init__(self, master, on_logout=None):
        self.master = master
        self.on_logout = on_logout
        
        # Main frame
        self.main_frame = ctk.CTkFrame(
            master,
            fg_color=color['background']
        )
        
        # Sidebar
        self.create_sidebar()
        
        # Content area
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=color['background']
        )
        self.content_frame.pack(side='right', fill='both', expand=True, padx=30, pady=30)
        
        # Pages
        self.pages = {}
        
        self.create_dashboard_page()
        self.create_live_page()
        self.create_records_page()
        self.create_notifications_page()
        self.create_users_page()
        self.create_settings_page()
        self.create_about_page()
        
        # Default: Dashboard
        self.show_page("dashboard")
    
    # ===================================
    # SIDEBAR
    # ===================================
    
    def create_sidebar(self):
        """Sidebar oluştur"""
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            width=250,
            fg_color=color['white'],
            corner_radius=0
        )
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Logo
        ctk.CTkLabel(
            self.sidebar,
            text="🛡 VisionGuard AI",
            font=('Arial', 16, 'bold'),
            text_color=color['primary']
        ).pack(anchor='w', padx=20, pady=(30, 40))
        
        # Menu items
        menus = [
            ("📊 Dasboard", "dashboard"),
            ("📷 Live", "live"),
            ("💾 Records", "records"),
            ("🔔 Notifications", "notifications"),
           # ("👥 Kullanıcı Yönetimi", "users"),
            ("⚙️ Settings", "settings"),
            ("ℹ️ About", "about"),
        ]
        
        for text, page in menus:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45,
                fg_color='transparent',
                hover_color='#E8F4FF',
                text_color=color['text'],
                anchor='w',
                font=('Arial', 12),
                corner_radius=10,
                command=lambda p=page: self.show_page(p)
            )
            btn.pack(fill='x', padx=15, pady=5)
        
        # Exit button
        ctk.CTkButton(
            self.sidebar,
            text="🚪 exist",
            height=45,
            fg_color='#FF6B6B',
            hover_color='#FF5252',
            text_color=color['white'],
            font=('Arial', 12, 'bold'),
            corner_radius=10,
            command=self._handle_logout
        ).pack(side='bottom', fill='x', padx=15, pady=20)
    
    def _handle_logout(self):
        """Çıkış yap"""
        if self.on_logout:
            self.on_logout()
    
    # ===================================
    # PAGE SYSTEM
    # ===================================
    
    def create_page(self, name):
        """Sayfa oluştur"""
        frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=color['background']
        )
        self.pages[name] = frame
        return frame
    
    def show_page(self, name):
        """Sayfayı göster"""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill='both', expand=True)
    
    # ===================================
    # DASHBOARD PAGE
    # ===================================
    
    def create_dashboard_page(self):
        """Dashboard sayfası"""
        page = self.create_page("dashboard")
        
        # Title
        ctk.CTkLabel(
            page,
            text="DASBOARD",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            page,
            text="Smart Motion sistem durumu",
            font=('Arial', 13),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(0, 20))
        
        # Small cards
        cards_frame = ctk.CTkFrame(page, fg_color=color['background'])
        cards_frame.pack(fill='x', pady=(0, 20))
        
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        
        self.create_small_card(cards_frame, 0, "📷 Camera", "4 Active")
        self.create_small_card(cards_frame, 1, "🚨 State", "Active")
        self.create_small_card(cards_frame, 2, "💾 Record", "124")
        
        # Main area
        main_area = ctk.CTkFrame(page, fg_color=color['background'])
        main_area.pack(fill='both', expand=True)
        
        main_area.grid_columnconfigure(0, weight=3)
        main_area.grid_columnconfigure(1, weight=1)
        main_area.grid_rowconfigure(0, weight=1)
        
        # Camera section
        camera = ctk.CTkFrame(
            main_area,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        camera.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        ctk.CTkLabel(
            camera,
            text="📹 LİVE",
            font=('Arial', 28, 'bold'),
            text_color=color['primary']
        ).place(relx=0.5, rely=0.5, anchor='center')
        
        # Info panel
        info_panel = ctk.CTkFrame(
            main_area,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        info_panel.grid(row=0, column=1, sticky='nsew')
        
        ctk.CTkLabel(
            info_panel,
            text="System Information",
            font=('Arial', 18, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 15))
        
        # Control panel
        self.create_control_panel(info_panel)
        
        # Info items
        infos = [
            ("Camera", "Logitech C920"),
            ("Resolution", "640x480"),
            ("FPS", "25 FPS"),
            ("State", "Aktif"),
        ]
        
        for label, value in infos:
            self.create_info_row(info_panel, label, value)
    
    def create_small_card(self, parent, column, title, value):
        """Küçük kart"""
        card = ctk.CTkFrame(
            parent,
            fg_color=color['white'],
            corner_radius=12,
            border_width=1,
            border_color=color['border'],
            height=80
        )
        card.grid(row=0, column=column, sticky='ew', padx=5)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=('Arial', 12),
            text_color=color['text_light']
        ).pack(anchor='w', padx=15, pady=(12, 3))
        
        ctk.CTkLabel(
            card,
            text=value,
            font=('Arial', 18, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15)
    
    def create_control_panel(self, parent):
        """Kontrol paneli"""
        control = ctk.CTkFrame(
            parent,
            fg_color='#F0F8FF',
            corner_radius=12
        )
        control.pack(fill='x', padx=12, pady=(0, 15))
        
        ctk.CTkLabel(
            control,
            text="Controls",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=12, pady=(12, 10))
        
        # Buttons
        buttons = ctk.CTkFrame(control, fg_color='transparent')
        buttons.pack(fill='x', padx=10)
        
        ctk.CTkButton(
            buttons,
            text="▶ Starts",
            height=38,
            fg_color='#45C46B',
            hover_color='#36A856',
            font=('Arial', 11, 'bold'),
            corner_radius=10
        ).pack(side='left', expand=True, fill='x', padx=5)
        
        ctk.CTkButton(
            buttons,
            text="⏹ Stop",
            height=38,
            fg_color='#FF5C5C',
            hover_color='#FF4747',
            font=('Arial', 11, 'bold'),
            corner_radius=10
        ).pack(side='left', expand=True, fill='x', padx=5)
        
        # Slider
        slider_frame = ctk.CTkFrame(control, fg_color='transparent')
        slider_frame.pack(fill='x', padx=12, pady=(12, 12))
        
        ctk.CTkLabel(
            slider_frame,
            text="Sensitivity Settings",
            font=('Arial', 12, 'bold'),
            text_color=color['text']
        ).pack(anchor='w')
        
        slider = ctk.CTkSlider(
            slider_frame,
            from_=0,
            to=100,
            progress_color=color['primary'],
            button_color=color['primary'],
            button_hover_color=color['primary_dark']
        )
        slider.set(70)
        slider.pack(fill='x', pady=(8, 5))
        
        ctk.CTkLabel(
            slider_frame,
            text="%70",
            font=('Arial', 11),
            text_color=color['text_light']
        ).pack(anchor='e')
    
    def create_info_row(self, parent, label, value):
        """Info satırı"""
        row = ctk.CTkFrame(
            parent,
            fg_color='#F0F8FF',
            corner_radius=10,
            height=50
        )
        row.pack(fill='x', padx=12, pady=6)
        
        ctk.CTkLabel(
            row,
            text=label,
            font=('Arial', 12),
            text_color=color['text_light']
        ).pack(side='left', padx=12)
        
        text_color = '#45C46B' if value == "Aktif" else color['text']
        
        ctk.CTkLabel(
            row,
            text=value,
            font=('Arial', 12, 'bold'),
            text_color=text_color
        ).pack(side='right', padx=12)
    
    # ===================================
    # OTHER PAGES
    # ===================================
    
    def create_live_page(self):
        page = self.create_page("live")
        self.simple_page_title(page, "📷 Live")
    
    def create_records_page(self):
        page = self.create_page("records")
        self.simple_page_title(page, "💾 Rcords")
    
    def create_notifications_page(self):
        page = self.create_page("notifications")
        self.simple_page_title(page, "🔔 Notifications")
    
    
    def create_users_page(self):
        page = self.create_page("users")
        self.simple_page_title(page, "👥 Kullanıcı Yönetimi")
    
    def create_settings_page(self):
        #Ayarlar sayfası
        page = self.create_page("settings")
        
        from gui.dashboard.settings_page import SettingsPage
        settings_page = SettingsPage(page, self.on_logout)
    """
    def create_settings_page(self):
       #Ayarlar sayfası
       page = self.create_page("settings")
    
       # SettingsTab'ı doğrudan çağır
       from gui.dashboard.settings_tab import SettingsTab
       SettingsTab(page, self.on_logout)"""
    
    def create_about_page(self):
        page = self.create_page("about")
        self.simple_page_title(page, "ℹ️ About")
    
    def simple_page_title(self, page, text):
        """Basit sayfa başlığı"""
        ctk.CTkLabel(
            page,
            text=text,
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 20))