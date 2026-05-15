from PIL import Image, ImageDraw
from config.settings import color, layout

def create_gradient_background(width, height, color_top, color_bottom):
    """Gradient arka plan oluştur"""
    img = Image.new('RGB', (width, height), color_top)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    top_rgb = hex_to_rgb(color_top)
    bottom_rgb = hex_to_rgb(color_bottom)
    
    # Gradient çiz
    for y in range(height):
        ratio = y / height
        r = int(top_rgb[0] * (1 - ratio) + bottom_rgb[0] * ratio)
        g = int(top_rgb[1] * (1 - ratio) + bottom_rgb[1] * ratio)
        b = int(top_rgb[2] * (1 - ratio) + bottom_rgb[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img