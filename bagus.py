import fitz

from api_db import SupabaseAPI


def get_db_sku(api:SupabaseAPI):
    table_name = "aron"
    data = api.read_data(table_name)
    if data:
        return data[0]["sku"]
    return {}

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

# def get_text_area(x0,y0,x1,y1):
#     """
#     Mendapatkan text di dalam area bounding box
#     """
#     area = fitz.Rect(x0, y0, x1, y1)

#     text_area = page.get_text("text", clip=area)
#     return text_area

def get_qty(page):
    rects = page.search_for("Qty Total:")
    words = page.get_text("words")  # [x0, y0, x1, y1, "teks", block_no, line_no, word_no]
    qty_value = ""
    for rect in rects:
        for w in words:
            # w[0:4] = koordinat kata, w[4] = teks
            if w[0] > rect.x1 and abs(w[1] - rect.y0) < 5:  
                # kata yang muncul di sebelah kanan (x lebih besar, y sejajar)
                qty_value = w[4]
                return qty_value
            

split_map = {
    "SQUWNT": ["SQU", "WNT"],
    "IFISPJ": ["IFI", "SPJ"],
    "KLRNSQU": ["KLRN", "SQU"],
    "CSHWNT": ["CSH", "WNT"]
}

def process_sku_qty(sku_list, qty_list, split_map=split_map):
    result = {}

    for sku, qty in zip(sku_list, qty_list):
        if sku in split_map:
            parts = split_map[sku]
            # SKU gabungan → qty dibagi rata atau satu-satu?
            # Dari contoh Anda: SQUWNT menjadi SQU 1 dan WNT 1
            for p in parts:
                result[p] = result.get(p, 0) + qty
        else:
            result[sku] = result.get(sku, 0) + qty

    return result



def extract_sku_from_page(page):
    seller_x0 = find_get_koordinat(page,"Seller SKU", "bl")
    seller_x1 = find_get_koordinat(page, "Qty Total", "tl") if find_get_koordinat(page,"Qty Total", "tl") != None else find_get_koordinat(page,"Order ID", "tl")


    seller_area = fitz.Rect(seller_x0 , seller_x1)

    seller_text_area = page.get_text("text", clip=seller_area)
    print(f"SKU = {seller_text_area}")

    hasil_sku = [baris.replace(" ", "") for baris in seller_text_area.split("\n") if baris.strip()]
    return hasil_sku

def extract_qty_from_page(page):
    qty_x0 = find_get_koordinat(page,"Qty\n", "bl")
    qty_x1 = find_get_koordinat(page,"Qty Total", "tr") if find_get_koordinat(page,"Qty Total", "tr") != None else fitz.Point(269.9817199707031, 71.13655090332031) #find_get_koordinat("Order ID", "tr") + 100


    qty_area = fitz.Rect(qty_x0, qty_x1)

    qty_text_area = page.get_text("text", clip=qty_area)

    if qty_text_area == "":
        print(f"QTY {get_qty(page)}")
        # qty.append([get_qty()])
        hasil_qty = [get_qty(page)]
        return hasil_qty

    else :
        print(f" Qty {qty_text_area}")
        hasil_qty = list(filter(None, qty_text_area.split("\n")))
        return hasil_qty

def rectangle_with_padding(page, text, x, y, fontsize:10, padding:5):
    # hitung lebar text
    text_width = fitz.get_text_length(
        text,
        fontname="Helvetica-Bold",
        fontsize=fontsize
    )

    # buat rectangle
    rect = fitz.Rect(
        x - padding,
        y - fontsize - padding,
        x + text_width + padding,
        y + padding
    )

    # gambar kotak
    page.draw_rect(
        rect,
        color=(0, 0, 0),      # border hitam
        width=1
    )

# def add_stamp(page, text, x, y, size=10):
#     page.insert_text(
#         (x, y),
#         text,
#         fontsize=size,
#         fontname="Helvetica-bold",
#         color=(0, 0, 0)
#     )

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



