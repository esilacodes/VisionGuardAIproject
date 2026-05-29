
import customtkinter as ctk
from gui.shared.message_box import MessageBox
from backend.database import db
from config.settings import color

class SettingsTab:
    def __init__(self, master, on_logout=None):
        self.master = master
        self.on_logout = on_logout
        
        # Main frame with scroll
        self.frame = ctk.CTkScrollableFrame(master, fg_color=color['background'], label_text="")
        self.frame.pack(fill='both', expand=True)
        
        # Title
        ctk.CTkLabel(
            self.frame,
            text="⚙️ Settings",
            font=('Arial', 28, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', pady=(0, 25), padx=0)
        
        # User Management Section
        self.create_user_management()
        # Security Settings Section
        self.create_security_settings()
        # System Settings Section
        self.create_system_settings()
    
    def create_user_management(self):
        """User Yönetimi bölümü"""
        section = ctk.CTkFrame(
            self.frame,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        section.pack(fill='x', padx=0, pady=(0, 20))
        
        # Section title
        ctk.CTkLabel(
            section,
            text="👤 User Management",
            font=('Arial', 16, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        # Description
        ctk.CTkLabel(
            section,
            text="Manage your account settings",
            font=('Arial', 11),
            text_color=color['text_light']
        ).pack(anchor='w', padx=20, pady=(0, 15))
        
        # Buttons container
        buttons_frame = ctk.CTkFrame(section, fg_color=color['white'])
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Change Username button
        ctk.CTkButton(
            buttons_frame,
            text="📝 Change Username",
            height=45,
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            font=('Arial', 12, 'bold'),
            corner_radius=10,
            command=self._change_username
        ).pack(fill='x', pady=8)
    
    def create_security_settings(self):
        """Güvenlik Settingsı bölümü"""
        section = ctk.CTkFrame(
            self.frame,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        section.pack(fill='x', padx=0, pady=(0, 20))
        
        # Section title
        ctk.CTkLabel(
            section,
            text="🔐 Security Settings",
            font=('Arial', 16, 'bold'),
            text_color=color['text']
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        # Description
        ctk.CTkLabel(
            section,
            text="Keep your account secure",
            font=('Arial', 11),
            text_color=color['text_light']
        ).pack(anchor='w', padx=20, pady=(0, 15))
        
        # Buttons container
        buttons_frame = ctk.CTkFrame(section, fg_color=color['white'])
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Change Password button
        ctk.CTkButton(
            buttons_frame,
            text="🔑 Change Password",
            height=45,
            fg_color='#4A90E2',
            hover_color='#3A80D2',
            text_color=color['white'],
            font=('Arial', 12, 'bold'),
            corner_radius=10,
            command=self._change_password
        ).pack(fill='x', pady=8)
    
    def create_system_settings(self):
        """System Settings bölümü"""
        section = ctk.CTkFrame(
            self.frame,
            fg_color=color['white'],
            corner_radius=15,
            border_width=1,
            border_color=color['border']
        )
        section.pack(fill='x', padx=0, pady=(0, 20))
        
        # Section title
        ctk.CTkLabel(
            section,
            text="⚠️ Dangerous Operations",
            font=('Arial', 16, 'bold'),
            text_color='#FF5C5C'
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        # Description
        ctk.CTkLabel(
            section,
            text="This action cannot be undone. Please proceed with caution.",
            font=('Arial', 11),
            text_color=color['text_light']
        ).pack(anchor='w', padx=20, pady=(0, 15))
        
        # Buttons container
        buttons_frame = ctk.CTkFrame(section, fg_color=color['white'])
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Delete Account button
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Delete Account",
            height=45,
            fg_color='#FF5C5C',
            hover_color='#FF4747',
            text_color=color['white'],
            font=('Arial', 12, 'bold'),
            corner_radius=10,
            command=self._delete_account
        ).pack(fill='x', pady=8)
    
    # ===================================
    # CHANGE USERNAME
    # ===================================
    
    def _change_username(self):
        """User adını değiştir"""
        popup = ctk.CTkToplevel(self.master)
        popup.title("change username")
        popup.geometry("450x250")
        popup.resizable(False, False)
        popup.grab_set()
        
        # Label
        ctk.CTkLabel(
            popup,
            text="new username:",
            font=('Arial', 12),
            text_color=color['text']
        ).pack(pady=(20, 10), padx=20, anchor='w')
        
        # Input field
        username_entry = ctk.CTkEntry(
            popup,
            placeholder_text="enter the new username",
            width=400,
            height=45,
            corner_radius=10,
            fg_color=color['input_bg'],
            border_color=color['input_border'],
            font=('Arial', 11)
        )
        username_entry.pack(pady=(0, 30), padx=25)
        
        # Buttons
        button_frame = ctk.CTkFrame(popup, fg_color='transparent')
        button_frame.pack(fill='x', padx=25, pady=(0, 20))
        
        def save_username():
            new_username = username_entry.get()
            if not new_username:
                MessageBox.show_error(popup, "Error", "Username is not empty")
                return
            
            success, message = db.change_username(new_username)
            
            if success:
                MessageBox.show_success(popup, "Success", message)
                popup.destroy()
            else:
                MessageBox.show_error(popup, "Error", message)
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            width=180,
            height=40,
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=save_username
        ).pack(side='left', padx=5, expand=True, fill='x')
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=180,
            height=40,
            fg_color=color['tab_bg'],
            hover_color='#E8F4FF',
            text_color=color['text'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=popup.destroy
        ).pack(side='left', padx=5, expand=True, fill='x')
    
    # ===================================
    # CHANGE PASSWORD
    # ===================================
    
    def _change_password(self):
        """Passwordyi değiştir"""
        popup = ctk.CTkToplevel(self.master)
        popup.title("Change password")
        popup.geometry("450x400")
        popup.resizable(False, False)
        popup.grab_set()
        
        # Old password
        ctk.CTkLabel(
            popup,
            text="old password:",
            font=('Arial', 12),
            text_color=color['text']
        ).pack(pady=(20, 8), padx=25, anchor='w')
        
        old_password = ctk.CTkEntry(
            popup,
            placeholder_text="enter the old password",
            width=400,
            height=40,
            corner_radius=10,
            show="*",
            fg_color=color['input_bg'],
            border_color=color['input_border'],
            font=('Arial', 11)
        )
        old_password.pack(pady=(0, 15), padx=25)
        
        # New password
        ctk.CTkLabel(
            popup,
            text="new  password:",
            font=('Arial', 12),
            text_color=color['text']
        ).pack(pady=(8, 8), padx=25, anchor='w')
        
        new_password = ctk.CTkEntry(
            popup,
            placeholder_text="enter the new password",
            width=400,
            height=40,
            corner_radius=10,
            show="*",
            fg_color=color['input_bg'],
            border_color=color['input_border'],
            font=('Arial', 11)
        )
        new_password.pack(pady=(0, 15), padx=25)
        
        # Confirm password
        ctk.CTkLabel(
            popup,
            text="confirm password:",
            font=('Arial', 12),
            text_color=color['text']
        ).pack(pady=(8, 8), padx=25, anchor='w')
        
        confirm_password = ctk.CTkEntry(
            popup,
            placeholder_text=" enter the password again",
            width=400,
            height=40,
            corner_radius=10,
            show="*",
            fg_color=color['input_bg'],
            border_color=color['input_border'],
            font=('Arial', 11)
        )
        confirm_password.pack(pady=(0, 30), padx=25)
        
        # Buttons
        button_frame = ctk.CTkFrame(popup, fg_color='transparent')
        button_frame.pack(fill='x', padx=25, pady=(0, 20))
        
        def save_password():
            old_pass = old_password.get()
            new_pass = new_password.get()
            confirm_pass = confirm_password.get()
            
            if not old_pass or not new_pass or not confirm_pass:
                MessageBox.show_error(popup, "Error", "fill all labels.")
                return
            
            if new_pass != confirm_pass:
                MessageBox.show_error(popup, "Error", "new Password is not mach")
                return
            
            success, message = db.change_password(old_pass, new_pass)
            
            if success:
                MessageBox.show_success(popup, "Success", message)
                popup.destroy()
            else:
                MessageBox.show_error(popup, "Error", message)
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            width=180,
            height=40,
            fg_color='#4A90E2',
            hover_color='#3A80D2',
            text_color=color['white'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=save_password
        ).pack(side='left', padx=5, expand=True, fill='x')
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=180,
            height=40,
            fg_color=color['tab_bg'],
            hover_color='#E8F4FF',
            text_color=color['text'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=popup.destroy
        ).pack(side='left', padx=5, expand=True, fill='x')
    
    # ===================================
    # DELETE ACCOUNT
    # ===================================
    
    def _delete_account(self):
        """Hesabı sil"""
        popup = ctk.CTkToplevel(self.master)
        popup.title(" delete Account")
        popup.geometry("450x300")
        popup.resizable(False, False)
        popup.grab_set()
        
        # Warning
        ctk.CTkLabel(
            popup,
            text="⚠️ Warning!",
            font=('Arial', 16, 'bold'),
            text_color='#FF5C5C'
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            popup,
            text="Your account will be permanently deleted.\nThis action cannot be undone.",
            font=('Arial', 12),
            text_color=color['text_light'],
            justify='center'
        ).pack(pady=(0, 25))
        
        # Password confirmation
        ctk.CTkLabel(
            popup,
            text="enter password:",
            font=('Arial', 12),
            text_color=color['text']
        ).pack(pady=(0, 8), padx=25, anchor='w')
        
        password_entry = ctk.CTkEntry(
            popup,
            placeholder_text=" enter password",
            width=400,
            height=40,
            corner_radius=10,
            show="*",
            fg_color=color['input_bg'],
            border_color=color['input_border'],
            font=('Arial', 11)
        )
        password_entry.pack(pady=(0, 30), padx=25)
        
        # Buttons
        button_frame = ctk.CTkFrame(popup, fg_color='transparent')
        button_frame.pack(fill='x', padx=25, pady=(0, 20))
        
        def delete_account():
            password = password_entry.get()
            if not password:
                MessageBox.show_error(popup, "Error", "enter password")
                return
            
            success, message = db.delete_account(password)
            
            if success:
                MessageBox.show_success(popup, "Success", message)
                popup.destroy()
                if self.on_logout:
                    self.on_logout()
            else:
                MessageBox.show_error(popup, "Error", message)
        
        ctk.CTkButton(
            button_frame,
            text="yes , delete",
            width=180,
            height=40,
            fg_color='#FF5C5C',
            hover_color='#FF4747',
            text_color=color['white'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=delete_account
        ).pack(side='left', padx=5, expand=True, fill='x')
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=180,
            height=40,
            fg_color=color['tab_bg'],
            hover_color='#E8F4FF',
            text_color=color['text'],
            font=('Arial', 11, 'bold'),
            corner_radius=8,
            command=popup.destroy
        ).pack(side='left', padx=5, expand=True, fill='x')
