import fitz  # pymupdf
import re
from collections import defaultdict
import os
split_map = {
    "SQUWNT": ["SQU", "WNT"],
    "IFISPJ": ["IFI", "SPJ"],
    "CBO": ["KLRN", "SQU"],
    "AGS": ["CSH", "WNT"]
}
def combine_items(items, values, split_map):
    result = defaultdict(int)

    for item, value in zip(items, values):
        key = item.upper().strip()

        # Abaikan jika SKU kosong/empty
        if not key:
            print(f"⊘ Mengabaikan item kosong dengan qty: {value}")
            continue

        # Abaikan jika mengandung "BONUS"
        if "BONUS" in key:
            print(f"⊘ Mengabaikan item '{item}' (qty: {value}) karena mengandung 'BONUS'")
            continue
        # Abaikan jika mengandung "BROSUR"
        if "BROSUR" in key:
            print(f"⊘ Mengabaikan item '{item}' (qty: {value}) karena mengandung 'BROSUR'")
            continue

        if key in split_map:
            for sub_key in split_map[key]:
                result[sub_key] += value
        else:
            result[key] += value

    return dict(result)


def format_produk_text(combined_result, suffix="ASE"):
    produk_text = " ".join(
        f"{qty} {name}"
        for name, qty in combined_result.items()
    )

    return f"{produk_text} - {suffix}"


def format_copy_text(combined_result, prefix="JXXXXXXXX"):
    # Membuat format: 3,SQU,3,WNT
    detail = ",".join(
        f"{qty},{name}"
        for name, qty in combined_result.items()
    )

    return f"{prefix},{detail}"


# Contoh penggunaan
# items = ['squ', 'ifispj', 'squ', 'squwnt']
# values = [1, 2, 1, 1]

# split_map = {
#     "SQUWNT": ["SQU", "WNT"],
#     "IFISPJ": ["IFI", "SPJ"],
#     "KLRNSQU": ["KLRN", "SQU"],
#     "CSHWNT": ["CSH", "WNT"]
# }

# hasil = combine_items(items, values, split_map)

# text_produk = format_produk_text(hasil)
# text_copy = format_copy_text(hasil)

# print(text_produk)
# print(text_copy)

