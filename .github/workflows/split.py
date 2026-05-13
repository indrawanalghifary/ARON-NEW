import fitz  # pymupdf
import re
# from fitz import Rect, Page, open, Document

def find_get_koordinat(page, text:str, nilai:str='x0'):
    """
    menemukan koordinat sebuah text
    (x0,y0)-----------(x1,y0)
    |                 |
    |     TEKS        |
    |                 |
    (x0,y1)-----------(x1,y1)
    area = fitz.Rect(inst.x0, inst.y0, inst.x1, inst.y1)
    """
    
    text_instances = page.search_for(text)
    
    for inst in text_instances:
        print("Koordinat:", inst)
        # text_inside = page.get_text("text", clip=inst)
        if nilai == 'x0' :
            return inst.x0
        if nilai == 'x1' :
            return inst.x1
        if nilai == 'y0' :
            return inst.y0
        if nilai == 'y1' :
            return inst.y1
        if nilai == 'tl' :
            return inst.tl
        if nilai == 'bl' :
            return inst.bl
        if nilai == 'br' :
            return inst.br
        if nilai == 'tr' :
            return inst.tr

def add_stamp(page, text, x, y, size=12):
    # padding = 4

    # # hitung lebar text
    # text_width = fitz.get_text_length(
    #     text,
    #     fontname="Times-Bold",
    #     fontsize=size
    # )

    # # estimasi tinggi text
    # text_height = size

    # # buat rectangle
    # rect = fitz.Rect(
    #     x - padding,
    #     y - text_height - padding,
    #     x + text_width + padding,
    #     y + padding
    # )

    # # gambar kotak
    # page.draw_rect(
    #     rect,
    #     color=(0, 0, 0),   # border hitam
    #     width=1
    # )

    # tulis text
    page.insert_text(
        (x, y),
        text,
        fontsize=size,
        fontname="Times-Bold",
        color=(0, 0, 0)
    )

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

def search_and_extract_resi(input_pdf, resi_keyword="SPXID"):
    """
    Mencari nomor resi dengan keyword tertentu
    
    Args:
        input_pdf: Path ke file PDF input
        resi_keyword: Keyword yang dicari (default: "SPXID")
    
    Returns:
        List berisi nomor resi yang cocok dengan keyword
    """
    resi_list = extract_resi_number(input_pdf)
    filtered_list = [resi for resi in resi_list if resi_keyword in resi['number']]
    
    print(f"\nFilter '{resi_keyword}': {len(filtered_list)} hasil")
    return filtered_list

def extract_sku_region(input_pdf, output_dir="extracted_sku"):
    """
    Ekstrak area SKU dengan kriteria spesifik:
    - Left: Tepat dibawah "SKU" + 5 padding
    - Top: Sejajar dengan number/baris "1"
    - Right: Sejajar dengan "Variasi" + 10 padding
    - Bottom: Jika ada baris 2, gunakan baris 3. Jika ada baris 3, gunakan baris 4, dst.
    
    Args:
        input_pdf: Path ke file PDF input
        output_dir: Direktori untuk menyimpan hasil crop
    
    Returns:
        List berisi info area yang di-extract
    """
    import os
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    src = fitz.open(input_pdf)
    extracted_regions = []
    
    for page_num, page in enumerate(src):
        # Dapatkan text blocks dengan posisi koordinat
        text_dict = page.get_text("dict")
        
        sku_pos = None  # Posisi "SKU" untuk referensi kiri
        variasi_pos = None  # Posisi "Variasi" untuk referensi kanan
        row_positions = {}  # Dict untuk menyimpan posisi baris {nomor: bbox}
        
        # Cari posisi dari berbagai elemen penting
        for block in text_dict["blocks"]:
            if block["type"] == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"].strip()
                        bbox = span["bbox"]  # (x0, y0, x1, y1)
                        
                        if text == "SKU":
                            sku_pos = bbox
                        elif text == "Variasi":
                            variasi_pos = bbox
                        
                        # Cari semua baris bernomor (1, 2, 3, 4, dst)
                        if text.isdigit():
                            row_num = int(text)
                            if row_num not in row_positions:
                                row_positions[row_num] = bbox
        
        # Jika semua elemen ditemukan, hitung bounding box
        if sku_pos and variasi_pos and row_positions:
            # Koordinat:
            # Left: "SKU" x0 - 5 (padding kiri)
            # Top: sejajar dengan row "1" (y0)
            # Right: "Variasi" x0 + 10 (padding kanan)
            # Bottom: gunakan baris berikutnya dari row terbesar
            
            left = sku_pos[0] - 5
            
            # Top dari row 1
            if 1 in row_positions:
                top = row_positions[1][1]
            else:
                top = variasi_pos[3] + 5  # Jika row 1 tidak ada, gunakan bawah header + margin
            
            right = variasi_pos[0] + 10
            
            # Tentukan bottom: gunakan baris berikutnya dari row terbesar
            sorted_rows = sorted(row_positions.keys())
            max_row = max(sorted_rows)
            
            # Cari baris berikutnya (max_row + 1)
            next_row = max_row + 1
            
            if next_row in row_positions:
                # Jika ada baris berikutnya, gunakan posisinya
                bottom = row_positions[next_row][1]
            else:
                # Jika tidak ada baris berikutnya, gunakan teks "spx" atau tinggi page
                spx_pos = None
                for block in text_dict["blocks"]:
                    if block["type"] == 0:
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                text = span["text"].strip()
                                if text.lower().startswith("spx"):
                                    spx_pos = span["bbox"]
                                    break
                
                if spx_pos:
                    bottom = spx_pos[1]
                else:
                    bottom = page.rect.height
            
            # Create rect
            crop_rect = fitz.Rect(left, top, right, bottom)
            
            # Render dan simpan
            pix = page.get_pixmap(clip=crop_rect, alpha=False)
            output_path = os.path.join(output_dir, f"sku_page{page_num + 1}.png")
            pix.save(output_path)
            
            extracted_regions.append({
                'page': page_num + 1,
                'coordinates': {
                    'left': left,
                    'top': top,
                    'right': right,
                    'bottom': bottom,
                    'width': right - left,
                    'height': bottom - top
                },
                'rows_found': sorted_rows,
                'boundary_row': next_row,
                'output_file': output_path
            })
            
            print(f"Halaman {page_num + 1}: Ekstrak SKU (baris {sorted_rows[0]}-{max_row}, batas di baris {next_row}) → {output_path}")
    
    src.close()
    
    if not extracted_regions:
        print("Tidak ditemukan area SKU di PDF")
    else:
        print(f"\nTotal area SKU di-extract: {len(extracted_regions)}")
    
    return extracted_regions

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

