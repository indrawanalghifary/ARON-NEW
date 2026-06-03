# Konfigurasi warna stamp untuk berbagai platform
# Format RGB tuple: (Red, Green, Blue) dengan nilai 0-255

# Warna standar
STAMP_COLORS = {
    # Platform
    "shopee": (255, 0, 0),      # Merah (brand color Shopee)
    "tiktok": (0, 0, 0),        # Hitam (default)
    "lazada": (0, 102, 255),    # Biru cerah (brand color Lazada)
    
    # Warna umum
    "default": (0, 0, 0),       # Hitam
    "red": (255, 0, 0),         # Merah
    "blue": (0, 0, 255),        # Biru
    "green": (0, 128, 0),       # Hijau
    "orange": (255, 165, 0),    # Orange
    "purple": (128, 0, 128),    # Ungu
    "black": (0, 0, 0),         # Hitam
    "white": (255, 255, 255),   # Putih
}

def normalize_color(color_rgb):
    """
    Normalize warna dari range 0-255 ke range 0-1 (untuk PyMuPDF)
    
    Args:
        color_rgb: RGB tuple (r, g, b) dengan nilai 0-255
    
    Returns:
        RGB tuple (r, g, b) dengan nilai 0-1.0
    
    Examples:
        >>> normalize_color((255, 0, 0))
        (1.0, 0.0, 0.0)
        
        >>> normalize_color((0, 128, 255))
        (0.0, 0.5019607843137255, 1.0)
    """
    if not color_rgb or len(color_rgb) != 3:
        return (0.0, 0.0, 0.0)  # Default hitam
    
    return tuple(c / 255.0 for c in color_rgb)

def get_platform_color(platform="default", normalize=True):
    """
    Dapatkan warna stamp untuk platform tertentu
    
    Args:
        platform: Nama platform (shopee, tiktok, lazada, atau warna umum)
        normalize: Jika True, normalize ke range 0-1 (default PyMuPDF)
                   Jika False, kembalikan RGB 0-255
    
    Returns:
        RGB tuple (r, g, b)
        - Jika normalize=True: range 0-1.0 (untuk PyMuPDF)
        - Jika normalize=False: range 0-255
    
    Examples:
        >>> get_platform_color("shopee")
        (1.0, 0.0, 0.0)  # normalized
        
        >>> get_platform_color("shopee", normalize=False)
        (255, 0, 0)  # original 0-255
        
        >>> get_platform_color("tiktok")
        (0.0, 0.0, 0.0)  # normalized hitam
    """
    color_rgb = STAMP_COLORS.get(platform.lower(), STAMP_COLORS["default"])
    
    if normalize:
        return normalize_color(color_rgb)
    else:
        return color_rgb

def get_all_colors(normalize=True):
    """
    Return dictionary semua warna yang tersedia
    
    Args:
        normalize: Jika True, return warna normalized (0-1)
                   Jika False, return warna original (0-255)
    """
    if normalize:
        return {name: normalize_color(color) for name, color in STAMP_COLORS.items()}
    else:
        return STAMP_COLORS.copy()

# Contoh penggunaan:
if __name__ == "__main__":
    print("Available stamp colors (0-255 range):")
    for name, color in STAMP_COLORS.items():
        print(f"  {name}: {color}")
    
    print("\nExample usages:")
    print(f"Shopee color (normalized): {get_platform_color('shopee')}")
    print(f"Shopee color (0-255): {get_platform_color('shopee', normalize=False)}")
    print(f"TikTok color (normalized): {get_platform_color('tiktok')}")
    print(f"Lazada color (normalized): {get_platform_color('lazada')}")