def extract_table_data(input_pdf, output_dir="extracted_sku"):
    """
    Ekstrak data tabel produk dari PDF dengan kolom:
    # | Nama Produk | SKU | Variasi | Qty
    
    Tabel dimulai dari header row dan berhenti pada 'Pesan :' text
    
    Args:
        input_pdf: Path ke file PDF input
        output_dir: Direktori referensi (optional)
    
    Returns:
        List berisi dictionaries dengan struktur:
        {
            'page': nomor halaman,
            'rows': [
                {
                    '#': '1',
                    'Nama Produk': '...',
                    'SKU': '...',
                    'Variasi': '...',
                    'Qty': '...'
                },
                ...
            ]
        }
    """
    src = fitz.open(input_pdf)
    table_data = []
    
    header_keywords = ['#', 'Nama Produk', 'SKU', 'Variasi', 'Qty']
    boundary_text = 'Pesan:'
    
    for page_num, page in enumerate(src):
        text_dict = page.get_text("dict")
        page_data = {
            'page': page_num + 1,
            'rows': []
        }
        
        # Kumpulkan semua teks dengan koordinatnya
        all_texts = []
        for block in text_dict["blocks"]:
            if block["type"] == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text_content = span["text"].strip()
                        if text_content:
                            all_texts.append({
                                'text': text_content,
                                'bbox': span["bbox"],  # (x0, y0, x1, y1)
                                'y0': span["bbox"][1],
                                'y1': span["bbox"][3],
                                'x0': span["bbox"][0],
                                'x1': span["bbox"][2]
                            })
        
        # Cari header row dengan mencari keyword header
        header_row_y = None
        header_spans = {}
        
        for text_obj in all_texts:
            if text_obj['text'] in header_keywords:
                if header_row_y is None:
                    header_row_y = text_obj['y0']
                # Catat posisi setiap kolom header
                header_spans[text_obj['text']] = text_obj['x0']
        
        if header_row_y is None:
            print(f"Halaman {page_num + 1}: Header tabel tidak ditemukan")
            continue
        
        # Sort header spans untuk mendapatkan urutan kolom
        sorted_headers = sorted(header_spans.items(), key=lambda x: x[1])
        column_names = [h[0] for h in sorted_headers]
        column_positions = [h[1] for h in sorted_headers]
        
        print(f"Halaman {page_num + 1}: Header ditemukan di y={header_row_y:.2f}")
        print(f"  Kolom: {column_names}")
        print(f"  Posisi X: {[f'{x:.2f}' for x in column_positions]}")
        
        # Ekstrak rows di bawah header hingga menemukan 'Pesan :'
        data_rows = []
        current_row = {}
        current_y = None
        boundary_found = False
        
        for text_obj in sorted(all_texts, key=lambda x: (x['y0'], x['x0'])):
            # Check if boundary text found
            if boundary_text.lower() in text_obj['text'].lower():
                boundary_found = True
                break
            
            # Skip header row dan text di atasnya
            if text_obj['y0'] <= header_row_y:
                continue
            
            y_pos = text_obj['y0']
            x_pos = text_obj['x0']
            text_val = text_obj['text']
            
            # Jika y berubah jauh, berarti baris baru
            if current_y is not None and abs(y_pos - current_y) > 5:  # threshold 5 points
                if current_row:
                    data_rows.append(current_row)
                current_row = {}
            
            current_y = y_pos
            
            # Tentukan kolom berdasarkan posisi x terdekat dengan column_positions
            closest_col_idx = 0
            min_distance = abs(x_pos - column_positions[0])
            
            for idx, col_x in enumerate(column_positions):
                distance = abs(x_pos - col_x)
                if distance < min_distance:
                    min_distance = distance
                    closest_col_idx = idx
            
            col_name = column_names[closest_col_idx]
            
            # Append text ke kolom (beberapa text mungkin termasuk dalam 1 kolom)
            if col_name in current_row:
                current_row[col_name] += " " + text_val
            else:
                current_row[col_name] = text_val
        
        # Tambahkan row terakhir
        if current_row:
            data_rows.append(current_row)
        
        # **PERBAIKAN: Merge rows yang incomplete (SKU atau Qty kosong)**
        # Logika: Jika ada row dengan SKU kosong tapi Qty ada, merge dengan row sebelumnya yang punya SKU
        merged_rows = []
        i = 0
        while i < len(data_rows):
            current = data_rows[i]
            current_sku = current.get('SKU', '').strip()
            current_qty = current.get('Qty', '').strip()
            
            # Jika SKU kosong dan ada row sebelumnya dengan SKU, merge ke row sebelumnya
            if not current_sku and merged_rows:
                prev_row = merged_rows[-1]
                prev_sku = prev_row.get('SKU', '').strip()
                prev_qty = prev_row.get('Qty', '').strip()
                
                # Jika row sebelumnya punya SKU dan Qty kosong, gunakan Qty dari row ini
                if prev_sku and not prev_qty and current_qty:
                    prev_row['Qty'] = current_qty
                    print(f"  → Merged row dengan SKU kosong ke row sebelumnya: SKU={prev_sku}, Qty={current_qty}")
                    i += 1
                    continue
                # Jika row sebelumnya punya SKU dan sudah lengkap, tambah row ini sebagai baru
                elif prev_sku and prev_qty:
                    merged_rows.append(current)
                    i += 1
                    continue
            
            # Jika Qty kosong dan ada row sebelumnya dengan Qty, skip dan merge ke sebelumnya
            if not current_qty and current_sku and merged_rows:
                prev_row = merged_rows[-1]
                prev_qty = prev_row.get('Qty', '').strip()
                prev_sku = prev_row.get('SKU', '').strip()
                
                # Jika row sebelumnya punya Qty tapi SKU kosong, update SKU
                if prev_qty and not prev_sku:
                    prev_row['SKU'] = current_sku
                    print(f"  → Merged SKU ke row sebelumnya: SKU={current_sku}, Qty={prev_qty}")
                    i += 1
                    continue
            
            # Jika row lengkap atau tidak ada matching sebelumnya, tambah apa adanya
            merged_rows.append(current)
            i += 1
        
        data_rows = merged_rows
        
        # Normalisasi rows - ensure semua kolom ada
        for row in data_rows:
            normalized_row = {}
            for col in column_names:
                normalized_row[col] = row.get(col, '').strip()
            page_data['rows'].append(normalized_row)
        
        table_data.append(page_data)
        print(f"  Rows extracted: {len(data_rows)}")
        print(f"  Boundary ('{boundary_text}') found: {boundary_found}\n")
    
    src.close()
    
    if not table_data:
        print("Tidak ditemukan data tabel di PDF")
    
    return table_data

