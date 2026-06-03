# 🎨 QUICK REFERENCE: Stamp Color Customization

## TL;DR (Ringkas)

✅ Fitur siap! Stamp text sekarang otomatis berwarna sesuai platform:
- **Shopee**: 🔴 Merah
- **TikTok**: ⬛ Hitam
- **Lazada**: 🔵 Biru

---

## Cara Menggunakan

### GUI (Mudah - Recommended)
```
1. Buka aplikasi ARON
2. Login dengan token
3. TikTok tab → akan auto hitam ⬛
4. Shopee tab → akan auto merah 🔴
5. Selesai! ✨
```

### Command Line (Advanced)

```python
# TikTok (Hitam)
from bagus import main
from stamp_colors import get_platform_color

color = get_platform_color("tiktok", normalize=True)
main("input.pdf", "output.pdf", stamp_color=color)

# Shopee (Merah)
from split import spk_proses
from stamp_colors import get_platform_color

color = get_platform_color("shopee", normalize=True)
spk_proses("input.pdf", "output.pdf", stamp_color=color)

# Custom Warna
from stamp_colors import normalize_color

custom_orange = normalize_color((255, 165, 0))
spk_proses("input.pdf", "output.pdf", stamp_color=custom_orange)
```

---

## Available Colors

```python
get_platform_color("tiktok")      # ⬛ Hitam
get_platform_color("shopee")      # 🔴 Merah
get_platform_color("lazada")      # 🔵 Biru
get_platform_color("red")         # 🔴 Merah
get_platform_color("blue")        # 🔵 Biru
get_platform_color("green")       # 🟢 Hijau
get_platform_color("orange")      # 🟠 Orange
get_platform_color("purple")      # 🟣 Ungu
get_platform_color("black")       # ⬛ Hitam
get_platform_color("white")       # ⚪ Putih
```

---

## Behind The Scenes

| Component | File | Perubahan |
|-----------|------|-----------|
| Config | `stamp_colors.py` | NEW - Warna & helper |
| Shopee | `split.py` | +color param |
| TikTok | `bagus.py` | +color param |
| UI | `main.py` | auto-apply warna |
| Test | `test_stamp_colors.py` | NEW - Verify feature |

---

## Testing

Verify semuanya berjalan:
```bash
python test_stamp_colors.py
```

Expected output: ✓ ALL TESTS COMPLETED

---

## Notes

⚠️ **Important**: Warna format adalah 0-1 range (PyMuPDF standard)
- Jangan pass (255, 0, 0) - akan error!
- Gunakan get_platform_color() atau normalize_color()
- Atau langsung pass (1.0, 0.0, 0.0) ✓

💡 **Tip**: Add custom warna di stamp_colors.py STAMP_COLORS dict

🔗 **Docs**: See [STAMP_COLOR_FINAL_DOCS.md](STAMP_COLOR_FINAL_DOCS.md) untuk detail lengkap

---

**Status**: ✅ READY TO USE
