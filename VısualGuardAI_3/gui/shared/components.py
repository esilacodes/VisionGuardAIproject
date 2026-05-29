

import customtkinter as ctk
from config.settings import color, font, layout



class TextInputField:
    """CustomTkinter Entry with icon"""
    def __init__(self, master, label_text, show=None, icon_text=None):
        self.label_text = label_text
        self.show = show
        
        # ✅ FRAME (icon + entry beraber)
        self.main_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.main_frame.pack(pady=8, padx=0, fill='x')  # ✅ pady azaltıldı (10→8)
        
        # ✅ ICON
        if icon_text:
            icon_label = ctk.CTkLabel(
                self.main_frame,
                text=icon_text,
                font=('Arial', 16),
                text_color=color['icon']
            )
            icon_label.pack(side='left', padx=(0, 10))
        
        # ✅ ENTRY
        self.entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text=label_text,
            width=layout['input_width'],
            height=layout['input_height'],
            corner_radius=14,
            border_color=color['input_border'],
            fg_color=color['input_bg'],
            font=font['body'],
            text_color=color['text'],
            placeholder_text_color=color['text_light']
        )
        self.entry.pack(side='left', fill='x', expand=True, padx=0, pady=0)
        
        if show:
            self.entry.configure(show=show)
    
    def get_value(self):
        return self.entry.get()
    
    def clear(self):
        self.entry.delete(0, ctk.END)


class Button:
    """CustomTkinter Button"""
    def __init__(self, master, text, command=None):
        self.button = ctk.CTkButton(
            master,
            text=text,
            command=command,
            width=layout['button_width'],
            height=layout['button_height'],
            corner_radius=14,
            fg_color=color['primary'],
            hover_color=color['primary_dark'],
            text_color=color['white'],
            font=font['button']
        )
        self.button.pack(pady=10, padx=0, fill='x')  # ✅ pady azaltıldı (15→10)
class Link:
    
    def __init__(self, master, text, command=None):
        self.label = ctk.CTkLabel(
            master,
            text=text,
            font=font['label'],
            text_color=color['primary'],
            cursor="hand2"
        )
        self.label.pack(side='left')
        if command:
            self.label.bind("<Button-1>", lambda e: command())