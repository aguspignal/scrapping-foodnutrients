import json
import csv
import re

# From the JSONL file with foods of a given country, retrieve all desired information

arabic_regex = re.compile(r'[\u0600-\u06FF]')

def is_arabic(text):
    if text is None:
        return False
    return bool(arabic_regex.search(text))

def is_str_valid(text: str):
    if text is None:
        return False
    
    if isinstance(text, (int, float)):
        return True
    
    text = text.strip()
    return text != '' and text.upper() != 'N/A'

def get_nutrients(nutriments, nutrient_key: str, default=None):
    nutrient_100g = nutriments.get(f'{nutrient_key}_100g', None)
    nutrient = nutrient_100g if nutrient_100g is not None else nutriments.get(f'{nutrient_key}_serving', default)
    return nutrient

def get_string(product, property_key: str):
    prop = product.get(f'{property_key}', None)
    prop = prop if is_str_valid(prop) else 'N/A'
    return prop

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

    with open(f'{data_filename}.jsonl', 'r', encoding='utf-8') as datafile, \
        open(f'{output_filename}.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()

        for line in datafile:
            product = json.loads(line)

            barcode = get_string(product, 'code')
            brands = get_string(product, 'brands')
            generic_name = get_string(product, 'generic_name')
            product_name = get_string(product, 'product_name')
            if not is_str_valid(brands) and not is_str_valid(product_name) and not is_str_valid(generic_name):
                continue
            if is_arabic(brands) or is_arabic(product_name) or is_arabic(generic_name):
                continue

            nutriments = product.get('nutriments', {})
            if nutriments == {}:
                continue
           
            protein = get_nutrients(nutriments=nutriments, nutrient_key="protein", default=0)
            sat_fat = get_nutrients(nutriments=nutriments, nutrient_key="saturated-fat", default=0)
            mono_fat = get_nutrients(nutriments=nutriments, nutrient_key="monounsaturated-fat", default=0)
            poly_fat = get_nutrients(nutriments=nutriments, nutrient_key="polyunsaturated-fat", default=0)
            trans_fat = get_nutrients(nutriments=nutriments, nutrient_key="trans-fat", default=0)
            fat = get_nutrients(nutriments=nutriments, nutrient_key="fat", default=None)
            fat = fat if fat is not None else sat_fat + mono_fat + poly_fat + trans_fat
            carbs = get_nutrients(nutriments=nutriments, nutrient_key="carbohydrates", default=0)
            tot_sug = get_nutrients(nutriments=nutriments, nutrient_key="sugars", default=0)
            add_sug = get_nutrients(nutriments=nutriments, nutrient_key="added-sugars", default=0)
            fiber = get_nutrients(nutriments=nutriments, nutrient_key="fiber", default=0)
            sodium = get_nutrients(nutriments=nutriments, nutrient_key="sodium", default=0)
            potassium = get_nutrients(nutriments=nutriments, nutrient_key="potassium", default=0)
            cholesterol = get_nutrients(nutriments=nutriments, nutrient_key="cholesterol", default=0)
            calories = get_nutrients(nutriments=nutriments, nutrient_key='energy-kcal', default=None)
            calories = calories if calories is not None else protein*4 + fat*9 + carbs*4

            serving_quantity = get_string(product, 'serving_quantity')
            serving_qty_unit = get_string(product, 'serving_quantity_unit')
            serving_size = get_string(product, 'serving_size')

            if (serving_size == 'N/A' and serving_quantity == "N/A"):
                if (calories == 0 and fiber == 0 and sodium == 0 and potassium == 0 and cholesterol == 0):
                    continue

            writer.writerow({
                'Barcode': barcode,
                'Brands': brands,
                'Product name': product_name, 
                'Generic name': generic_name, 
                'Serving quantity': serving_quantity, 
                'Serving qty unit': serving_qty_unit, 
                'Serving size': serving_size,

                'Calories': calories,
                'Protein': protein,
                'Fats': fat,
                'Saturated fats': sat_fat,
                'Monounsaturated fats': mono_fat,
                'Polyunsaturated fats': poly_fat,
                'Trans fats': trans_fat,
                'Carbs': carbs,
                'Total sugars': tot_sug,
                'Added sugars': add_sug,
                'Fiber': fiber,
                'Sodium': sodium,
                'Potassium': potassium,
                'Cholesterol': cholesterol
            })

if __name__ == "__main__":
    data_filename = "data-openfoodfacts_argentina"
    output_filename = "scrapped-openfoodfacts"

    extract_data(data_filename, output_filename)
