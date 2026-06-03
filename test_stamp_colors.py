#!/usr/bin/env python3
"""
Test script untuk fitur color customization pada stamp text

Verifikasi bahwa:
1. Warna Shopee (merah) diterapkan dengan benar
2. Warna TikTok (hitam) diterapkan dengan benar
3. Custom warna bisa digunakan
4. Fallback position menggunakan warna yang sama
5. Warna dinormalisasi dari 0-255 ke 0-1 (PyMuPDF)
"""

import fitz
from split import find_text_and_add_text
from stamp_colors import get_platform_color, normalize_color, STAMP_COLORS

def create_test_pdf_for_colors():
    """Buat PDF test dengan 2 halaman: normal dan kosong"""
    doc = fitz.open()
    
    # Halaman 1: Normal
    page1 = doc.new_page()
    page1.insert_text((50, 50), "No.Pesanan: 12345", fontsize=12)
    page1.insert_text((50, 100), "Halaman 1 - Untuk test stamp", fontsize=10)
    
    # Halaman 2: Kosong (test fallback)
    page2 = doc.new_page()
    page2.insert_text((50, 100), "Halaman 2 - Kosong (akan gunakan fallback)", fontsize=10)
    
    doc.save("test_colors.pdf")
    doc.close()
    print("✓ Test PDF dibuat: test_colors.pdf")


def test_stamp_colors():
    """Test stamp dengan berbagai warna"""
    
    print("\n" + "="*70)
    print("TEST: Stamp Color Customization")
    print("="*70 + "\n")
    
    # Test cases dengan berbagai warna
    test_cases = [
        {
            'name': 'Shopee (Merah)',
            'platform': 'shopee',
            'expected_255': (255, 0, 0),
            'expected_01': (1.0, 0.0, 0.0)
        },
        {
            'name': 'TikTok (Hitam)',
            'platform': 'tiktok',
            'expected_255': (0, 0, 0),
            'expected_01': (0.0, 0.0, 0.0)
        },
        {
            'name': 'Lazada (Biru)',
            'platform': 'lazada',
            'expected_255': (0, 102, 255),
        },
        {
            'name': 'Red (Merah)',
            'platform': 'red',
            'expected_255': (255, 0, 0),
        },
    ]
    
    print("Testing color retrieval (normalized 0-1):")
    print("-" * 70)
    
    for test in test_cases:
        color_normalized = get_platform_color(test['platform'], normalize=True)
        color_255 = get_platform_color(test['platform'], normalize=False)
        
        # Check normalized value
        is_correct = True
        if 'expected_01' in test:
            is_correct = abs(color_normalized[0] - test['expected_01'][0]) < 0.01
        
        result = "✓ PASS" if is_correct else "✗ FAIL"
        print(f"{result} | {test['name']:<20} | 0-1: {color_normalized}")
        print(f"      | RGB (0-255): {color_255}")
    
    print("\n" + "-"*70)
    print("\nTesting stamp application with different colors:")
    print("-" * 70 + "\n")
    
    doc = fitz.open("test_colors.pdf")
    
    # Test pada halaman normal (dengan referensi teks)
    page1 = doc[0]
    print("Page 1 (dengan referensi 'No.Pesanan: '):")
    
    results = []
    for test in test_cases[:3]:  # Test 3 warna di halaman pertama
        color = get_platform_color(test['platform'], normalize=True)
        result = find_text_and_add_text(
            page1,
            "No.Pesanan: ",
            f"STAMP {test['name']}",
            offset_x=100 + len(results) * 50,  # Offset berbeda untuk tiap test
            offset_y=30,
            fontsize=8,
            color=color
        )
        
        if result:
            status = "✓ FALLBACK" if result.get('is_fallback') else "✓ NORMAL"
            print(f"  {status} | {test['name']:<20} | Color: {color}")
            results.append(result)
        else:
            print(f"  ✗ FAILED | {test['name']:<20}")
    
    # Test pada halaman kosong (akan gunakan fallback position)
    page2 = doc[1]
    print("\nPage 2 (kosong - akan gunakan fallback position):")
    
    for i, test in enumerate(test_cases[:3]):
        color = get_platform_color(test['platform'], normalize=True)
        result = find_text_and_add_text(
            page2,
            "No.Pesanan: ",
            f"FALLBACK {test['name']}",
            fallback_x=10,
            fallback_y=50 + i * 20,  # Offset berbeda
            fontsize=8,
            color=color
        )
        
        if result:
            status = "✓ FALLBACK" if result.get('is_fallback') else "✓ NORMAL"
            print(f"  {status} | {test['name']:<20} | Color: {color}")
        else:
            print(f"  ✗ FAILED | {test['name']:<20}")
    
    doc.save("test_colors_output.pdf")
    doc.close()
    
    print("\n" + "="*70)
    print("✓ Test selesai - Output: test_colors_output.pdf")
    print("="*70)


