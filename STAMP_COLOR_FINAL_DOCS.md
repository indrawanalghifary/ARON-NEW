# ✨ FITUR STAMP COLOR CUSTOMIZATION - DOKUMENTASI FINAL

## 📋 Ringkasan Fitur
Fitur baru yang memungkinkan customisasi warna stamp text untuk setiap platform:
- **Shopee**: Merah (255, 0, 0) 🔴 - brand color Shopee
- **TikTok**: Hitam (0, 0, 0) ⬛ - netral/professional
- **Lazada**: Biru (0, 102, 255) 🔵 - brand color Lazada

---

## 🔧 Implementasi Teknis

### 1. File Konfigurasi: `stamp_colors.py`

**Fungsi utama:**
```python
get_platform_color(platform="default", normalize=True)
```

- **Parameter `platform`**: Nama platform (shopee, tiktok, lazada, red, blue, green, dll)
- **Parameter `normalize`**: 
  - `True` (default): Return warna normalized 0-1 (untuk PyMuPDF)
  - `False`: Return warna original 0-255

**Contoh:**
```python
from stamp_colors import get_platform_color

# Get normalized color untuk Shopee
shopee_color = get_platform_color("shopee", normalize=True)
# Result: (1.0, 0.0, 0.0)

# Get original RGB untuk referensi
shopee_rgb = get_platform_color("shopee", normalize=False)
# Result: (255, 0, 0)
```

### 2. Update `split.py` (Shopee)

**Function signature:**
```python
def spk_proses(input_pdf, output_pdf, split_map=split_map, 
               codename="ASE", stamp_color=(0, 0, 0), stamp_fontsize=9):
    # ... proses PDF ...
    result = find_text_and_add_text(
        page, "No.Pesanan: ", text_produk,
        fontsize=stamp_fontsize,
        color=stamp_color  # ← Pass normalized color
    )
```

**Parameter:**
- `stamp_color`: Tuple RGB (r, g, b) dengan range 0-1.0
- `stamp_fontsize`: Ukuran font stamp (default: 9)

### 3. Update `bagus.py` (TikTok)

**Function signature:**
```python
def main(pdf_path, out_path, split_map=split_map, 
         codename="ASE", stamp_color=(0, 0, 0)):

def adding_stamp(page, text, color=(0, 0, 0)):

def add_stamp(page, text, x, y, size=12, color=(0, 0, 0)):
```

**Changes:**
- Semua function menerima parameter `color`
- `add_stamp()` pass color ke `page.insert_text()`

### 4. Update `main.py` (UI Integration)

**Import:**
```python
from stamp_colors import get_platform_color
```

**TikTok tab:**
```python
def jalankan_edit(self):
    stamp_color = get_platform_color("tiktok", normalize=True)
    hasil = main(..., stamp_color=stamp_color)
```

**Shopee tab:**
```python
def jalankan_edit_shopee(self):
    stamp_color = get_platform_color("shopee", normalize=True)
    hasil = spk_proses(..., stamp_color=stamp_color)
```

---

## 📊 Warna yang Tersedia

| Nama | RGB (0-255) | RGB (0-1.0) | Hex | Platform |
|------|-------------|------------|-----|----------|
| red | (255, 0, 0) | (1.0, 0.0, 0.0) | #ff0000 | Shopee 🔴 |
| blue | (0, 0, 255) | (0.0, 0.0, 1.0) | #0000ff | - |
| green | (0, 128, 0) | (0.0, 0.5, 0.0) | #008000 | - |
| black | (0, 0, 0) | (0.0, 0.0, 0.0) | #000000 | TikTok ⬛ |
| orange | (255, 165, 0) | (1.0, 0.65, 0.0) | #ffa500 | Tokopedia |
| purple | (128, 0, 128) | (0.5, 0.0, 0.5) | #800080 | - |
| white | (255, 255, 255) | (1.0, 1.0, 1.0) | #ffffff | - |
| lazada | (0, 102, 255) | (0.0, 0.4, 1.0) | #0066ff | Lazada 🔵 |

---

## 🚀 Cara Menggunakan

### Cara #1: Automatic via UI ✨
```python
# TikTok - Otomatis hitam
jalankan_edit()  

# Shopee - Otomatis merah
jalankan_edit_shopee()
```