def print_table_data(table_data, export_to_csv=None):
    """
    Menampilkan data tabel dalam format yang mudah dibaca
    
    Args:
        table_data: Hasil dari extract_table_data()
        export_to_csv: Path file CSV jika ingin export (optional)
    """
    import csv
    
    all_rows = []
    
    for page_info in table_data:
        page_num = page_info['page']
        rows = page_info['rows']
        
        print(f"\n{'='*100}")
        print(f"HALAMAN {page_num}")
        print(f"{'='*100}")
        
        if not rows:
            print("Tidak ada data")
            continue
        
        # Print header
        headers = list(rows[0].keys())
        header_line = " | ".join([f"{h:20}" for h in headers])
        print(header_line)
        print("-" * len(header_line))
        
        # Print rows
        for row in rows:
            row_line = " | ".join([f"{str(row.get(h, '')):20}" for h in headers])
            print(row_line)
            all_rows.append(row)
    
    # Export ke CSV jika diminta
    if export_to_csv and all_rows:
        with open(export_to_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\n✓ Data diekspor ke: {export_to_csv}")

def extract_sku_qty_columns(table_data):
    """
    Mengambil semua isi kolom SKU dan Kolom Qty dari hasil extract_table_data()
    
    Args:
        table_data: Hasil dari extract_table_data()
    
    Returns:
        dict dengan struktur:
        {
            'sku': ['SKU1', 'SKU2', ...],
            'qty': [1, 2, ...],
            'combined': [
                {'sku': 'SKU1', 'qty': 1},
                {'sku': 'SKU2', 'qty': 2},
                ...
            ],
            'total_items': int,
            'total_quantity': int
        }
    """
    sku_list = []
    qty_list = []
    combined_list = []
    
    total_quantity = 0
    
    for page_info in table_data:
        rows = page_info['rows']
        
        for row in rows:
            sku = row.get('SKU', '').strip()
            qty_str = row.get('Qty', '').strip()
            
            # Parse Qty ke integer
            try:
                qty = int(qty_str) if qty_str else 0
            except ValueError:
                qty = 0
            
            # Hanya tambahkan jika SKU tidak kosong
            if sku:
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

def print_sku_qty_data(sku_qty_data, export_to_txt=None):
    """
    Menampilkan data SKU dan Qty dalam format yang mudah dibaca
    
    Args:
        sku_qty_data: Hasil dari extract_sku_qty_columns()
        export_to_txt: Path file TXT jika ingin export (optional)
    """
    print(f"\n{'='*80}")
    print("DAFTAR SKU DAN QUANTITY")
    print(f"{'='*80}")
    print(f"{'No':>4} | {'SKU':30} | {'Qty':>8}")
    print("-" * 80)
    
    for idx, item in enumerate(sku_qty_data['combined'], 1):
        print(f"{idx:4} | {item['sku']:30} | {item['qty']:>8}")
    
    print("-" * 80)
    print(f"Total Items    : {sku_qty_data['total_items']}")
    print(f"Total Quantity : {sku_qty_data['total_quantity']}")
    print(f"{'='*80}\n")
    
    # Export ke TXT jika diminta
    if export_to_txt:
        with open(export_to_txt, 'w', encoding='utf-8') as f:
            f.write("DAFTAR SKU DAN QUANTITY\n")
            f.write("=" * 80 + "\n")
            f.write(f"{'No':>4} | {'SKU':30} | {'Qty':>8}\n")
            f.write("-" * 80 + "\n")
            
            for idx, item in enumerate(sku_qty_data['combined'], 1):
                f.write(f"{idx:4} | {item['sku']:30} | {item['qty']:>8}\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"Total Items    : {sku_qty_data['total_items']}\n")
            f.write(f"Total Quantity : {sku_qty_data['total_quantity']}\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ Data diekspor ke: {export_to_txt}")

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
            find_text_and_add_text(page, "No.Pesanan: ", "HERBAL", offset_x=150, offset_y=20)
            # Copy halaman ke dokumen baru jika tidak mengandung teks yang dicari
            dst.insert_pdf(src, from_page=page_num, to_page=page_num)
            
    
    dst.save(output_pdf)
    dst.close()
    src.close()
    
    print(f"\nTotal halaman: {total_pages}")
    print(f"Halaman dihapus: {removed_count}")
    print(f"Halaman tersisa: {total_pages - removed_count}")
    print(f"Hasil disimpan ke: {output_pdf}")
    return output_pdf



# ====================================
input_pdf = "split2.pdf"
output_pdf = "output_split.pdf"

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
extract_sku_region(output_pdf)
data_table = extract_table_data(output_pdf)
print_table_data(data_table, export_to_csv="output_table.csv")

print("Selesai:", output_pdf)