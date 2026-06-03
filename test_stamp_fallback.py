#!/usr/bin/env python3
"""
Test script untuk memverifikasi bahwa stamp tampil pada halaman kosong
dengan menggunakan fallback position.

Masalah: Stamp tidak tampil saat halaman kosong setelah split
Solusi: find_text_and_add_text() sekarang memiliki fallback position
"""

import fitz
from split import find_text_and_add_text

def create_test_pdf():
    """Membuat PDF test dengan 2 halaman: 1 normal, 1 kosong"""
    doc = fitz.open()
    
    # Halaman 1: Normal (dengan teks "No.Pesanan: ")
    page1 = doc.new_page()
    page1.insert_text((50, 50), "No.Pesanan: 12345", fontsize=12)
    page1.insert_text((50, 100), "Halaman pertama - teks ada", fontsize=10)
    
    # Halaman 2: Kosong (tanpa teks "No.Pesanan: ")
    page2 = doc.new_page()
    page2.insert_text((50, 100), "Halaman kedua - kosong dari No.Pesanan", fontsize=10)
    
    doc.save("test_stamp.pdf")
    doc.close()
    print("✓ Test PDF dibuat: test_stamp.pdf")


def test_stamp_on_pages():
    """Test penambahan stamp pada halaman normal dan kosong"""
    doc = fitz.open("test_stamp.pdf")
    
    test_cases = [
        {
            'page_num': 0,
            'name': 'Halaman Normal',
            'expected': 'Teks "No.Pesanan: " ditemukan, stamp di posisi normal'
        },
        {
            'page_num': 1,
            'name': 'Halaman Kosong',
            'expected': 'Teks "No.Pesanan: " TIDAK ditemukan, stamp di fallback position (10, 20)'
        }
    ]
    
    for test_case in test_cases:
        page = doc[test_case['page_num']]
        print(f"\n{'='*60}")
        print(f"TEST: {test_case['name']}")
        print(f"{'='*60}")
        print(f"Expected: {test_case['expected']}\n")
        
        result = find_text_and_add_text(
            page, 
            "No.Pesanan: ",
            "📦 PRODUK STAMP TEST",
            offset_x=100,
            offset_y=-3,
            fontsize=9,
            fallback_x=10,
            fallback_y=20
        )
        
        if result:
            print(f"\nResult:")
            print(f"  - is_fallback: {result.get('is_fallback')}")
            print(f"  - inserted_at: {result.get('inserted_at')}")
            if result.get('found_at'):
                print(f"  - found_at: {result.get('found_at')}")
        else:
            print("Result: None")
    
    # Save ke file baru
    doc.save("test_stamp_output.pdf")
    doc.close()
    print(f"\n{'='*60}")
    print("✓ Test selesai - hasil disimpan: test_stamp_output.pdf")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("DEBUGGING: Stamp pada Halaman Kosong\n")
    create_test_pdf()
    test_stamp_on_pages()
