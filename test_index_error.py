#!/usr/bin/env python3
"""
Test script untuk debugging error "list index out of range"

Masalah: Error terjadi ketika jumlah halaman > jumlah resi entries
Solusi: Tambah boundary check sebelum akses resi[page_number - 1]
"""

import fitz
import re
from split import extract_resi_number

def create_multipage_test_pdf():
    """Membuat PDF dengan banyak halaman tetapi hanya sedikit resi"""
    doc = fitz.open()
    
    # Halaman 1: Dengan No. Resi:
    page1 = doc.new_page()
    page1.insert_text((50, 50), "No. Resi: RESI001", fontsize=12)
    page1.insert_text((50, 100), "Halaman 1 - Ada resi", fontsize=10)
    
    # Halaman 2: Dengan No. Resi:
    page2 = doc.new_page()
    page2.insert_text((50, 50), "No. Resi: RESI002", fontsize=12)
    page2.insert_text((50, 100), "Halaman 2 - Ada resi", fontsize=10)
    
    # Halaman 3: TANPA No. Resi: (akibat split, bisa kosong)
    page3 = doc.new_page()
    page3.insert_text((50, 100), "Halaman 3 - Kosong (tanpa resi)", fontsize=10)
    
    # Halaman 4: Juga tanpa resi
    page4 = doc.new_page()
    page4.insert_text((50, 100), "Halaman 4 - Kosong (tanpa resi)", fontsize=10)
    
    doc.save("test_multipage.pdf")
    doc.close()
    print("✓ Test PDF dibuat: test_multipage.pdf (4 halaman)")


def test_resi_boundary():
    """Test boundary check untuk resi list"""
    print("\n" + "="*60)
    print("TEST: Extract Resi with Boundary Check")
    print("="*60 + "\n")
    
    # Extract resi
    resi = extract_resi_number("test_multipage.pdf")
    print(f"Total resi found: {len(resi)}")
    for r in resi:
        print(f"  - Page {r['page']}: {r['number']}")
    
    # Simulate page iteration dengan boundary check
    src = fitz.open("test_multipage.pdf")
    total_pages = len(src)
    print(f"\nTotal pages in PDF: {total_pages}")
    print(f"Total resi entries: {len(resi)}")
    
    print("\n--- ITERASI DENGAN BOUNDARY CHECK ---")
    for page_num in range(total_pages):
        page_number = page_num + 1
        resi_number = None
        
        # ✅ BOUNDARY CHECK - ini yang memperbaiki error
        if page_number - 1 < len(resi) and resi[page_number - 1]['page'] == page_number:
            resi_number = resi[page_number - 1]['number']
            print(f"Halaman {page_number}: Resi ditemukan = '{resi_number}'")
        else:
            print(f"Halaman {page_number}: Resi TIDAK ditemukan (fallback)")
    
    src.close()
    print("\n✅ Test selesai tanpa error (boundary check berhasil)")


def test_without_boundary_check():
    """Test TANPA boundary check (untuk menunjukkan error)"""
    print("\n" + "="*60)
    print("TEST: Extract Resi WITHOUT Boundary Check (untuk demo error)")
    print("="*60 + "\n")
    
    resi = extract_resi_number("test_multipage.pdf")
    print(f"Total resi found: {len(resi)}")
    print(f"Trying to access pages without boundary check:\n")
    
    src = fitz.open("test_multipage.pdf")
    total_pages = len(src)
    
    try:
        for page_num in range(total_pages):
            page_number = page_num + 1
            # ❌ TANPA BOUNDARY CHECK - ini yang error
            if resi[page_number - 1]['page'] == page_number:
                print(f"Halaman {page_number}: Resi = {resi[page_number - 1]['number']}")
    except IndexError as e:
        print(f"❌ ERROR pada halaman {page_number}: {type(e).__name__}: {e}")
        print(f"   (Trying to access resi[{page_number - 1}] tapi list hanya punya {len(resi)} items)")
    
    src.close()


if __name__ == "__main__":
    print("DEBUGGING: List Index Out of Range Error\n")
    create_multipage_test_pdf()
    
    # Demonstrasi error tanpa boundary check
    test_without_boundary_check()
    
    # Test dengan boundary check
    test_resi_boundary()
    
    print("\n" + "="*60)
    print("KESIMPULAN:")
    print("="*60)
    print("""
✅ Boundary check (page_number - 1 < len(resi)) mencegah IndexError
✅ Ketika resi tidak ditemukan, fallback position digunakan
✅ Semua halaman diproses tanpa error
""")