def get_rows_by_page(table_data, page_number):
    for page in table_data:
        if page['page'] == page_number:
            return page['rows']
    return []

def extract_sku_qty_columns(table_data, page=None):
    """
    Ambil SKU dan Qty dari halaman tertentu
    
    Args:
        table_data: hasil extract_table_data()
        page: nomor halaman yang ingin diambil
              None = semua halaman
    """

    sku_list = []
    qty_list = []
    combined_list = []

    total_quantity = 0

    for page_info in table_data:

        # FILTER HALAMAN
        if page is not None and page_info['page'] != page:
            continue

        rows = page_info['rows']

        print(f"Processing page {page_info['page']}")
        print(f"hasil rows =\n{rows}")

        for row in rows:
            sku = row.get('SKU', '').strip()
            qty_str = row.get('Qty', '').strip()

            print(f"Extracted SKU: '{sku}', Qty: '{qty_str}'")

            try:
                qty = int(qty_str) if qty_str else 0
            except ValueError:
                qty = 0

            if sku:

                # default qty = 1
                if qty == 0 and not qty_str:
                    qty = 1
                    print(f"  → Qty kosong untuk SKU '{sku}', set default ke 1")

                sku_list.append(sku)
                qty_list.append(qty)

                combined_list.append({
                    'sku': sku,
                    'qty': qty
                })

                total_quantity += qty

    result = {
        'sku': sku_list,
        'qty': qty_list,
        'combined': combined_list,
        'total_items': len(sku_list),
        'total_quantity': total_quantity
    }

    return result

def find_text_and_add_text(page, search_text, insert_text, offset_x=0, offset_y=0, 
                            reference_point="x0", fontsize=12, fontname="Times-Bold", 
                            color=(0, 0, 0), fallback_x=10, fallback_y=20):
    """
    Mencari teks tertentu di halaman, kemudian memasukkan teks lain 
    dengan offset x dan y dari posisi teks yang ditemukan
    
    Jika teks tidak ditemukan (halaman kosong), stamp ditambahkan di posisi fallback
    
    Args:
        page: Halaman PDF (fitz.Page object)
        search_text: Teks yang akan dicari
        insert_text: Teks yang akan dimasukkan
        offset_x: Offset horizontal dari posisi yang ditemukan (default: 0)
        offset_y: Offset vertikal dari posisi yang ditemukan (default: 0)
        reference_point: Titik referensi - 'x0', 'x1', 'y0', 'y1', 'tl', 'tr', 'bl', 'br' (default: 'x0')
        fontsize: Ukuran font (default: 12)
        fontname: Nama font (default: "Times-Bold")
        color: Warna RGB (default: (0, 0, 0) = hitam)
        fallback_x: Koordinat X fallback untuk halaman kosong (default: 10)
        fallback_y: Koordinat Y fallback untuk halaman kosong (default: 20)
    
    Returns:
        dict: Info tentang teks yang ditemukan dan teks yang dimasukkan, atau None jika tidak ditemukan
    """
    text_instances = page.search_for(search_text)
    
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
            'is_fallback': True,
            'reference_point': reference_point,
            'offset': {'x': offset_x, 'y': offset_y}
        }
        
        print(f"✓ Stamp ditambahkan di fallback position ({fallback_x}, {fallback_y})")
        return result
    
    inst = text_instances[0]  # Ambil instance pertama
    
    # Tentukan titik referensi
    reference_map = {
        'x0': (inst.x0, inst.y0),
        'x1': (inst.x1, inst.y0),
        'y0': (inst.x0, inst.y0),
        'y1': (inst.x0, inst.y1),
        'tl': inst.tl,  # top-left
        'tr': inst.tr,  # top-right
        'bl': inst.bl,  # bottom-left
        'br': inst.br,  # bottom-right
    }
    
    ref_point = reference_map.get(reference_point, inst.tl)
    
    # Hitung posisi akhir
    final_x = ref_point[0] + offset_x
    final_y = ref_point[1] + offset_y
    
    # Masukkan teks
    page.insert_text(
        (final_x, final_y),
        insert_text,
        fontsize=fontsize,
        fontname=fontname,
        color=color
    )
    
    result = {
        'search_text': search_text,
        'insert_text': insert_text,
        'found_at': {
            'x0': inst.x0,
            'y0': inst.y0,
            'x1': inst.x1,
            'y1': inst.y1
        },
        'inserted_at': {
            'x': final_x,
            'y': final_y
        },
        'reference_point': reference_point,
        'offset': {'x': offset_x, 'y': offset_y},
        'is_fallback': False
    }
    
    print(f"Ditemukan '{search_text}' di ({inst.x0:.2f}, {inst.y0:.2f})")
    print(f"Memasukkan '{insert_text}' di ({final_x:.2f}, {final_y:.2f})")
    
    return result