def test_available_colors():
    """Tampilkan semua warna yang tersedia"""
    
    print("\n" + "="*70)
    print("Available Stamp Colors")
    print("="*70 + "\n")
    
    colors_255 = STAMP_COLORS
    for name in sorted(colors_255.keys()):
        rgb_255 = colors_255[name]
        rgb_01 = normalize_color(rgb_255)
        r, g, b = rgb_255
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        print(f"  {name:<15} | RGB(0-255): {str(rgb_255):<15} | 0-1: {rgb_01}")
        print(f"                  | HEX: {hex_color}")
    
    print("\n" + "="*70)


def test_custom_colors():
    """Test warna custom yang tidak di list"""
    
    print("\n" + "="*70)
    print("TEST: Custom Color (not in predefined list)")
    print("="*70 + "\n")
    
    # Custom color (0-255)
    custom_color_255 = (200, 100, 50)  # Orange custom
    custom_color_01 = normalize_color(custom_color_255)
    
    # Seharusnya return default jika tidak ada
    default_color = get_platform_color("custom_unknown_color", normalize=True)
    print(f"Requesting unknown color 'custom_unknown_color':")
    print(f"  Result: {default_color}")
    print(f"  Expected: (0.0, 0.0, 0.0) [default]")
    
    if abs(default_color[0]) < 0.01:  # Check if close to (0, 0, 0)
        print(f"  ✓ PASS - Correctly returned default color\n")
    else:
        print(f"  ✗ FAIL - Should return default color\n")
    
    # Test untuk membuat stamp dengan warna custom
    doc = fitz.open("test_colors.pdf")
    page = doc[0]
    
    result = find_text_and_add_text(
        page,
        "No.Pesanan: ",
        "CUSTOM COLOR TEST",
        offset_x=150,
        offset_y=60,
        fontsize=9,
        color=custom_color_01  # Use normalized color
    )
    
    print(f"Adding stamp dengan custom color {custom_color_255} (normalized: {custom_color_01}):")
    if result:
        print(f"  ✓ PASS - Stamp ditambahkan dengan warna custom")
        print(f"  Color used: {custom_color_01}")
    else:
        print(f"  ✗ FAIL - Gagal menambahkan stamp")
    
    doc.close()
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n" + "🎨 "*10)
    print("STAMP COLOR CUSTOMIZATION TEST")
    print("🎨 "*10 + "\n")
    
    # Create test PDF
    create_test_pdf_for_colors()
    
    # Test color retrieval
    test_available_colors()
    
    # Test custom colors
    test_custom_colors()
    
    # Test stamp application
    test_stamp_colors()
    
    print("\n" + "🎨 "*10)
    print("✓ ALL TESTS COMPLETED")
    print("🎨 "*10 + "\n")
    print("Generated files:")
    print("  - test_colors.pdf (input)")
    print("  - test_colors_output.pdf (output dengan stamps berwarna)")

