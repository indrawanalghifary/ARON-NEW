# DEBUG: Stamp Tidak Tampil pada Halaman Kosong

## 🔍 Masalah
Stamp (teks yang ditambahkan ke PDF) tidak tampil ketika halaman kosong setelah split. Ini terjadi karena fungsi `find_text_and_add_text()` mencari teks referensi (`"No.Pesanan: "`), dan jika tidak ditemukan, fungsi mengembalikan `None` tanpa menambahkan stamp.

### Alur Masalah Lama
```
Halaman Kosong
    ↓
find_text_and_add_text() mencari "No.Pesanan: "
    ↓
Teks TIDAK ditemukan
    ↓
page.search_for() mengembalikan list kosong []
    ↓
return None (TIDAK ada stamp ditambahkan!)
```

## ✅ Solusi
Menambahkan **fallback position** untuk halaman kosong. Ketika teks referensi tidak ditemukan, stamp tetap ditambahkan di posisi default (top-left).

### Alur Masalah Baru
```
Halaman Kosong
    ↓
find_text_and_add_text() mencari "No.Pesanan: "
    ↓
Teks TIDAK ditemukan
    ↓
page.search_for() mengembalikan list kosong []
    ↓
TAMBAHKAN STAMP DI FALLBACK POSITION (x=10, y=20)
    ↓
return result dengan is_fallback=True ✓
```

## 📝 Perubahan yang Dilakukan

### 1. Update Signature Fungsi `find_text_and_add_text()`
**File**: `split.py` (baris 330-358)

```python
def find_text_and_add_text(page, search_text, insert_text, offset_x=0, offset_y=0, 
                            reference_point="x0", fontsize=12, fontname="Times-Bold", 
                            color=(0, 0, 0), fallback_x=10, fallback_y=20):  # ← Tambahan parameter
```

Parameter baru:
- `fallback_x=10`: Koordinat X fallback (default top-left)
- `fallback_y=20`: Koordinat Y fallback

### 2. Tambah Logika Fallback (baris 359-377)
```python
if not text_instances:
    # Jika teks tidak ditemukan (halaman kosong), tambahkan di posisi fallback
    print(f"Teks '{search_text}' tidak ditemukan di halaman → menggunakan fallback position")
    page.insert_text(
        (fallback_x, fallback_y),
        insert_text,
        fontsize=fontsize,
        fontname=fontname,
        color=color
    )
    
    result = {
        'search_text': search_text,
        'insert_text': insert_text,
        'found_at': None,
        'inserted_at': {
            'x': fallback_x,
            'y': fallback_y
        },
        'is_fallback': True,  # ← Flag untuk menandai fallback
        ...
    }
    return result
```

### 3. Update Flag `is_fallback` untuk Kasus Normal (baris 425)
```python
result = {
    ...
    'is_fallback': False  # ← Tambahan flag
}
```

### 4. Improve Logging di `spk_proses()` (baris 684-690)
```python
result = find_text_and_add_text(page, "No.Pesanan: ", ...)
if result:
    if result.get('is_fallback'):
        print(f"⚠ Stamp ditambahkan di fallback position (halaman kosong)")
    else:
        print(f"✓ Stamp berhasil ditambahkan di posisi normal")
else:
    print(f"✗ Gagal menambahkan stamp")
```

## 🧪 Cara Testing

### Test 1: Verifikasi dengan Test Script
```bash
cd /media/indrawan/MULTIMEDIA1/KODING/ARON-NEW
python test_stamp_fallback.py
```

Akan menghasilkan:
- `test_stamp.pdf` - PDF test dengan 2 halaman
- `test_stamp_output.pdf` - Hasil dengan stamp pada kedua halaman

**Output yang diharapkan**:
```
TEST: Halaman Normal
✓ Stamp berhasil ditambahkan di posisi normal
  - is_fallback: False
  - inserted_at: {x: 150, y: 47}

TEST: Halaman Kosong  
✓ Stamp ditambahkan di fallback position
  - is_fallback: True
  - inserted_at: {x: 10, y: 20}
```

### Test 2: Verifikasi dengan File Asli
```bash
python main.py
```

Cek log output untuk:
- Halaman normal: `✓ Stamp berhasil ditambahkan di posisi normal`
- Halaman kosong: `⚠ Stamp ditambahkan di fallback position (halaman kosong)`

## 🎯 Hasil
- ✓ Stamp **SELALU** ditampilkan, baik di halaman normal maupun kosong
- ✓ Posisi stamp dapat dikontrol via `fallback_x` dan `fallback_y`
- ✓ Flag `is_fallback` memudahkan tracking halaman kosong vs normal
- ✓ Backward compatible - tidak mengubah signature fungsi yang ada

## 📌 Catatan Penting

1. **Default Fallback Position**: `(10, 20)` = top-left PDF page
   - Bisa disesuaikan dengan melewatkan parameter saat memanggil fungsi
   
2. **Contoh Customize Fallback**:
   ```python
   result = find_text_and_add_text(
       page, 
       "No.Pesanan: ", 
       text_produk,
       fallback_x=100,  # Posisi horizontal custom
       fallback_y=50    # Posisi vertikal custom
   )
   ```

3. **Debug di Halaman Kosong**: Jika stamp masih tidak muncul, cek:
   - Apakah `fallback_x` dan `fallback_y` dalam batas halaman?
   - Apakah font size cukup besar untuk terlihat?
   - Apakah ada overlay atau background yang menutupi?

## 🔗 File yang Berubah
- `split.py` - Main fix
- `test_stamp_fallback.py` - Test script baru
- `DEBUG_STAMP.md` - Documentation (file ini)
