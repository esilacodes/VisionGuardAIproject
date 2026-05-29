"""
Logs Viewer Component - Passwordlenmiş Logları Görüntüler
"""

import customtkinter as ctk
from config.settings import color
from backend.log_manager import log_manager
from backend.database import db
import json


class LogsViewer:
    """Displays logs in styled cards"""
    
    def __init__(self, parent):
        """Initialize log viewer"""
        self.parent = parent
        self.log_manager = log_manager
        
        self.create_ui()
        self.load_logs()
    
    def create_ui(self):
        """Create UI"""
        # Scrollable main frame
        main_scroll = ctk.CTkScrollableFrame(
            self.parent,
            fg_color='transparent'
        )
        main_scroll.pack(fill='both', expand=True, padx=15, pady=15)
        
        # 4 Kart oluştur
        self.cards = {}
        
        # 1. System Events
        self.cards['system'] = self._create_log_card(
            main_scroll,
            "⚙️ System Events",
            "#F0F8FF",
            "system"
        )
        
        # 2. Motion Detections
        self.cards['motion'] = self._create_log_card(
            main_scroll,
            "📷 Motion Detections",
            "#FFF8F0",
            "motion"
        )
        
        # 3. Notifications
        self.cards['notifications'] = self._create_log_card(
            main_scroll,
            "🔔 Notifications",
            "#F0FFF8",
            "notifications"
        )
            
    def _create_log_card(self, parent, title, bg_color, log_type):
        """Create a log card"""
        # Ana card
        card = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        card.pack(fill='x', pady=12)
        
        # Header
        header = ctk.CTkFrame(card, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            header,
            text=title,
            font=('Arial', 14, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', side='left')
        
        # Counter
        count_label = ctk.CTkLabel(
            header,
            text="Loading...",
            font=('Arial', 11),
            text_color=color['text_light']
        )
        count_label.pack(anchor='e', side='right')
        
        # Scrollable content
        content = ctk.CTkScrollableFrame(
            card,
            fg_color='transparent',
            height=150
        )
        content.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        return {
            'frame': card,
            'content': content,
            'count_label': count_label,
            'type': log_type
        }
    
    def load_logs(self):
        """Load logs for current user only"""

        current_user = db.current_user

        # System Logs - only current user
        system_logs = self.log_manager.get_system_logs()
        system_logs = [
            log for log in (system_logs or [])
            if log.get("username") == current_user
        ]
        self._populate_card('system', system_logs)

        # Motion Logs (filtered)
        motion_logs = self.log_manager.get_motion_logs()
        motion_logs = [
            log for log in (motion_logs or [])
            if log.get("username") == current_user
        ]
        self._populate_card('motion', motion_logs)

        # Notification Logs (filtered)
        notif_logs = self.log_manager.get_notification_logs()
        notif_logs = [
            log for log in (notif_logs or [])
            if log.get("username") == current_user
        ]
        self._populate_card('notifications', notif_logs)
            
    def _populate_card(self, card_type, logs):
        """Populate card with logs"""
        card = self.cards[card_type]
        
        # Clear content
        for widget in card['content'].winfo_children():
            widget.destroy()
        
        # Update counter
        count = len(logs) if logs else 0
        card['count_label'].configure(text=f"📊 {count} log")
        
        if not logs:
            ctk.CTkLabel(
                card['content'],
                text="No logs yet",
                font=('Arial', 11),
                text_color=color['text_light']
            ).pack(pady=20)
            return
        
        # Show last 10 logs
        for log in logs[-10:]:
            self._create_log_item(card['content'], log, card_type)
    
    def _create_log_item(self, parent, log_dict, log_type):
        """Create a log item"""
        # Log item
        item = ctk.CTkFrame(
            parent,
            fg_color=color['white'],
            corner_radius=8,
            border_width=1,
            border_color=color['border']
        )
        item.pack(fill='x', pady=5)
        
        # Timestamp
        timestamp = log_dict.get('timestamp', 'N/A')
        ctk.CTkLabel(
            item,
            text=f"⏰ {timestamp}",
            font=('Arial', 9),
            text_color=color['text_light']
        ).pack(anchor='w', padx=10, pady=(8, 3))
        
        # Log content
        if log_type == 'system':
            message = f"{log_dict.get('event_type', 'N/A')}: {log_dict.get('message', 'N/A')}"
        elif log_type == 'motion':
            message = f"Detection #{log_dict.get('detection_id', 'N/A')} (Sensitivity: {log_dict.get('sensitivity', 'N/A')}%)"
        elif log_type == 'notifications':
            message = log_dict.get('message', 'N/A')
        elif log_type == 'user':
            message = f"{log_dict.get('event_type', 'N/A')}"
        else:
            message = str(log_dict)
        
        ctk.CTkLabel(
            item,
            text=message,
            font=('Arial', 10),
            text_color=color['text'],
            wraplength=400,
            justify='left'
        ).pack(anchor='w', padx=10, pady=(0, 8))

