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
            ("📊 Dashboard", "dashboard"),
            ("📷 Live", "live"),
            ("💾 Records", "records"),
            ("🔔 Notifications", "notifications"),
           
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
            text="🚪 Exit",
            height=45,
            fg_color='#FF6B6B',
            hover_color='#FF5252',
            text_color=color['white'],
            font=('Arial', 12, 'bold'),
            corner_radius=10,
            command=self._handle_logout
        ).pack(side='bottom', fill='x', padx=15, pady=20)
    
    def _handle_logout(self):
        """Logout yap"""
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
        """Sayfayı göster ve gerekirse refresh yap"""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill='both', expand=True)
        
        # Records sayfasını her açışta yenile
        if name == "records":
            if hasattr(self, 'records_content'):
                for widget in self.records_content.winfo_children():
                    widget.destroy()
                self._load_detections_view()
 
        # Notifications sayfasını her açışta yenile
        if name == "notifications":
            if hasattr(self, 'notifications_scrollable'):
                for widget in self.notifications_scrollable.winfo_children():
                    widget.destroy()
                self._load_notifications()
    
    # ===================================
    # DASHBOARD PAGE
    # ===================================
    
    def create_dashboard_page(self):
        """Dashboard sayfası - Sekmeli yapı kaldırıldı, bilgi ve kontrol paneli yan tarafta"""
        page = self.create_page("dashboard")
        
        # Title
        ctk.CTkLabel(
            page,
            text="📊 Dashboard",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            page,
            text="Camera Control and Status Summary",
            font=('Arial', 13),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(0, 20))
        
        # Ana container - grid ile kesin boyut kontrolü
        main_container = ctk.CTkFrame(page, fg_color='transparent')
        main_container.pack(fill='both', expand=True)
        main_container.grid_columnconfigure(0, weight=1)   # sol (kamera) genişler
        main_container.grid_columnconfigure(1, weight=0)   # sağ (kontrol) sabit
        main_container.grid_rowconfigure(0, weight=1)

        # ============================================
        # SOL TARAF - KAMERA VE BİLGİLER
        # ============================================
        left_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        left_frame.grid_rowconfigure(0, weight=1)   # kamera genişler
        left_frame.grid_rowconfigure(1, weight=0)   # bilgi kartları sabit
        left_frame.grid_columnconfigure(0, weight=1)

        # Camera görüntüsü
        camera_frame = ctk.CTkFrame(
            left_frame,
            fg_color=color['white'],
            corner_radius=15,
            border_width=2,
            border_color=color['primary']
        )
        camera_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 10))

        self.dashboard_camera_label = ctk.CTkLabel(
            camera_frame,
            text="📹 Camera view",
            font=('Arial', 24, 'bold'),
            text_color=color['text_light']
        )
        self.dashboard_camera_label.pack(fill='both', expand=True)

        # Bilgi kartları - kameranın altında sabit
        info_container = ctk.CTkFrame(left_frame, fg_color='transparent')
        info_container.grid(row=1, column=0, sticky='ew')
        
        # Camera Durumu
        camera_status_card = ctk.CTkFrame(
            info_container,
            fg_color='#F0F8FF',
            corner_radius=12
        )
        camera_status_card.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(
            camera_status_card,
            text="🎥 Camera State",
            font=('Arial', 12, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=12, pady=(10, 5))
        
        self.dashboard_camera_status = ctk.CTkLabel(
            camera_status_card,
            text="● Closed",
            font=('Arial', 14, 'bold'),
            text_color='#FF5C5C'
        )
        self.dashboard_camera_status.pack(anchor='w', padx=12, pady=(0, 10))
        
        # Toplam Record Sayısı
        records_card = ctk.CTkFrame(
            info_container,
            fg_color='#FFF8F0',
            corner_radius=12
        )
        records_card.pack(fill='x')
        
        ctk.CTkLabel(
            records_card,
            text="💾 Total Record",
            font=('Arial', 12, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=12, pady=(10, 5))
        
        self.dashboard_total_records = ctk.CTkLabel(
            records_card,
            text="0 Detected",
            font=('Arial', 14, 'bold'),
            text_color='#45C46B'
        )
        self.dashboard_total_records.pack(anchor='w', padx=12, pady=(0, 10))
        
        # ============================================
        # SAĞ TARAF - KONTROL PANELİ
        # ============================================
        right_frame = ctk.CTkFrame(main_container, fg_color='transparent', width=280)
        right_frame.grid(row=0, column=1, sticky='ns')
        right_frame.grid_propagate(False)
        
        # Kontrol paneli başlığı
        control_header = ctk.CTkFrame(right_frame, fg_color='transparent')
        control_header.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(
            control_header,
            text="🎮 Control Panel",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w')
        
        # Durum göstergesi
        status_card = ctk.CTkFrame(
            right_frame,
            fg_color='#F0F8FF',
            corner_radius=10
        )
        status_card.pack(fill='x', pady=(0, 12))
        
        ctk.CTkLabel(
            status_card,
            text="State",
            font=('Arial', 10, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=10, pady=(8, 3))
        
        self.dashboard_status_label = ctk.CTkLabel(
            status_card,
            text="● Ready",
            font=('Arial', 11, 'bold'),
            text_color='#45C46B'
        )
        self.dashboard_status_label.pack(anchor='w', padx=10, pady=(0, 8))
        
        # Start/Stop Butonları
        button_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        button_frame.pack(fill='x', pady=(0, 12))
        
        self.dashboard_start_btn = ctk.CTkButton(
            button_frame,
            text="▶ Start",
            height=40,
            fg_color='#45C46B',
            hover_color='#36A856',
            font=('Arial', 11, 'bold'),
            command=self._dashboard_start_camera
        )
        self.dashboard_start_btn.pack(fill='x', pady=(0, 8))
        
        self.dashboard_stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹ Stop",
            height=40,
            fg_color='#FF5C5C',
            hover_color='#FF4747',
            font=('Arial', 11, 'bold'),
            command=self._dashboard_stop_camera,
            state='disabled'
        )
        self.dashboard_stop_btn.pack(fill='x')
        
        # Sensitivity Settingı
        sensitivity_card = ctk.CTkFrame(
            right_frame,
            fg_color='#FFF8F0',
            corner_radius=10
        )
        sensitivity_card.pack(fill='x', pady=(0, 12))
        
        ctk.CTkLabel(
            sensitivity_card,
            text="Sensitivity",
            font=('Arial', 10, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=10, pady=(8, 5))
        
        self.dashboard_sensitivity = ctk.CTkSlider(
            sensitivity_card,
            from_=0,
            to=100,
            progress_color=color['primary'],
            button_color=color['primary'],
            button_hover_color=color['primary_dark'],
            height=6
        )
        self.dashboard_sensitivity.set(70)
        self.dashboard_sensitivity.pack(fill='x', padx=10, pady=(0, 5))
        
        self.dashboard_sensitivity_label = ctk.CTkLabel(
            sensitivity_card,
            text="70%",
            font=('Arial', 10, 'bold'),
            text_color=color['text'],
        )
        self.dashboard_sensitivity_label.pack(anchor='e', padx=10, pady=(0, 8))
        
        self.dashboard_sensitivity.configure(
            command=lambda v: self._update_dashboard_sensitivity(v)
        )
        
        # Bilgi Kartı
        info_card = ctk.CTkFrame(
            right_frame,
            fg_color='#F0FFF8',
            corner_radius=10
        )
        info_card.pack(fill='both', expand=True, pady=(0, 0))
        
        ctk.CTkLabel(
            info_card,
            text="ℹ️ information",
            font=('Arial', 10, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=10, pady=(8, 5))
        
        self.dashboard_info_text = ctk.CTkLabel(
            info_card,
            text="Camera off.\nMotion detection is ready.",
            font=('Arial', 9),
            text_color=color['text_light'],
            justify='left'
        )
        self.dashboard_info_text.pack(anchor='nw', padx=10, pady=(0, 8), fill='both', expand=True)
    
    def _update_dashboard_sensitivity(self, value):
        """Sensitivity slider'ını güncelle"""
        from backend.log_manager import log_manager
        from backend.database import db
        self.dashboard_sensitivity_label.configure(text=f"{int(float(value))}%")
        # Live sekmesi ile senkronize et
        if hasattr(self, 'sensitivity_slider'):
            self.sensitivity_slider.set(float(value))
            self.sensitivity_label.configure(text=f"{int(float(value))}%")
        # Log sensitivity change
        log_manager.log_system_event(
            "info",
            f"Sensitivity changed to {int(float(value))}%",
            username=db.current_user
        )
    
    def _update_live_sensitivity(self, value):
        """Live sekmesi sensitivity slider güncelle + log"""
        from backend.log_manager import log_manager
        from backend.database import db
        self.sensitivity_label.configure(text=f"{int(float(value))}%")
        # Dashboard slider ile senkronize et
        if hasattr(self, 'dashboard_sensitivity'):
            self.dashboard_sensitivity.set(float(value))
            self.dashboard_sensitivity_label.configure(text=f"{int(float(value))}%")
        # Log sensitivity change
        log_manager.log_system_event(
            "info",
            f"Sensitivity changed to {int(float(value))}%",
            username=db.current_user
        )

    def _dashboard_start_camera(self):
        """Dashboard'dan kamera başlat (Live sekmesi ile senkronize)"""
        # Live sekmesindeki start butonunun komutunu çağır
        self._start_motion_detection()
        # Dashboard kontrol panelini güncelle
        self.dashboard_start_btn.configure(state='disabled')
        self.dashboard_stop_btn.configure(state='normal')
        self.dashboard_status_label.configure(text="● Running", text_color='#45C46B')
        self.dashboard_camera_label.configure(text="📹 Camera Active\nWaiting for motion...")
        self.dashboard_camera_status.configure(text="● Running", text_color='#45C46B')
        self.dashboard_info_text.configure(text="Camera Active.\nMotion detection in progress…")
    
    def _dashboard_stop_camera(self):
        """Dashboard'dan kamera durdur (Live sekmesi ile senkronize)"""
        # Live sekmesindeki stop butonunun komutunu çağır
        self._stop_motion_detection()
        # Dashboard kontrol panelini güncelle
        self.dashboard_start_btn.configure(state='normal')
        self.dashboard_stop_btn.configure(state='disabled')
        self.dashboard_status_label.configure(text="● Ready", text_color='#FF9500')
        self.dashboard_camera_label.configure(text="📹 Camera off")
        self.dashboard_camera_status.configure(text="● Closed", text_color='#FF5C5C')
        self.dashboard_info_text.configure(text="Camera off.\nPress Start to begin.")
    def _get_records_stats(self):
        """Get records statistics"""
        from backend.database import db
        
        detections = db.get_detections()
        total = len(detections) if detections else 0
        
        camera_status = "🔴 Closed" if not self.is_detecting else "🟢 Running"
        sensitivity = int(self.sensitivity_slider.get()) if hasattr(self, 'sensitivity_slider') else 70
        
        return f"""
📷 Total Detections: {total}
🎥 Camera: {camera_status}
📊 Sensitivity: {sensitivity}%
        """.strip()
    
    def _create_dashboard_record_item(self, parent, detection_id, timestamp):
        """Dashboard kayıt öğesi oluştur"""
        item = ctk.CTkFrame(
            parent,
            fg_color='#F0F8FF',
            corner_radius=10,
            height=60
        )
        item.pack(fill='x', pady=6)
        
        # Sol taraf - bilgi
        left = ctk.CTkFrame(item, fg_color='transparent')
        left.pack(side='left', padx=12, pady=10, fill='both', expand=True)
        
        ctk.CTkLabel(
            left,
            text=f"📷 Detection", ## #{detection_id}
            font=('Arial', 11, 'bold'),
            text_color=color['text']
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            left,
            text=f"⏰ {timestamp}",
            font=('Arial', 10),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(2, 0))
        
        # Sağ taraf - buton
        ctk.CTkButton(
            item,
            text="👁 Show",
            width=80,
            height=30,
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            font=('Arial', 10, 'bold'),
            command=lambda: self._show_full_image(detection_id)
        ).pack(side='right', padx=12, pady=10)
    def _create_dashboard_notification_item(self, parent, notif_id, detection_id, message, sent_at):
        """Create dashboard notification item"""
        item = ctk.CTkFrame(
            parent,
            fg_color='#FFF8F0',
            corner_radius=10,
            height=70
        )
        item.pack(fill='x', pady=6)
        
        # Sol taraf - bilgi
        left = ctk.CTkFrame(item, fg_color='transparent')
        left.pack(side='left', padx=12, pady=10, fill='both', expand=True)
        
        ctk.CTkLabel(
            left,
            text=f"🔔 {message}",
            font=('Arial', 11, 'bold'),
            text_color=color['text']
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            left,
            text=f"⏰ {sent_at}",
            font=('Arial', 10),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(2, 0))
        
        # Sağ taraf - buton
        if detection_id:
            ctk.CTkButton(
                item,
                text="📷 View Image",
                width=90,
                height=30,
                fg_color='#FF9500',
                hover_color='#E88000',
                text_color=color['white'],
                font=('Arial', 10, 'bold'),
                command=lambda: self._show_full_image(detection_id)
            ).pack(side='right', padx=12, pady=10)

    def create_live_page(self):
        """Live kamera sayfası"""
        page = self.create_page("live")

        # Title
        ctk.CTkLabel(
            page,
            text="📷 Live",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 10))

        ctk.CTkLabel(
            page,
            text="Live Camera Feed",
            font=('Arial', 13),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(0, 10))

        # Control panel - ÖNCE pack et, alta sabit kalsın
        control_panel = ctk.CTkFrame(
            page,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        control_panel.pack(side='bottom', fill='x', pady=(10, 0))

        # Camera display - control panel'den kalan alanı kullan
        camera_frame = ctk.CTkFrame(
            page,
            fg_color=color['white'],
            corner_radius=15,
            border_width=2,
            border_color=color['primary']
        )
        camera_frame.pack(fill='both', expand=True, pady=(0, 10))

        self.camera_label = ctk.CTkLabel(
            camera_frame,
            text="📹 Camera Connecting...",
            font=('Arial', 24, 'bold'),
            text_color=color['text_light']
        )
        self.camera_label.pack(fill='both', expand=True)
        
        ctk.CTkLabel(
            control_panel,
            text="🎮 Control Panel",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Status
        status_frame = ctk.CTkFrame(
            control_panel,
            fg_color='#F0F8FF',
            corner_radius=10
        )
        status_frame.pack(fill='x', padx=12, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="State",
            font=('Arial', 12, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=12, pady=(10, 5))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="● Ready",
            font=('Arial', 11),
            text_color='#45C46B'
        )
        self.status_label.pack(anchor='w', padx=12, pady=(0, 10))
        
        # Buttons and Sensitivity - Aynı satırda
        control_frame = ctk.CTkFrame(control_panel, fg_color='transparent')
        control_frame.pack(fill='x', padx=12, pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
        button_frame.pack(side='left', fill='x', expand=False)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="▶ Start",
            width=100,
            height=35,
            fg_color='#45C46B',
            hover_color='#36A856',
            font=('Arial', 10, 'bold'),
            corner_radius=10,
            command=self._start_motion_detection
        )
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹ Stop",
            width=100,
            height=35,
            fg_color='#FF5C5C',
            hover_color='#FF4747',
            font=('Arial', 10, 'bold'),
            corner_radius=10,
            command=self._stop_motion_detection,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)
        
        # Sensitivity
        sensitivity_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
        sensitivity_frame.pack(side='right', fill='x', expand=True)
        
        ctk.CTkLabel(
            sensitivity_frame,
            text="Sensitivity:",
            font=('Arial', 11, 'bold'),
            text_color=color['text']
        ).pack(side='left', padx=(20, 10))
        
        self.sensitivity_slider = ctk.CTkSlider(
            sensitivity_frame,
            from_=0,
            to=100,
            progress_color=color['primary'],
            button_color=color['primary'],
            button_hover_color=color['primary_dark'],
            width=200
        )
        self.sensitivity_slider.set(70)
        self.sensitivity_slider.pack(side='left', fill='x', expand=True, padx=5)
        
        self.sensitivity_label = ctk.CTkLabel(
            sensitivity_frame,
            text="70%",
            font=('Arial', 11),
            text_color=color['text_light'],
            width=40
        )
        self.sensitivity_label.pack(side='left', padx=(10, 0))
        
        self.sensitivity_slider.configure(
            command=lambda v: self._update_live_sensitivity(v)
        )
        
        # Initialize flags
        self.is_detecting = False
 
 
    def create_records_page(self):
        page = self.create_page("records")
        
        # Title
        ctk.CTkLabel(
            page,
            text="💾 Records",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            page,
            text="Recorded Notifications",
            font=('Arial', 13),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(0, 20))
        
        # Create tabs
        tabs_frame = ctk.CTkFrame(page, fg_color='transparent')
        tabs_frame.pack(fill='x', pady=(0, 15))
        
        self.records_tab = ctk.StringVar(value="detections")
        
        ctk.CTkButton(
            tabs_frame,
            text="📷 Refresh",
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            command=lambda: self._show_records_tab("detections")
        ).pack(side='left', padx=5)
        
        self.records_content = ctk.CTkFrame(
            page,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        self.records_content.pack(fill='both', expand=True)
        
        # Load detections by default
        self._load_detections_view()
    
    def create_notifications_page(self):
        page = self.create_page("notifications")
        
        # Title
        ctk.CTkLabel(
            page,
            text="🔔 Notifications",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 10))
        
        ctk.CTkLabel(
            page,
            text="Sent Notifications",
            font=('Arial', 13),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(0, 20))
        
        # Scrollable frame
        self.notifications_scrollable = ctk.CTkScrollableFrame(
            page,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        self.notifications_scrollable.pack(fill='both', expand=True)
        
        # Logları yükleme show_page() zamanında yapılacak
        # İlk açılışta boş bırak
 
 
    def create_users_page(self):
        page = self.create_page("users")
        self.simple_page_title(page, "👥 User Setting")
    
    def create_settings_page(self):
        #Settings sayfası
        page = self.create_page("settings")
        
        from gui.dashboard.settings_page import SettingsPage
        settings_page = SettingsPage(page, self.on_logout)
    
    
    def create_about_page(self):
        page = self.create_page("about")
        
        # Scrollable content
        scroll = ctk.CTkScrollableFrame(page, fg_color='transparent')
        scroll.pack(fill='both', expand=True)
        
        # Logo/Title
        ctk.CTkLabel(
            scroll,
            text="🛡️ VisionGuard AI",
            font=('Arial', 32, 'bold'),
            text_color=color['primary']
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            scroll,
            text="Smart Motion Detection System",
            font=('Arial', 14),
            text_color=color['text_light']
        ).pack(pady=(0, 30))
        
        # About Card
        about_card = ctk.CTkFrame(
            scroll,
            fg_color=color['white'],
            corner_radius=12,
            border_width=1,
            border_color=color['border']
        )
        about_card.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            about_card,
            text="About",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        about_text = """VisionGuard AI is a smart system that monitors your environment 24/7 using artificial intelligence and image processing technologies
        , detects motion,
          and sends security notifications.

Your data is securely stored and processed using advanced encryption technology.."""
        
        ctk.CTkLabel(
            about_card,
            text=about_text,
            font=('Arial', 11),
            text_color=color['text_light'],
            wraplength=400,
            justify='left'
        ).pack(anchor='w', padx=15, pady=(0, 15))
        
        # Features Card
        features_card = ctk.CTkFrame(
            scroll,
            fg_color='#F0F8FF',
            corner_radius=12,
            border_width=1,
            border_color=color['border']
        )
        features_card.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            features_card,
            text="📋 Core Features",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        features = [
           ("📷", "Live Motion Detection", "Real-time camera monitoring"),
           ("🔐", "AES-256 Encryption", "Secure data storage"),
           ("📦", "LZMA Compression", "Up to 70% file size reduction"),
           ("🔔", "Notification System", "Instant alerts when motion is detected"),
           ("💾", "Detailed Records", "Encrypted logging system"),
           ("🎨", "Modern Interface", "User-friendly design")
        ]
        
        for icon, title, desc in features:
            feature_item = ctk.CTkFrame(features_card, fg_color='transparent')
            feature_item.pack(fill='x', padx=15, pady=5)
            
            ctk.CTkLabel(
                feature_item,
                text=f"{icon} {title}",
                font=('Arial', 11, 'bold'),
                text_color=color['text']
            ).pack(anchor='w')
            
            ctk.CTkLabel(
                feature_item,
                text=f"   {desc}",
                font=('Arial', 10),
                text_color=color['text_light']
            ).pack(anchor='w')
        
        # Tech Stack Card
        tech_card = ctk.CTkFrame(
            scroll,
            fg_color='#FFF8F0',
            corner_radius=12,
            border_width=1,
            border_color=color['border']
        )
        tech_card.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            tech_card,
            text="🔧 Tech Used",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        tech_items = [
           ("Python 3.13+", "Main programming language"),
           ("CustomTkinter", "Modern UI framework"),
           ("SQLite3", "Database management"),
           ("OpenCV", "Image processing"),
           ("Cryptography", "Encryption and security"),
            ("LZMA", "Data compression")
        ]
        
        for tech, desc in tech_items:
            tech_item = ctk.CTkFrame(tech_card, fg_color='transparent')
            tech_item.pack(fill='x', padx=15, pady=3)
            
            ctk.CTkLabel(
                tech_item,
                text=f"▪ {tech}",
                font=('Arial', 11, 'bold'),
                text_color=color['text']
            ).pack(anchor='w')
        
        # Version Card
        version_card = ctk.CTkFrame(
            scroll,
            fg_color='#F0FFF8',
            corner_radius=12,
            border_width=1,
            border_color=color['border']
        )
        version_card.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            version_card,
            text="ℹ️ Version Information",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        version_items = [
           ("App Name", "VisionGuard AI"),
           ("Version", "1.2.0"),
           ("Status", "Production Ready"),
           ("Last Update", "May 26, 2024"),
           ("Developer", "VisionGuard Team"),
            ("License", "MIT License")
        ]
        
        for label, value in version_items:
            item = ctk.CTkFrame(version_card, fg_color='transparent')
            item.pack(fill='x', padx=15, pady=3)
            
            ctk.CTkLabel(
                item,
                text=f"{label}:",
                font=('Arial', 11, 'bold'),
                text_color=color['text']
            ).pack(anchor='w', side='left', padx=(0, 10))
            
            ctk.CTkLabel(
                item,
                text=value,
                font=('Arial', 11),
                text_color=color['text_light']
            ).pack(anchor='w', side='left')
        
        # Contact Card
        contact_card = ctk.CTkFrame(
            scroll,
            fg_color=color['white'],
            corner_radius=12,
            border_width=1,
            border_color=color['border']
        )
        contact_card.pack(fill='x', padx=10, pady=(10, 30))
     
        ctk.CTkLabel(
            contact_card,
            text="📧 Contact & Support",
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        contact_text = """For questions, suggestions, or bug reports, please feel free to contact us.

GitHub: https://github.com/visionguard
Email: support@visionguard.ai
Web: https://www.visionguard.ai”"""
        
        ctk.CTkLabel(
            contact_card,
            text=contact_text,
            font=('Arial', 10),
            text_color=color['text_light'],
            wraplength=400,
            justify='left'
        ).pack(anchor='w', padx=15, pady=(0, 15))
 
 
    def simple_page_title(self, page, text):
        """Basit sayfa başlığı"""
        ctk.CTkLabel(
            page,
            text=text,
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 20))
    
    # ===================================
    # RECORDS PAGE HELPERS
    # ===================================
    
    def _show_records_tab(self, tab):
        """Records sekmesini değiştir"""
        self.records_tab.set(tab)
        
        # Clear content
        for widget in self.records_content.winfo_children():
            widget.destroy()
        
        if tab == "detections":
            self._load_detections_view()
        else:
            self._load_notifications_view()
    
    def _load_detections_view(self):
        """Fotoğrafları yükle"""
        from backend.database import db
        
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(
            self.records_content,
            fg_color=color['white']
        )
        scrollable.pack(fill='both', expand=True, padx=15, pady=15)
        
        detections = db.get_detections()
        
        if not detections:
            ctk.CTkLabel(
                scrollable,
                text="No records yet",
                font=('Arial', 14),
                text_color=color['text_light']
            ).pack(pady=50)
            return
        
        for detection_id, timestamp in detections:
            self._create_detection_item(scrollable, detection_id, timestamp)
    
    def _create_detection_item(self, parent, detection_id, timestamp):
        """Create detection item"""
        item = ctk.CTkFrame(
            parent,
            fg_color='#F0F8FF',
            corner_radius=12,
            height=80
        )
        item.pack(fill='x', pady=8)
        
        # Left side - info
        left = ctk.CTkFrame(item, fg_color='transparent')
        left.pack(side='left', padx=15, pady=12, fill='both', expand=True)
        
        ctk.CTkLabel(
            left,
            text=f"📷 Detection #{detection_id}",
            font=('Arial', 13, 'bold'),
            text_color=color['text']
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            left,
            text=f"⏰ {timestamp}",
            font=('Arial', 11),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(3, 0))
        
        # Right side - button
        ctk.CTkButton(
            item,
            text="👁 Show",
            width=100,
            height=35,
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            font=('Arial', 11, 'bold'),
            command=lambda: self._show_full_image(detection_id)
        ).pack(side='right', padx=15, pady=12)
    
    def _show_full_image(self, detection_id):
        """Tam boyutlu resmi göster"""
        from backend.database import db
        import io
        from PIL import Image
        
        image_data = db.get_detection_image(detection_id)
        
        if not image_data:
            return
        
        try:
            # Image'ı göster
            img = Image.open(io.BytesIO(image_data))
            
            # New window
            view_window = ctk.CTkToplevel(self.master)
            view_window.title(f"Detection {detection_id}")
            view_window.geometry("800x600")
            
            # Convert PIL image to CTkImage for display
            from customtkinter import CTkImage
            from PIL import Image as PILImage
            
            # Resize for display
            display_img = img.copy()
            display_img.thumbnail((750, 550))
            
            # Display
            tk_image = CTkImage(display_img, size=(display_img.width, display_img.height))
            
            label = ctk.CTkLabel(view_window, image=tk_image, text="")
            label.image = tk_image  # Keep reference
            label.pack(padx=10, pady=10)
            
        except Exception as e:
            print(f"Error loading image: {e}")
    
    # ===================================
    # NOTIFICATIONS PAGE HELPERS
    # ===================================
    
    def _load_notifications(self):
        """Load notifications"""
        from backend.database import db
        
        notifications = db.get_notifications()
        
        if not notifications:
            ctk.CTkLabel(
                self.notifications_scrollable,
                text="No notifications yet",
                font=('Arial', 14),
                text_color=color['text_light']
            ).pack(pady=50)
            return
        
        for notif_id, detection_id, message, sent_at in notifications:
            self._create_notification_item(notif_id, detection_id, message, sent_at)
    
    def _create_notification_item(self, notif_id, detection_id, message, sent_at):
        """Create notification item"""
        item = ctk.CTkFrame(
            self.notifications_scrollable,
            fg_color='#FFF8F0',
            corner_radius=12,
            height=80
        )
        item.pack(fill='x', pady=8, padx=15)
        
        # Left side
        left = ctk.CTkFrame(item, fg_color='transparent')
        left.pack(side='left', padx=12, pady=12, fill='both', expand=True)
        
        ctk.CTkLabel(
            left,
            text=f"🔔 {message}",
            font=('Arial', 13, 'bold'),
            text_color=color['text']
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            left,
            text=f"⏰ {sent_at}",
            font=('Arial', 11),
            text_color=color['text_light']
        ).pack(anchor='w', pady=(3, 0))
        
        # Right side
        if detection_id:
            ctk.CTkButton(
                item,
                text="📷 View Image",
                width=100,
                height=35,
                fg_color='#FF9500',
                hover_color='#E88000',
                text_color=color['white'],
                font=('Arial', 11, 'bold'),
                command=lambda: self._show_full_image(detection_id)
            ).pack(side='right', padx=12, pady=12)
    
    # ===================================
    # REFRESH HELPERS
    # ===================================

    def _refresh_dashboard_stats(self):
        """Hareket sonrası tüm UI alanlarını güncelle"""
        from backend.database import db

        # Dashboard - total records badge
        detections = db.get_detections()
        total = len(detections) if detections else 0
        if hasattr(self, 'dashboard_total_records'):
            self.dashboard_total_records.configure(text=f"{total} Detected")

        # Records sayfası - eğer açıksa yenile
        if hasattr(self, 'records_content'):
            for widget in self.records_content.winfo_children():
                widget.destroy()
            self._load_detections_view()

        # Notifications sayfası - eğer açıksa yenile
        if hasattr(self, 'notifications_scrollable'):
            for widget in self.notifications_scrollable.winfo_children():
                widget.destroy()
            self._load_notifications()

        # Notifications count badge (dashboard card)
        notifications = db.get_notifications()
        if hasattr(self, 'notifications_stats_label'):
            self.notifications_stats_label.configure(
                text=f"🔔 Total Notifications: {len(notifications) if notifications else 0}\n🎥 Camera: {'🟢 Running' if self.is_detecting else '🔴 Closed'}"
            )

        # ===================================
    # MOTION DETECTION HELPERS
    # ===================================
    
    def _start_motion_detection(self):
        """Motion algılamayı başlat - Tüm göstergeler senkronize"""
        from backend.database import db
        from backend.log_manager import log_manager
        from backend.camera import camera_manager
        from customtkinter import CTkImage
        from PIL import Image

        def on_frame(pil_img):
            """Her frame'de GUI'yi güncelle (main thread'e schedule et)"""
            def update():
                if not self.is_detecting:
                    return
                try:
                    if hasattr(self, 'camera_label'):
                        lw = self.camera_label.winfo_width() or 640
                        lh = self.camera_label.winfo_height() or 480
                        img_live = pil_img.resize((lw, lh), Image.LANCZOS)
                        ctk_live = CTkImage(light_image=img_live, size=(lw, lh))
                        self.camera_label.configure(image=ctk_live, text="")
                        self.camera_label._ctk_image = ctk_live

                    if hasattr(self, 'dashboard_camera_label'):
                        dw = self.dashboard_camera_label.winfo_width() or 640
                        dh = self.dashboard_camera_label.winfo_height() or 480
                        img_dash = pil_img.resize((dw, dh), Image.LANCZOS)
                        ctk_dash = CTkImage(light_image=img_dash, size=(dw, dh))
                        self.dashboard_camera_label.configure(image=ctk_dash, text="")
                        self.dashboard_camera_label._ctk_image = ctk_dash
                except Exception:
                    pass
            self.master.after(0, update)

        def on_detection(image_bytes):
            """Save detection and notification to database"""
            def save():
                from datetime import datetime
                sensitivity = int(self.sensitivity_slider.get()) if hasattr(self, 'sensitivity_slider') else 70
                # 1. Save detection image
                success, detection_id = db.save_detection(image_bytes, encrypt=True)
                if success:
                    # 2. Log motion detection
                    log_manager.log_motion_detection(detection_id, db.current_user, sensitivity)
                    # 3. Save notification to DB
                    message = f"Motion Detected! ({datetime.now().strftime('%H:%M:%S')})"
                    notif_saved = db.save_notification(detection_id, message)
                    # 4. Log notification
                    if notif_saved:
                        log_manager.log_notification_sent(detection_id, detection_id, db.current_user, message)
                    # 5. Refresh UI
                    self._refresh_dashboard_stats()
            self.master.after(0, save)

        self.is_detecting = True
        sensitivity = int(self.sensitivity_slider.get()) if hasattr(self, 'sensitivity_slider') else 70
        camera_manager.start(sensitivity, on_frame, on_detection)
        
        # Live sekmesi - butonları güncelle
        if hasattr(self, 'start_btn'):
            self.start_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
            self.status_label.configure(text="● Running", text_color='#45C46B')
            self.camera_label.configure(text="📹 Camera Active\nWaiting for motion...")
        
        # Dashboard sekmesi - butonları güncelle
        if hasattr(self, 'dashboard_start_btn'):
            self.dashboard_start_btn.configure(state='disabled')
            self.dashboard_stop_btn.configure(state='normal')
            self.dashboard_status_label.configure(text="● Running", text_color='#45C46B')
            self.dashboard_camera_label.configure(text="📹 Camera Active\nWaiting for motion...")
            self.dashboard_camera_status.configure(text="● Running", text_color='#45C46B')
            self.dashboard_info_text.configure(text="Camera Active.\nMotion detection in progress...")
        
        # Log: Motion algılama başladı
        sensitivity = int(self.sensitivity_slider.get()) if hasattr(self, 'sensitivity_slider') else 70
        log_manager.log_system_event(
            "info",
            f"Motion detection started (Sensitivity: {sensitivity}%)",
            error=None,
            username=db.current_user
        )
        
    def _stop_motion_detection(self):
        """Motion algılamayı durdur - Tüm göstergeler senkronize"""
        from backend.log_manager import log_manager
        from backend.database import db
        from backend.camera import camera_manager
        
        self.is_detecting = False
        camera_manager.stop()
        
        # Kamera label'larını resetle
        if hasattr(self, 'camera_label'):
            self.camera_label.configure(image=None, text="📹 Camera Stopped")
        if hasattr(self, 'dashboard_camera_label'):
            self.dashboard_camera_label.configure(image=None, text="📹 Camera Stopped")
        
        # Live sekmesi - butonları güncelle
        if hasattr(self, 'start_btn'):
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            self.status_label.configure(text="● Ready", text_color='#FF9500')
            self.camera_label.configure(text="📹 Camera Stopped")
        
        # Dashboard sekmesi - butonları güncelle
        if hasattr(self, 'dashboard_start_btn'):
            self.dashboard_start_btn.configure(state='normal')
            self.dashboard_stop_btn.configure(state='disabled')
            self.dashboard_status_label.configure(text="● Ready", text_color='#FF9500')
            self.dashboard_camera_label.configure(text="📹 Camera Stopped")
            self.dashboard_camera_status.configure(text="● Closed", text_color='#FF5C5C')
            self.dashboard_info_text.configure(text="Camera stopped.\nPress Start to begin.")
        
        # Records sekmesini güncelle
        if hasattr(self, 'records_status_label'):
            self.records_status_label.configure(text="● Closed", text_color='#FF5C5C')
            if hasattr(self, 'records_stats_label'):
                self.records_stats_label.configure(text=self._get_records_stats())
        
        # Notifications sekmesini güncelle
        if hasattr(self, 'notifications_status_label'):
            self.notifications_status_label.configure(text="● Closed", text_color='#FF5C5C')
            if hasattr(self, 'notifications_stats_label'):
                from backend.database import db
                notifications = db.get_notifications()
                self.notifications_stats_label.configure(
                    text=f"🔔 Total Notifications: {len(notifications) if notifications else 0}\n🎥 Camera: 🔴 Closed"
                )
        
        # Log: Motion algılama durduruldu
        log_manager.log_system_event(
            "info",
            "Motion detection stopped",
            error=None,
            username=db.current_user
        )