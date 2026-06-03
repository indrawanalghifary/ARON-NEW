#!/usr/bin/env python3
"""Test empty SKU handling di split.py dan bagus.py"""

from split import combine_items
from bagus import process_sku_qty

print("=" * 60)
print("TEST: Empty SKU Handling (Shopee & TikTok)")
print("=" * 60)

# ========== SPLIT.PY (SHOPEE) ==========
print("\n" + "=" * 60)
print("SPLIT.PY (SHOPEE) - combine_items()")
print("=" * 60)

print("\nTEST 1: Ada SKU kosong dengan qty")
print("-" * 60)

items_1 = ['SQU', '', 'WNT', '  ', 'BONUS']
values_1 = [2, 5, 3, 1, 2]
split_map_1 = {"SQUWNT": ["SQU", "WNT"]}

result_1 = combine_items(items_1, values_1, split_map_1)
print(f"\nItems: {items_1}")
print(f"Values: {values_1}")
print(f"Result: {result_1}")
print(f"Expected: {{'SQU': 2, 'WNT': 3}} (kosong & whitespace diabaikan)")
status_1 = result_1 == {'SQU': 2, 'WNT': 3}
print(f"Status: {'✓ PASS' if status_1 else '✗ FAIL'}")

print("\nTEST 2: Semua kosong/whitespace")
print("-" * 60)

items_2 = ['', '  ', '\t', 'BONUS']
values_2 = [1, 2, 3, 4]
split_map_2 = {}

result_2 = combine_items(items_2, values_2, split_map_2)
print(f"\nItems: {items_2}")
print(f"Values: {values_2}")
print(f"Result: {result_2}")
print(f"Expected: {{}} (semua diabaikan)")
status_2 = result_2 == {}
print(f"Status: {'✓ PASS' if status_2 else '✗ FAIL'}")

print("\nTEST 3: Mix valid dan kosong")
print("-" * 60)

items_3 = ['', 'SQUWNT', '', 'IFI', '']
values_3 = [2, 1, 3, 2, 5]
split_map_3 = {"SQUWNT": ["SQU", "WNT"]}

result_3 = combine_items(items_3, values_3, split_map_3)
print(f"\nItems: {items_3}")
print(f"Values: {values_3}")
print(f"Result: {result_3}")
print(f"Expected: {{'SQU': 1, 'WNT': 1, 'IFI': 2}} (hanya valid diproses)")
status_3 = result_3 == {'SQU': 1, 'WNT': 1, 'IFI': 2}
print(f"Status: {'✓ PASS' if status_3 else '✗ FAIL'}")

# ========== BAGUS.PY (TIKTOK) ==========
print("\n" + "=" * 60)
print("BAGUS.PY (TIKTOK) - process_sku_qty()")
print("=" * 60)

print("\nTEST 4: Ada SKU kosong dengan qty")
print("-" * 60)

sku_list_4 = ['SQU', '', 'WNT', '  ', 'BONUS']
qty_list_4 = [2, 5, 3, 1, 2]
split_map_4 = {"SQUWNT": ["SQU", "WNT"]}

result_4 = process_sku_qty(sku_list_4, qty_list_4, split_map_4)
print(f"\nSKU List: {sku_list_4}")
print(f"Qty List: {qty_list_4}")
print(f"Result: {result_4}")
print(f"Expected: {{'SQU': 2, 'WNT': 3}} (kosong & whitespace diabaikan)")
status_4 = result_4 == {'SQU': 2, 'WNT': 3}
print(f"Status: {'✓ PASS' if status_4 else '✗ FAIL'}")

print("\nTEST 5: Semua kosong/whitespace")
print("-" * 60)

sku_list_5 = ['', '  ', '\t', 'BONUS']
qty_list_5 = [1, 2, 3, 4]
split_map_5 = {}

result_5 = process_sku_qty(sku_list_5, qty_list_5, split_map_5)
print(f"\nSKU List: {sku_list_5}")
print(f"Qty List: {qty_list_5}")
print(f"Result: {result_5}")
print(f"Expected: {{}} (semua diabaikan)")
status_5 = result_5 == {}
print(f"Status: {'✓ PASS' if status_5 else '✗ FAIL'}")

print("\nTEST 6: Mix valid dan kosong")
print("-" * 60)

sku_list_6 = ['', 'SQUWNT', '', 'IFI', '']
qty_list_6 = [2, 1, 3, 2, 5]
split_map_6 = {"SQUWNT": ["SQU", "WNT"]}

result_6 = process_sku_qty(sku_list_6, qty_list_6, split_map_6)
print(f"\nSKU List: {sku_list_6}")
print(f"Qty List: {qty_list_6}")
print(f"Result: {result_6}")
print(f"Expected: {{'SQU': 1, 'WNT': 1, 'IFI': 2}} (hanya valid diproses)")
status_6 = result_6 == {'SQU': 1, 'WNT': 1, 'IFI': 2}
print(f"Status: {'✓ PASS' if status_6 else '✗ FAIL'}")

# ========== SUMMARY ==========
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

all_pass = all([status_1, status_2, status_3, status_4, status_5, status_6])
passed = sum([status_1, status_2, status_3, status_4, status_5, status_6])
total = 6

print(f"\nPassed: {passed}/{total}")

if all_pass:
    print("\n✅ ALL TESTS PASSED!")
    print("✓ Empty SKU handling diterapkan di kedua platform")
    print("✓ BONUS handling tetap berfungsi")
    print("✓ Whitespace dibersihkan sebelum check")
else:
    print("\n❌ SOME TESTS FAILED!")
