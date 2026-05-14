from collections import defaultdict

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

    return f"Produk {produk_text} - {suffix}"


def format_j_text(combined_result, prefix="JXXXXXXXX"):
    # Membuat format: 3,SQU,3,WNT
    detail = ",".join(
        f"{qty},{name}"
        for name, qty in combined_result.items()
    )

    return f"{prefix},{detail}"


# Contoh penggunaan
items = ['squ', 'ifispj', 'squ', 'squwnt']
values = [1, 2, 1, 1]

split_map = {
    "SQUWNT": ["SQU", "WNT"],
    "IFISPJ": ["IFI", "SPJ"],
    "KLRNSQU": ["KLRN", "SQU"],
    "CSHWNT": ["CSH", "WNT"]
}

hasil = combine_items(items, values, split_map)

text_produk = format_produk_text(hasil)
text_j = format_j_text(hasil)

print(text_produk)
print(text_j)