### Cara #2: Manual Script
```python
from split import spk_proses
from bagus import main
from stamp_colors import get_platform_color

# Shopee dengan merah
color = get_platform_color("shopee", normalize=True)
spk_proses("input.pdf", "output.pdf", stamp_color=color)

# TikTok dengan hitam
color = get_platform_color("tiktok", normalize=True)
main("input.pdf", "output.pdf", stamp_color=color)

# Custom warna
from stamp_colors import normalize_color
custom_rgb = (200, 100, 50)  # Orange custom
color = normalize_color(custom_rgb)
spk_proses("input.pdf", "output.pdf", stamp_color=color)
```

### Cara #3: Add Custom Platform
```python
# Update stamp_colors.py
STAMP_COLORS = {
    "shopee": (255, 0, 0),
    "tiktok": (0, 0, 0),
    "lazada": (0, 102, 255),
    "tokopedia": (0, 150, 0),    # ← Add ini
    "blibli": (255, 0, 128),     # ← Add ini
}

# Update main.py
def jalankan_edit_tokopedia(self):
    stamp_color = get_platform_color("tokopedia", normalize=True)
    hasil = spk_proses(..., stamp_color=stamp_color)
```

---

## 🧪 Testing

Run test script:
```bash
python test_stamp_colors.py
```

**Test yang dilakukan:**
1. ✓ Color retrieval dari STAMP_COLORS
2. ✓ Normalisasi warna 0-255 → 0-1
3. ✓ Stamp dengan warna normal (reference text ada)
4. ✓ Stamp dengan warna fallback (halaman kosong)
5. ✓ Custom warna yang tidak di list
6. ✓ Generate test PDF dengan berbagai warna

**Output:**
```
✓ Test selesai - Output: test_colors_output.pdf
```

---

## 📁 File yang Dimodifikasi

| File | Perubahan |
|------|-----------|
| `stamp_colors.py` | NEW - Konfigurasi warna & helper functions |
| `split.py` | ADD: `stamp_color`, `stamp_fontsize` params |
| `bagus.py` | ADD: `stamp_color`, `color` params di semua function |
| `main.py` | IMPORT stamp_colors, UPDATE jalankan_edit calls |
| `test_stamp_colors.py` | NEW - Test script untuk verifikasi |
| `STAMP_COLOR_FEATURE.md` | NEW - Feature documentation |

---

## 🎯 Fitur yang Implemented

- [x] Color configuration (stamp_colors.py)
- [x] Color normalization untuk PyMuPDF
- [x] Support di split.py (Shopee)
- [x] Support di bagus.py (TikTok)
- [x] UI integration di main.py
- [x] Auto-apply warna per platform
- [x] Support custom warna
- [x] Comprehensive testing
- [x] Fallback position dengan warna yang sama

---

## 🔮 Future Improvements

### Phase 2 (Next Steps):
1. UI color picker untuk select warna custom
2. Save color preference di config file
3. Per-order color customization
4. Color preview sebelum process
5. Add lebih banyak platform (Lazada, Tokopedia, dll)

### Code Example (Future):
```python
# main.py - Add UI control untuk color
def show_color_selector(self):
    colors = get_all_colors(normalize=False)
    selected_color, ok = QInputDialog.getItem(
        self, "Pilih Warna Stamp", 
        "Warna:", list(colors.keys())
    )
    if ok:
        self.stamp_color = get_platform_color(selected_color, normalize=True)
```

---

## ✅ Verification Checklist

- [x] stamp_colors.py dibuat dengan fungsi helper
- [x] Color normalization untuk PyMuPDF (0-1 range)
- [x] split.py update dengan stamp_color parameter
- [x] bagus.py update dengan color parameter di semua tempat
- [x] main.py import dan gunakan get_platform_color()
- [x] TikTok automatic hitam
- [x] Shopee automatic merah
- [x] Test script berhasil dengan semua warna
- [x] Fallback position support custom color
- [x] Custom warna dapat digunakan

---

## 📌 Notes

1. **PyMuPDF Color Format**: Warna harus dalam range 0-1.0, bukan 0-255
   - Gunakan `normalize_color()` atau `get_platform_color(..., normalize=True)`

2. **Default Fallback Color**: (0.0, 0.0, 0.0) = Hitam
   - Jika platform tidak ada di STAMP_COLORS

3. **Backward Compatible**: Parameter bersifat optional dengan default values
   - Kode lama tetap berjalan tanpa perubahan

4. **Color Priority**: UI → Platform → Default
   - Jika UI pass warna → use UI color
   - Else jika platform defined → use platform color
   - Else → use default hitam

---

**Status**: ✅ FULLY IMPLEMENTED & TESTED
**Date**: June 3, 2026