def insert_text_at_position(page, text, x, y, fontsize=12, fontname="Times-Bold", 
                            color=(0, 0, 0), with_border=False, border_color=(0, 0, 0), 
                            border_width=1, padding=2):
    """
    Memasukkan teks pada koordinat tertentu dengan setting lengkap
    
    Args:
        page: Halaman PDF (fitz.Page object)
        text: Teks yang akan dimasukkan
        x: Koordinat x
        y: Koordinat y
        fontsize: Ukuran font (default: 12)
        fontname: Nama font (default: "Times-Bold")
        color: Warna RGB (default: (0, 0, 0) = hitam)
        with_border: Tambahkan border/kotak (default: False)
        border_color: Warna border (default: (0, 0, 0) = hitam)
        border_width: Tebal garis border (default: 1)
        padding: Jarak padding dari text ke border (default: 2)
    
    Returns:
        dict: Info tentang teks yang dimasukkan
    """
    if with_border:
        # Hitung lebar text untuk membuat border
        text_width = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
        text_height = fontsize
        
        # Buat rectangle untuk border
        rect = fitz.Rect(
            x - padding,
            y - text_height - padding,
            x + text_width + padding,
            y + padding
        )
        
        # Gambar kotak
        page.draw_rect(
            rect,
            color=border_color,
            width=border_width
        )
    
    # Masukkan teks
    page.insert_text(
        (x, y),
        text,
        fontsize=fontsize,
        fontname=fontname,
        color=color
    )
    
    result = {
        'text': text,
        'position': {'x': x, 'y': y},
        'fontsize': fontsize,
        'fontname': fontname,
        'color': color,
        'with_border': with_border
    }
    
    print(f"Memasukkan '{text}' di ({x:.2f}, {y:.2f})")
    
    return result

def extract_resi_number(input_pdf, pattern="No. Resi:"):
    """
    Mencari dan mengekstrak nomor resi dari PDF
    Mengambil teks setelah ': ' (colon dan space)
    
    Args:
        input_pdf: Path ke file PDF input
        pattern: Pattern yang dicari (default: "No. Resi:")
    
    Returns:
        List berisi nomor resi yang ditemukan
    """
    src = fitz.open(input_pdf)
    resi_list = []
    
    for page_num, page in enumerate(src):
        text = page.get_text()
        
        # Cari pattern "No. Resi: XXXXX"
        matches = re.finditer(rf"{re.escape(pattern)}\s*([^\n\s]+)", text)
        
        for match in matches:
            resi_number = match.group(1)  # Ambil text setelah pattern dan space
            resi_list.append({
                'page': page_num + 1,
                'pattern': pattern,
                'number': resi_number,
                'full_text': match.group(0)
            })
            print(f"Halaman {page_num + 1}: Ditemukan '{pattern}' → {resi_number}")
    
    src.close()
    
    if not resi_list:
        print(f"Tidak ditemukan pattern '{pattern}' di PDF")
    else:
        print(f"\nTotal ditemukan: {len(resi_list)} resi")
    
    return resi_list