def adding_stamp(page, text):
    jnt = page.search_for("Ship :")
    if jnt:
        print("ketemu JNT")
        cod_rect = jnt[0]
        print(f"Koordinat JNT : {cod_rect}")
        x = cod_rect.x1 + 10
        y = cod_rect.y0 + 25
        add_stamp(page,text, x, y)
    

    gtl = page.search_for("TT Order ID")
    if gtl :
        print("ketemu GTL")
        cod_rect = gtl[0]
        print(f"Koordinat GTL : {cod_rect}")
        x = cod_rect.x1 - 35
        y = cod_rect.y0 - 25
        add_stamp(page,text, x, y)

    instant = page.search_for("Pickup Code:")
    if instant :
        print("ketemu Instant")
        cod_rect = instant[0]
        print(f"Koordinat Instant : {cod_rect}")
        x = cod_rect.x1 - 75
        y = cod_rect.y0 + 30
        add_stamp(page,text, x, y)
    

    sicepat = page.search_for("Order ID")
    sicepat1 = page.search_for("Ke(penerima)")
    if sicepat and sicepat1 :
        print("ketemu Sicepat")
        cod_rect = sicepat[0]
        print(f"Koordinat Sicepat : {cod_rect}")
        x = cod_rect.x1 - 20
        y = cod_rect.y0 - 10
        add_stamp(page,text, x, y)

    print("Mencari Stamp Selesai")

def tracking_number(page):
    tr = find_get_koordinat(page, "Tracking Number:", "tr")
    x1 = find_get_koordinat(page, "Tracking Number:", "x1")
    y1 = find_get_koordinat(page, "Tracking Number:", "y1")

    area = fitz.Rect(tr, x1 + 200, y1  )

    tracking = page.get_text("text", clip=area)
    print(tracking.strip())
    return tracking.strip()

def save_edited(output_file, doc) :                
    new_doc = fitz.open()

    for page_num, page in enumerate(doc):
        # Periksa jika nomor halaman adalah ganjil (indeks halaman dimulai dari 0)
        if (page_num + 1) % 2 != 0:
            # Salin halaman ganjil ke dokumen baru
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    new_doc.save(output_file)
    new_doc.close()

def main(pdf_path, out_path, api:SupabaseAPI):
    split_map = get_db_sku(api)

    doc = fitz.open(pdf_path)

    resi = []
    stempel = []

    for i in range(1, len(doc), 2):  # i = 1,3,5… (halaman ganjil)
        try:
            print(f"Memproses halaman: Ganjil {i}, Genap {i+1}")
            page_ganjil = doc[i - 1]     # halaman 1,3,5…
            page_genap  = doc[i]         # halaman 2,4,6…

            # --- ambil data dari halaman genap ---
            raw_sku = extract_sku_from_page(page_genap)
            raw_qty = extract_qty_from_page(page_genap)
            tracking = tracking_number(page_genap)
            

            # sku_list = raw_sku.split()
            # qty_list = list(map(int, raw_qty.split()))
            sku_list = raw_sku
            print(f"SKU List: {sku_list}")
            qty_list = list(map(int, raw_qty))

            # --- proses SKU & QTY ---
            combined = process_sku_qty(sku_list, qty_list, split_map)

            # Format teks untuk stamp: "SQU 2 WNT 2 ..."
            stamp_text = " ".join(f"{v} {k}" for k, v in combined.items()) 
            res_text = ",".join(f"{v},{k}" for k, v in combined.items()) 
            print(f"Stamp Text: {stamp_text}")
            stempel.append(stamp_text)
            res = tracking + "," + res_text
            resi.append(res)

            # --- tempelkan ke halaman ganjil ---
            adding_stamp(page_ganjil, stamp_text + " - ASE")
            print(f"Processed page pair: Ganjil {i}, Genap {i+1}\n")
            print("=====================================")
        except Exception as e:
            print(f"Error memproses halaman {i} dan {i+1}: {e}")
    print(resi)
    print(stempel)
    # doc.save(out_path)
    save_edited(out_path, doc)
    doc.close()
    return resi


if __name__ == "__main__":
    supabase_url = "https://shhtzvevhywlixllklmm.supabase.co/"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNoaHR6dmV2aHl3bGl4bGxrbG1tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU4NDEwMjcsImV4cCI6MjA3MTQxNzAyN30.xTGInN9vGZEyEbFivNRbXXdiE1IH1WVA1Oxd8IY5t-A"
    api = SupabaseAPI(supabase_url, supabase_key)
    user = api.sign_in("indra@mail.com", "@Indraone22")
    # input_pdf = "CONTOH PESANAN GABUNGAN.pdf"
    # input_pdf = "PAKETAN X2.pdf"
    # input_pdf = "CONTOH INSTANT.pdf"
    # input_pdf = "all.pdf"
    input_pdf = "./hasil_gabungan.pdf"
    # input_pdf = "sicepat.pdf"
    output_pdf = "output.pdf"
    main(input_pdf, output_pdf, api)
