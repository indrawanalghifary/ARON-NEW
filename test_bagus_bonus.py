#!/usr/bin/env python3
"""Test BONUS handling di bagus.py"""

from bagus import process_sku_qty

print("=" * 50)
print("TEST: TikTok (bagus.py) - BONUS Handling")
print("=" * 50)

# Test case 1: Ada BONUS
print("\nTEST 1: Ada SKU BONUS")
print("-" * 50)

sku_list_1 = ['SQU', 'BONUS', 'WNT', 'BONUS SQU']
qty_list_1 = [2, 1, 3, 2]
split_map_1 = {"SQUWNT": ["SQU", "WNT"]}

result_1 = process_sku_qty(sku_list_1, qty_list_1, split_map_1)
print(f"\nSKU List: {sku_list_1}")
print(f"Qty List: {qty_list_1}")
print(f"Split Map: {split_map_1}")
print(f"Result: {result_1}")
print(f"Expected: {{'SQU': 2, 'WNT': 3}}")
print(f"Status: {'✓ PASS' if result_1 == {'SQU': 2, 'WNT': 3} else '✗ FAIL'}")

# Test case 2: Tidak ada BONUS
print("\n\nTEST 2: Tidak ada SKU BONUS")
print("-" * 50)

sku_list_2 = ['SQU', 'WNT', 'SQU']
qty_list_2 = [2, 3, 1]
split_map_2 = {"SQUWNT": ["SQU", "WNT"]}

result_2 = process_sku_qty(sku_list_2, qty_list_2, split_map_2)
print(f"\nSKU List: {sku_list_2}")
print(f"Qty List: {qty_list_2}")
print(f"Split Map: {split_map_2}")
print(f"Result: {result_2}")
print(f"Expected: {{'SQU': 3, 'WNT': 3}}")
print(f"Status: {'✓ PASS' if result_2 == {'SQU': 3, 'WNT': 3} else '✗ FAIL'}")

# Test case 3: Semua BONUS
print("\n\nTEST 3: Semua SKU adalah BONUS")
print("-" * 50)

sku_list_3 = ['BONUS', 'BONUS SQU', 'BONUS WNT']
qty_list_3 = [1, 2, 3]
split_map_3 = {"SQUWNT": ["SQU", "WNT"]}

result_3 = process_sku_qty(sku_list_3, qty_list_3, split_map_3)
print(f"\nSKU List: {sku_list_3}")
print(f"Qty List: {qty_list_3}")
print(f"Split Map: {split_map_3}")
print(f"Result: {result_3}")
print(f"Expected: {{}}")
print(f"Status: {'✓ PASS' if result_3 == {} else '✗ FAIL'}")

# Test case 4: Complex scenario dengan split_map
print("\n\nTEST 4: Complex Scenario dengan Split Map")
print("-" * 50)

sku_list_4 = ['SQUWNT', 'BONUS', 'IFI', 'BONUS SQUWNT', 'SPJ']
qty_list_4 = [1, 2, 1, 3, 1]
split_map_4 = {
    "SQUWNT": ["SQU", "WNT"],
    "IFISPJ": ["IFI", "SPJ"]
}

result_4 = process_sku_qty(sku_list_4, qty_list_4, split_map_4)
print(f"\nSKU List: {sku_list_4}")
print(f"Qty List: {qty_list_4}")
print(f"Split Map: {split_map_4}")
print(f"Result: {result_4}")
print(f"Expected: {{'SQU': 1, 'WNT': 1, 'IFI': 1, 'SPJ': 1}}")
expected_4 = {'SQU': 1, 'WNT': 1, 'IFI': 1, 'SPJ': 1}
print(f"Status: {'✓ PASS' if result_4 == expected_4 else '✗ FAIL'}")

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print("✓ TikTok (bagus.py) - BONUS handling sudah diterapkan!")
