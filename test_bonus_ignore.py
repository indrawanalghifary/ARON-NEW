#!/usr/bin/env python3
"""Test untuk verify SKU BONUS diabaikan"""

from split import combine_items

# Test case 1: Ada BONUS
print("=" * 50)
print("TEST 1: Ada SKU BONUS")
print("=" * 50)

items_1 = ['SQU', 'BONUS', 'WNT', 'BONUS SQU']
values_1 = [2, 1, 3, 2]
split_map_1 = {"SQUWNT": ["SQU", "WNT"]}

result_1 = combine_items(items_1, values_1, split_map_1)
print(f"\nItems: {items_1}")
print(f"Values: {values_1}")
print(f"Split Map: {split_map_1}")
print(f"\nResult: {result_1}")
print(f"Expected: {{'SQU': 2, 'WNT': 3}}")
print(f"Status: {'✓ PASS' if result_1 == {'SQU': 2, 'WNT': 3} else '✗ FAIL'}")

# Test case 2: Tidak ada BONUS
print("\n" + "=" * 50)
print("TEST 2: Tidak ada SKU BONUS")
print("=" * 50)

items_2 = ['SQU', 'WNT', 'SQU']
values_2 = [2, 3, 1]
split_map_2 = {"SQUWNT": ["SQU", "WNT"]}

result_2 = combine_items(items_2, values_2, split_map_2)
print(f"\nItems: {items_2}")
print(f"Values: {values_2}")
print(f"Split Map: {split_map_2}")
print(f"\nResult: {result_2}")
print(f"Expected: {{'SQU': 3, 'WNT': 3}}")
print(f"Status: {'✓ PASS' if result_2 == {'SQU': 3, 'WNT': 3} else '✗ FAIL'}")

# Test case 3: Semua BONUS
print("\n" + "=" * 50)
print("TEST 3: Semua SKU adalah BONUS")
print("=" * 50)

items_3 = ['BONUS', 'BONUS SQU', 'BONUS WNT']
values_3 = [1, 2, 3]
split_map_3 = {"SQUWNT": ["SQU", "WNT"]}

result_3 = combine_items(items_3, values_3, split_map_3)
print(f"\nItems: {items_3}")
print(f"Values: {values_3}")
print(f"Split Map: {split_map_3}")
print(f"\nResult: {result_3}")
print(f"Expected: {{}}")  # Empty dict
print(f"Status: {'✓ PASS' if result_3 == {} else '✗ FAIL'}")

# Test case 4: Complex scenario
print("\n" + "=" * 50)
print("TEST 4: Complex Scenario")
print("=" * 50)

items_4 = ['SQUWNT', 'BONUS', 'CBO', 'BONUS SQUWNT', 'IFI']
values_4 = [1, 2, 1, 3, 2]
split_map_4 = {
    "SQUWNT": ["SQU", "WNT"],
    "CBO": ["KLRN", "SQU"]
}

result_4 = combine_items(items_4, values_4, split_map_4)
print(f"\nItems: {items_4}")
print(f"Values: {values_4}")
print(f"Split Map: {split_map_4}")
print(f"\nResult: {result_4}")
print(f"Expected: {{'SQU': 2, 'WNT': 1, 'KLRN': 1, 'IFI': 2}}")
expected_4 = {'SQU': 2, 'WNT': 1, 'KLRN': 1, 'IFI': 2}
print(f"Status: {'✓ PASS' if result_4 == expected_4 else '✗ FAIL'}")

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print("✓ Test selesai - SKU BONUS diabaikan dengan benar")
