import json
import csv
import unicodedata

# From the JSONL file with foods of a given country, retrieve all desired information

def is_latin(text: str) -> bool:
    if not isinstance(text, str):
        return False
    for ch in text:
        if ch.isalpha():
            name = unicodedata.name(ch, "")
            if "LATIN" not in name:
                return False
    return True

def is_str_valid(text: str):
    if text is None:
        return False
    text = text.strip()
    return text != '' and text.upper() != 'N/A'


def extract_data(data_filename, output_filename):
    csv_fields = [
        'Barcode', 'Brands',
        'Product name', 'Generic name', 
        'Serving quantity', 'Serving qty unit', 'Serving size',
        'Calories', 'Protein',
        'Fats', 'Saturated fats', 'Monounsaturated fats', 'Polyunsaturated fats', 'Trans fats',
        'Carbs', 'Total sugars', 'Added sugars',
        'Fiber', 'Sodium', 'Potassium', 'Cholesterol'
    ]

    with open(f'{output_filename}.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()

        with open(f'{data_filename}.jsonl', 'r', encoding='utf-8') as bulkfile:
            for line in bulkfile:
                product = json.loads(line)

                barcode = product.get('code', 'N/A')
                if not is_str_valid(barcode):
                    continue

                brands = product.get('brands', 'N/A')
                generic_name = product.get('generic_name', 'N/A')
                product_name = product.get('product_name', 'N/A')
                if not is_str_valid(brands) or not is_str_valid(product_name) or not is_str_valid(generic_name):
                    continue
                elif not is_latin(brands) or not is_latin(product_name) or not is_latin(generic_name):
                    continue

                serving_quantity = product.get('serving_quantity', 'N/A')
                serving_quantity_unit = product.get('serving_quantity_unit', 'N/A')
                serving_size = product.get('serving_size', 'N/A')

                nutriments = product.get('nutriments', {})
                if nutriments == {}:
                    continue
                
                writer.writerow({
                    'Barcode': barcode,
                    'Brands': brands,
                    'Product name': product_name, 
                    'Generic name': generic_name, 
                    'Serving quantity': serving_quantity, 
                    'Serving qty unit': serving_quantity_unit, 
                    'Serving size': serving_size,
                    'Calories': nutriments.get('energy-kcal_100g', 0),
                    'Protein': nutriments.get('proteins_100g', 0),
                    'Fats': nutriments.get('fat_100g', 0),
                    'Saturated fats': nutriments.get('saturated-fat_100g', 0),
                    'Monounsaturated fats': nutriments.get('monounsaturated-fat_100g', 0),
                    'Polyunsaturated fats': nutriments.get('polyunsaturated-fat_100g', 0),
                    'Trans fats': nutriments.get('trans-fat_100g', 0),
                    'Carbs': nutriments.get('carbohydrates_100g', 0),
                    'Total sugars': nutriments.get('sugars_100g', 0),
                    'Added sugars': nutriments.get('added-sugars_100g', 0),
                    'Fiber': nutriments.get('fiber_100g', 0),
                    'Sodium': nutriments.get('sodium_100g', 0),
                    'Potassium': nutriments.get('potassium_100g', 0),
                    'Cholesterol': nutriments.get('cholesterol_100g', 0)
                })

if __name__ == "__main__":
    data_filename = "data-openfoodfacts_argentina"
    output_filename = "scrapped-openfoodfacts"

    extract_data(data_filename, output_filename)