def remove_pages_with_text(input_pdf, search_text, output_pdf):
    src = fitz.open(input_pdf)
    dst = fitz.open()

    removed_count = 0

    try:
        for page_num, page in enumerate(src):
            text = page.get_text()

            if search_text.upper() in text.upper():
                print(f"Menghapus halaman {page_num + 1}: Ditemukan '{search_text}'")
                removed_count += 1
            else:
                dst.insert_pdf(src, from_page=page_num, to_page=page_num)

        # SAVE KE TEMP FILE DULU
        temp_file = output_pdf + ".tmp.pdf"

        dst.save(temp_file)

        dst.close()
        src.close()

        # Replace setelah semua close
        os.replace(temp_file, output_pdf)

        print(f"Removed {removed_count} halaman")
    
    except Exception as e:
        print(f"Error in remove_pages_with_text: {e}")
        dst.close()
        src.close()
        
        # Cleanup temp file jika ada error
        temp_file = output_pdf + ".tmp.pdf"
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"  ✓ Temp file cleanup: {temp_file}")
            except Exception as cleanup_error:
                print(f"  ⚠ Gagal menghapus temp file: {cleanup_error}")
        
        raise  # Re-raise exception


def remove_pages_by_number(input_pdf, output_pdf, page_numbers):
    """
    Hapus halaman berdasarkan nomor halaman tertentu
    
    Args:
        input_pdf: Path ke file PDF input
        output_pdf: Path ke file PDF output
        page_numbers: List berisi nomor halaman yang akan dihapus (1-indexed)
        
    Example:
        remove_pages_by_number("input.pdf", "output.pdf", [2, 5, 7])
    """
    src = fitz.open(input_pdf)
    dst = fitz.open()
    
    removed_count = 0
    total_pages = len(src)  # Save sebelum close
    
    try:
        for page_num in range(total_pages):
            # page_num adalah 0-indexed, tapi page_numbers adalah 1-indexed
            current_page_number = page_num + 1
            
            if current_page_number in page_numbers:
                print(f"  🗑️  Menghapus halaman {current_page_number}")
                removed_count += 1
            else:
                dst.insert_pdf(src, from_page=page_num, to_page=page_num)
        
        # Save ke output
        temp_file = output_pdf + ".tmp.pdf"
        dst.save(temp_file)
        
        dst.close()
        src.close()
        
        # Replace setelah semua close
        os.replace(temp_file, output_pdf)
        
        print(f"✓ Berhasil menghapus {removed_count} halaman dari total {total_pages}")
    
    except Exception as e:
        print(f"Error in remove_pages_by_number: {e}")
        dst.close()
        src.close()
        
        # Cleanup temp file jika ada error
        temp_file = output_pdf + ".tmp.pdf"
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"  ✓ Temp file cleanup: {temp_file}")
            except Exception as cleanup_error:
                print(f"  ⚠ Gagal menghapus temp file: {cleanup_error}")
        
        raise  # Re-raise exception agar bisa ditangani di caller


# ====================================
def split_pdf_remove_blank(input_pdf, output_pdf):
    # input_pdf = "split2.pdf"
    # output_pdf = "output_split.pdf"

    # Ukuran kertas: 4.14 × 5.83 inch (converted to PDF points: 1 inch = 72 points)
    PAGE_WIDTH = 4.14 * 72  # 297.68 points
    PAGE_HEIGHT = 5.83 * 72  # 419.76 points

    src = fitz.open(input_pdf)
    dst = fitz.open()

    for page in src:
        rect = page.rect

        width = rect.width
        height = rect.height

        mid_x = width / 2

        # =========================
        # Bagian kiri
        # =========================
        left_rect = fitz.Rect(0, 0, mid_x, height)

        new_page = dst.new_page(
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )

        # render + rotate
        new_page.show_pdf_page(
            new_page.rect,
            src,
            page.number,
            clip=left_rect,
            rotate=0
        )

        # =========================
        # Bagian kanan
        # =========================
        right_rect = fitz.Rect(mid_x, 0, width, height)

        new_page = dst.new_page(
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )

        new_page.show_pdf_page(
            new_page.rect,
            src,
            page.number,
            clip=right_rect,
            rotate=0
        )      
        
            
            



    dst.save(output_pdf)
    dst.close()
    src.close()
    remove_pages_with_text(output_pdf, "DAFTAR PRODUK", output_pdf)

def convert_config(response):
    return {
        item['sku']: item['items']
        for item in response.get('config', [])
    }
    # return split_map
    # if not isinstance(config_data, list):
    #     return {}

    # return {
    #     item.get('sku'): item.get('items', [])
    #     for item in config_data
    #     if isinstance(item, dict) and item.get('sku')
    # }

