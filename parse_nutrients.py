import csv

# From the scrapped information (csv files) retrieve nutrients

foodnutrients_fields = [
    'food_id ',
    'calories',
    'protein',
    'fat',
    'saturated_fat',
    'monounsaturated_fat',
    'polyunsaturated_fat',
    'trans_fat',
    'carbohydrates',
    'total_sugars',
    'added_sugars',
    'fiber',
    'sodium',
    'potassium',
    'cholesterol',
]

def parse_usda_foodnutrients(file_name):
    with open(f'{file_name}.csv', 'r', encoding='utf-8') as data_csvfile, \
        open('tables/nutrients-usda_foundation.csv', 'w', encoding='utf-8', newline='') as nutrients_csvfile:

        reader = csv.reader(data_csvfile)
        next(reader, None)
        writer = csv.DictWriter(nutrients_csvfile, fieldnames=foodnutrients_fields)
        writer.writeheader()
        
        id = 1
        for product in reader:
            writer.writerow({
                'food_id ': id,
                'calories': product[4],
                'protein': product[5],
                'fat': product[6],
                'saturated_fat': product[7],
                'monounsaturated_fat': product[8],
                'polyunsaturated_fat': product[9],
                'trans_fat': product[10],
                'carbohydrates': product[11],
                'total_sugars': product[12],
                'added_sugars': product[13],
                'fiber': product[14],
                'sodium': product[15],
                'potassium': product[16],
                'cholesterol': product[17]
            })

            id += 1

def parse_off_foodnutrients(file_name):
    with open(f'{file_name}.csv', 'r', encoding='utf-8') as data_csvfile, \
        open('tables/nutrients-openfoodfacts.csv', 'w', encoding='utf-8', newline='') as nutrients_csvfile:

        reader = csv.reader(data_csvfile)
        next(reader, None)
        writer = csv.DictWriter(nutrients_csvfile, fieldnames=foodnutrients_fields)
        writer.writeheader()
        
        id = 344
        for product in reader:
            writer.writerow({
                'food_id ': id,
                'calories': product[7],
                'protein': product[8],
                'fat': product[9],
                'saturated_fat': product[10],
                'monounsaturated_fat': product[11],
                'polyunsaturated_fat': product[12],
                'trans_fat': product[13],
                'carbohydrates': product[14],
                'total_sugars': product[15],
                'added_sugars': product[16],
                'fiber': product[17],
                'sodium': product[18],
                'potassium': product[19],
                'cholesterol': product[20]
            })

            id += 1

if __name__ == '__main__':
    usda_data_filename = 'scrapped-usda_foundation'
    off_data_filename = 'scrapped-openfoodfacts'

    parse_usda_foodnutrients(usda_data_filename)
    parse_off_foodnutrients(off_data_filename)