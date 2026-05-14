import fitz  # pymupdf
import re
from collections import defaultdict
import os

def combine_items(items, values, split_map):
    result = defaultdict(int)

    for item, value in zip(items, values):
        key = item.upper()

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
                            color=(0, 0, 0)):
    """
    Mencari teks tertentu di halaman, kemudian memasukkan teks lain 
    dengan offset x dan y dari posisi teks yang ditemukan
    
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
    
    Returns:
        dict: Info tentang teks yang ditemukan dan teks yang dimasukkan, atau None jika tidak ditemukan
    """
    text_instances = page.search_for(search_text)
    
    if not text_instances:
        print(f"Teks '{search_text}' tidak ditemukan di halaman")
        return None
    
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
        'offset': {'x': offset_x, 'y': offset_y}
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
    """
    Menghapus halaman yang mengandung teks tertentu dari PDF
    
    Args:
        input_pdf: Path ke file PDF input
        search_text: Teks yang dicari (misalnya: "DAFTAR PRODUK")
        output_pdf: Path ke file PDF output
    """
    src = fitz.open(input_pdf)
    dst = fitz.open()
    
    removed_count = 0
    total_pages = len(src)
    
    for page_num, page in enumerate(src):
        # Cari teks di halaman
        text = page.get_text()
        
        if search_text.upper() in text.upper():
            print(f"Menghapus halaman {page_num + 1}: Ditemukan '{search_text}'")
            removed_count += 1
        else:
            # find_text_and_add_text(page, "No.Pesanan: ", "HERBAL", offset_x=150, offset_y=20)
            # Copy halaman ke dokumen baru jika tidak mengandung teks yang dicari
            dst.insert_pdf(src, from_page=page_num, to_page=page_num)
            
    
    dst.save(output_pdf)
    dst.close()
    src.close()

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

def spk_proses(input_pdf, output_pdf):
    split_map = {
        "SQUWNT": ["SQU", "WNT"],
        "IFISPJ": ["IFI", "SPJ"],
        "KLRNSQU": ["KLRN", "SQU"],
        "CSHWNT": ["CSH", "WNT"]
}

    split_pdf_remove_blank(input_pdf, output_pdf)
    table_data = extract_table_data(output_pdf)
    print(f"Extracted table data:\n{table_data}\n")
    resi = extract_resi_number(output_pdf)
    src = fitz.open(output_pdf)
    copy_resi = []
    for page_num, page in enumerate(src):
        page_number = page_num + 1
        resi_number = None
        if resi[page_number - 1]['page'] == page_number:
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
        text_produk = format_produk_text(combined_result)
        text_copy = format_copy_text(combined_result, prefix=resi_number if resi_number else "")
        print(f"\nFormatted Produk Text: {text_produk}")
        print(f"Formatted Copy Text: {text_copy}")
        copy_resi.append(text_copy)
        result = find_text_and_add_text(page, "No.Pesanan: ", f"{text_produk}", offset_x=130, offset_y=20, fontsize=12)
        if result:
            print(f"✓ Stamp Lunas berhasil ditambahkan di halaman {page_number}")
        else:
            print(f"✗ Pattern 'No.Pesanan: ' tidak ditemukan di halaman {page_number}")
    
    # Save to temp file then replace original (untuk handle encrypted PDF)
    temp_output = output_pdf + "_temp"
    src.save(temp_output)
    src.close()
    os.replace(temp_output, output_pdf)
    print(f"\n✓ PDF berhasil disimpan: {output_pdf}")
    return copy_resi


if __name__ == '__main__':
    input_pdf = "split_asal.pdf"
    output_pdf = "output_split.pdf"
    hasil = spk_proses(input_pdf, output_pdf)
    print("\nCopy Resi:")
    for copy in hasil:
        print(copy)