# ✨ FITUR BARU: Customisasi Warna Stamp Text

## 🎨 Apa itu Fitur Ini?
Memungkinkan warna stamp (teks produk yang ditambahkan ke PDF) dapat dikustomisasi berbeda untuk setiap platform:
- **Shopee**: Merah (255, 0, 0) - sesuai brand color Shopee
- **TikTok**: Hitam (0, 0, 0) - netral
- **Lazada**: Biru (0, 102, 255) - sesuai brand color Lazada

---

## 🔧 Implementasi

### 1. File Konfigurasi Warna: `stamp_colors.py`
```python
STAMP_COLORS = {
    "shopee": (255, 0, 0),      # Merah
    "tiktok": (0, 0, 0),        # Hitam
    "lazada": (0, 102, 255),    # Biru
    "default": (0, 0, 0),       # Hitam
    "red": (255, 0, 0),         # Merah
    "blue": (0, 0, 255),        # Biru
    # ... dll
}
```

**Penggunaan**:
```python
from stamp_colors import get_platform_color

# Ambil warna untuk platform
shopee_color = get_platform_color("shopee")    # (255, 0, 0)
tiktok_color = get_platform_color("tiktok")    # (0, 0, 0)
```

---

### 2. Update `split.py` (untuk Shopee)
```python
def spk_proses(input_pdf, output_pdf, split_map=split_map, 
               codename="ASE", stamp_color=(0, 0, 0), stamp_fontsize=9):
    # ... proses PDF ...
    result = find_text_and_add_text(
        page, "No.Pesanan: ", text_produk,
        offset_x=100, offset_y=-3, 
        fontsize=stamp_fontsize,
        color=stamp_color  # ← Gunakan color parameter
    )
```

**Signature baru**:
- `stamp_color=(0, 0, 0)`: Warna RGB tuple untuk stamp
- `stamp_fontsize=9`: Ukuran font stamp

---

### 3. Update `bagus.py` (untuk TikTok)
```python
def main(pdf_path, out_path, split_map=split_map, 
         codename="ASE", stamp_color=(0, 0, 0)):
    # ... proses PDF ...
    adding_stamp(page_ganjil, stamp_text + " - " + codename, 
                 color=stamp_color)  # ← Pass warna

def adding_stamp(page, text, color=(0, 0, 0)):
    # ... cari lokasi stamp ...
    add_stamp(page, text, x, y, color=color)  # ← Pass warna

def add_stamp(page, text, x, y, size=12, color=(0, 0, 0)):
    page.insert_text((x, y), text, fontsize=size, 
                     fontname="Times-Bold", color=color)  # ← Gunakan color
```

---

### 4. Update `main.py` (UI Integration)
```python
from stamp_colors import get_platform_color

# TikTok: Warna hitam
def jalankan_edit(self):
    stamp_color = get_platform_color("tiktok")
    hasil = main(self.file_path, save_file, 
                 split_map=self.split_map, 
                 codename=self.codename, 
                 stamp_color=stamp_color)

# Shopee: Warna merah
def jalankan_edit_shopee(self):
    stamp_color = get_platform_color("shopee")
    hasil = spk_proses(self.file_path_shopee, save_file,
                       split_map=self.split_map,
                       codename=self.codename,
                       stamp_color=stamp_color)
```

---

## 📊 Perubahan File

| File | Perubahan | Type |
|------|-----------|------|
| `stamp_colors.py` | Baru | Created |
| `split.py` | Add `stamp_color`, `stamp_fontsize` parameters | Modified |
| `bagus.py` | Add `stamp_color`, `color` parameters | Modified |
| `main.py` | Import `get_platform_color`, update calls | Modified |

---

## 🚀 Cara Menggunakan

### Cara #1: Automatic (UI)
```python
# TikTok tab - Otomatis merah
jalankan_edit()

# Shopee tab - Otomatis hitam
jalankan_edit_shopee()
```

### Cara #2: Manual (Script)
```python
from split import spk_proses
from stamp_colors import get_platform_color

# Shopee dengan warna merah
color = get_platform_color("shopee")
hasil = spk_proses("input.pdf", "output.pdf", 
                   stamp_color=color)

# TikTok dengan warna hitam
color = get_platform_color("tiktok")
hasil = spk_proses("input.pdf", "output.pdf", 
                   stamp_color=color)

# Custom warna
hasil = spk_proses("input.pdf", "output.pdf", 
                   stamp_color=(100, 200, 50))  # RGB custom
```

### Cara #3: Add Custom Platform
```python
# Update di stamp_colors.py
STAMP_COLORS = {
    # ... existing ...
    "lazada": (0, 102, 255),    # Biru Lazada
    "tokopedia": (0, 150, 0),   # Hijau Tokopedia
}

# Gunakan
color = get_platform_color("lazada")
```

---

## 🎨 Contoh Warna RGB

| Warna | RGB | Contoh |
|-------|-----|---------|
| Merah | (255, 0, 0) | Shopee ❤️ |
| Biru | (0, 0, 255) | General |
| Hijau | (0, 128, 0) | Green |
| Hitam | (0, 0, 0) | TikTok (default) |
| Orange | (255, 165, 0) | Tokopedia |
| Ungu | (128, 0, 128) | Custom |
| Cyan | (0, 255, 255) | Custom |

---

## ✅ Testing Checklist

- [x] `stamp_colors.py` dibuat dengan fungsi helper
- [x] `split.py` mendapat parameter `stamp_color` dan `stamp_fontsize`
- [x] `bagus.py` mendapat parameter `stamp_color` di semua tempat relevan
- [x] `main.py` menggunakan `get_platform_color()` untuk setiap platform
- [x] TikTok menggunakan warna hitam (default)
- [x] Shopee menggunakan warna merah

---

## 🧪 Test Script: `test_stamp_colors.py`

```bash
python test_stamp_colors.py
```

Script ini akan:
1. Buat test PDF dengan halaman normal dan kosong
2. Process dengan berbagai warna
3. Verifikasi hasil

---

## 📝 Contoh Output Log

```
Processing Shopee PDF:
  Stamp color: (255, 0, 0) - Merah
  ✓ Stamp ditambahkan dengan warna merah

Processing TikTok PDF:
  Stamp color: (0, 0, 0) - Hitam
  ✓ Stamp ditambahkan dengan warna hitam
```

---

## 🎯 Next Steps (Future)

### Feature Ideas:
1. UI dropdown untuk select warna custom
2. Color preview sebelum process
3. Save warna preference di config
4. Per-order color customization

### Code:
```python
# Di main.py - tambah UI control untuk warna
def show_color_selector(self):
    colors = get_all_colors()
    selected_color, ok = QInputDialog.getItem(
        self, "Pilih Warna Stamp", 
        "Warna:", list(colors.keys())
    )
    if ok:
        self.stamp_color = get_platform_color(selected_color)
```

---

**Status**: ✅ IMPLEMENTED & READY