def crop_pdf_until_marker(
    input_pdf,
    output_pdf,
    # marker="# Nama Produk SKU Lokasi Variasi Qty"
    marker="SKU"
):
    doc = fitz.open(input_pdf)
    output = fitz.open()

    for page in doc:
        rects = page.search_for(marker)

        if rects:
            print(f"Marker ditemukan di halaman {page.number + 1} pada posisi {rects[0]}")
            marker_rect = rects[0]

            # area yang dipertahankan:
            # dari atas halaman sampai tepat sebelum marker
            crop_rect = fitz.Rect(
                page.rect.x0,
                page.rect.y0,
                page.rect.x1,
                marker_rect.y0
            )

            new_page = output.new_page(
                width=crop_rect.width,
                height=crop_rect.height
            )

            new_page.show_pdf_page(
                fitz.Rect(0, 0, crop_rect.width, crop_rect.height),
                doc,
                page.number,
                clip=crop_rect
            )
        else:
            # jika marker tidak ditemukan, salin halaman apa adanya
            print(f"Marker tidak ditemukan di halaman {page.number + 1} → menyimpan halaman apa adanya")
            new_page = output.new_page(
                width=page.rect.width,
                height=page.rect.height
            )

            new_page.show_pdf_page(
                new_page.rect,
                doc,
                page.number
            )

    output.save(output_pdf)
    output.close()
    doc.close()

def get_page_orientation(pdf_path, page_num=0):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    rect = page.rect

    if rect.width > rect.height:
        return "landscape"
    elif rect.height > rect.width:
        return "portrait"

