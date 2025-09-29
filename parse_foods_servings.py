import csv
import re

# From the scrapped information (csv files),
# retrieve what is not a nutrient and separate foods and servings
# for usda 340 foods + 3 added so last id = 343

foods_fields = [
    'id',
    'barcode',
    'name',
]

servings_fields = [
    'food_id',
    'serving_text',
    'serving_weight',
    'is_grams'
]

def parse_brands(brand: str) -> str:
    return re.sub(r',(?=\S)', ', ', brand) 

def is_field_valid(text):
    if text is None:
        return False
    if isinstance(text, (int, float)):
        return text > 0
    text = text.strip()
    return text != '' and text.upper() != 'N/A' and text != "0"


def parse_usda_csv(file_name):
    with open(f'{file_name}.csv', 'r', encoding='utf-8') as data_csvfile, \
        open(f'{file_name}_foodnames_friendly.csv', 'r', encoding='utf-8') as foodnames_csvfile, \
        open('tables/foods-usda_foundation.csv', 'w', encoding='utf-8', newline='') as foods_csvfile, \
        open('tables/servings-usda_foundation.csv', 'w', encoding='utf-8', newline='') as servings_csvfile:

        data_reader = csv.reader(data_csvfile)
        next(data_reader, None)
        foodnames_reader = csv.reader(foodnames_csvfile)
        foods_writer = csv.DictWriter(foods_csvfile, fieldnames=foods_fields)
        foods_writer.writeheader()
        servings_writer = csv.DictWriter(servings_csvfile, fieldnames=servings_fields)
        servings_writer.writeheader()

        id = 1

        for product in data_reader:
            foodname_row = next(foodnames_reader, None)
            if foodname_row is None:
                break

            serving_size = int(float(product[1].strip()))
            serving_unit = product[2]

            foods_writer.writerow({
                'id': id,
                'barcode': None,
                'name': foodname_row[0],
            })

            servings_writer.writerow({
                'food_id': id,
                'serving_text': f'{serving_size} {serving_unit.strip()}',
                'serving_weight': product[3],
                'is_grams': True,
            })

            id += 1

def parse_off_csv(file_name):
    with open(f'{file_name}.csv', 'r', encoding='utf-8') as data_csvfile, \
        open('tables/foods-openfoodfacts.csv', 'w', encoding='utf-8-sig', newline='') as foods_csvfile, \
        open('tables/servings-openfoodfacts.csv', 'w', encoding='utf-8-sig', newline='') as servings_csvfile:
        
        reader = csv.reader(data_csvfile)
        next(reader, None)
        foods_writer = csv.DictWriter(foods_csvfile, fieldnames=foods_fields)    
        foods_writer.writeheader()
        servings_writer = csv.DictWriter(servings_csvfile, fieldnames=servings_fields)    
        servings_writer.writeheader()

        id = 344

        for product in reader:
            brand = product[1]
            product_name = product[2]
            generic_name = product[3]

            if is_field_valid(product_name):
                name = f'{product_name}, {parse_brands(brand)}' if is_field_valid(brand) else product_name
            elif is_field_valid(generic_name): 
                name = f'{parse_brands(brand)}, {generic_name}' if is_field_valid(brand) else generic_name
            elif is_field_valid(brand):
                name = parse_brands(brand)
            else:
                continue

            foods_writer.writerow({
                'id': id,
                'barcode': str(product[0]),
                'name': name,
            })

            serving_unit = product[5]
            serving_quantity = product[4]
            serving_quantity = serving_quantity if is_field_valid(serving_quantity) else None
            serving_size = product[6]

            if (is_field_valid(serving_size) and not is_field_valid(serving_quantity)):
                serving_size = '100 g'

            servings_writer.writerow({
                'food_id': id,
                'serving_text': serving_size.strip() if is_field_valid(serving_size) else '100 g',
                'serving_weight': serving_quantity if is_field_valid(serving_quantity) else 100,
                'is_grams': serving_unit == 'g' or not is_field_valid(serving_unit),
            })

            id += 1

            
if __name__ == "__main__":
    usda_file_name = "scrapped-usda_foundation"
    off_file_name = "scrapped-openfoodfacts"

    parse_usda_csv(usda_file_name)
    parse_off_csv(off_file_name)