def spk_proses(input_pdf, output_pdf, split_map=split_map, codename="ASE", stamp_color=(0, 0, 0), stamp_fontsize=9):
    """
    Proses PDF dengan stamp teks yang bisa dikustomisasi
    Halaman dengan fallback position (halaman kosong) akan dihapus
    
    Args:
        input_pdf: Path ke file PDF input
        output_pdf: Path ke file PDF output
        split_map: Mapping untuk split SKU
        codename: Kode nama produk (default: "ASE")
        stamp_color: Warna stamp dalam RGB tuple (default: (0, 0, 0) = hitam)
        stamp_fontsize: Ukuran font stamp (default: 9)
    
    Examples:
        # Warna hitam (default)
        spk_proses(input_pdf, output_pdf)
        
        # Warna merah (Shopee)
        spk_proses(input_pdf, output_pdf, stamp_color=(255, 0, 0))
        
        # Warna biru (TikTok)
        spk_proses(input_pdf, output_pdf, stamp_color=(0, 0, 255))
    """
    cek_orientation = get_page_orientation(input_pdf)
    if cek_orientation == "landscape":
        try:
            split_pdf_remove_blank(input_pdf, output_pdf)
        except Exception as e:
            print(f"⚠ Gagal memproses PDF landscape: {e}")
    else:
        marker = "SPX"
        marker2 = "Retur"
        src1 = fitz.open(input_pdf)
        for page in src1:
            rects = page.search_for(marker)
            rects2 = page.search_for(marker2)   
            if not rects or rects2:
                print(f"Marker '{marker}' tidak ditemukan di halaman {page.number + 1} → menyimpan halaman apa adanya")
                raise Exception(f"Periksa File Tidak cocok dengan Format Shopee yang di tentukan. {marker} tidak ditemukan")
            else:
                print(f"Marker '{marker}' ditemukan di halaman {page.number + 1} pada posisi {rects[0]}")
                src1.save(output_pdf)
        src1.close()
    try :
        table_data = extract_table_data(output_pdf)
        print(f"Extracted table data:\n{table_data}\n")
        resi = extract_resi_number(output_pdf)
        src = fitz.open(output_pdf)
        copy_resi = []
        pages_to_remove = []  # Track pages dengan fallback position
        
        for page_num, page in enumerate(src):
            page_number = page_num + 1
            resi_number = None
            # Boundary check: pastikan indeks ada dalam list resi
            if page_number - 1 < len(resi) and resi[page_number - 1]['page'] == page_number:
                resi_number = resi[page_number - 1]['number']
                print(f"Halaman {page_number}: Menambahkan resi '{resi_number}'")
            rows = get_rows_by_page(table_data, page_number)
            print(f"Rows on page {page_number}:")
            for row in rows:
                print(row)

            # Extract SKU and Quantity columns
            sku_qty_data = extract_sku_qty_columns(table_data, page=page_number)
            print("\nExtracted SKU and Quantity columns:")
            print(sku_qty_data)
            combined_result = combine_items(sku_qty_data['sku'], sku_qty_data['qty'], split_map)
            print(f"\nCombined SKU and Quantity:")
            print(combined_result)
            text_produk = format_produk_text(combined_result,codename)
            text_copy = format_copy_text(combined_result, prefix=resi_number if resi_number else "")
            print(f"\nFormatted Produk Text: {text_produk}")
            print(f"Formatted Copy Text: {text_copy}")
            if combined_result:
                copy_resi.append(text_copy)
            result = find_text_and_add_text(page, "No.Pesanan: ", f"{text_produk}", offset_x=100, offset_y=-3, fontsize=stamp_fontsize, color=stamp_color)
            if result:
                if result.get('is_fallback'):
                    print(f"⚠ Stamp ditambahkan di fallback position (halaman kosong) - halaman {page_number}")
                    pages_to_remove.append(page_number)  # Tandai halaman untuk dihapus
                else:
                    print(f"✓ Stamp berhasil ditambahkan di posisi normal - halaman {page_number}")
            else:
                print(f"✗ Gagal menambahkan stamp di halaman {page_number}")
        
        # Save to temp file then replace original (untuk handle encrypted PDF)
        temp_output = output_pdf + "_temp"
        src.save(temp_output)
        src.close()
        
        # Hapus halaman yang menggunakan fallback position
        if pages_to_remove:
            print(f"\n🗑️  Menghapus {len(pages_to_remove)} halaman dengan fallback position: {pages_to_remove}")
            remove_pages_by_number(temp_output, output_pdf, pages_to_remove)
            # Hapus file temp yang sudah tidak dipakai
            if os.path.exists(temp_output):
                os.remove(temp_output)
                print(f"  ✓ File temp dihapus: {temp_output}")
        else:
            os.replace(temp_output, output_pdf)
        
        print(f"\n✓ PDF berhasil disimpan: {output_pdf}")
        try:
            temp_pdf = output_pdf.replace(".pdf", "_temp.pdf")
            crop_pdf_until_marker(output_pdf, temp_pdf)
            # replace file lama
            os.replace(temp_pdf, output_pdf)
            #crop_pdf_until_marker(output_pdf, output_pdf)
            print(f"✓ PDF berhasil dipotong hingga marker")
        except Exception as crop_error:
            print(f"⚠ Gagal memotong PDF: {crop_error}")
        return copy_resi
    except Exception as e:
        print(f"{e}")
        # Cleanup temp files jika ada error
        temp_files = [output_pdf + "_temp", output_pdf + ".tmp.pdf"]
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"  ✓ Temp file cleanup: {temp_file}")
                except Exception as cleanup_error:
                    print(f"  ⚠ Gagal menghapus temp file {temp_file}: {cleanup_error}")
        return []


if __name__ == '__main__':
    input_pdf = "split_asal.pdf"
    # input_pdf = "Shopee Seller Centre.pdf"
    output_pdf = "output_split.pdf"
    hasil = spk_proses(input_pdf, output_pdf, split_map=split_map, codename="ASE")
    print("\nCopy Resi:")
    for copy in hasil:
        print(copy)
    print(split_map)

    response = {'status': 'success', 'data': {'token': 'VTOX-S4YS-BK08-LXQD', 'is_expired': False, 'remaining_days': 6, 'app_code': 'ARON', 'expired_at': '2026-05-20', 'package_title': 'Trial', 'codename': 'AGS', 'max_devices': 1, 'used_devices': 1, 'remaining_devices': 0, 'profile_name': 'Agis Maulana', 'account_email': 'kangagis02@gmail.com', 'website_url': 'https://duadev.xyz'}, 'config': [{'sku': 'SQUWNT', 'items': ['SQU', 'WNT']}, {'sku': 'CBO', 'items': ['IFI', 'SPJ']}, {'sku': 'AGS', 'items': ['CSH', 'WNT']}]}
    split_map = {
        item['sku']: item['items']
        for item in response.get('config', [])
    }
    print(split_map)
    chek = convert_config(response)
    print(chek)