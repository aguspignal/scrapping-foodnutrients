import json
import csv

# From the USDA Foundation JSON file, retrieve the desired information
# also generates another file with just the names

def extract_food_data(file_filename, output_filename):
    field_names = [
        'Name', 
        'Serving size', 
        'Serving unit', 
        'Serving weight (g)',
        'Calories',
        'Protein',
        'Fats',
        'Saturated fats',
        'Monounsaturated fats',
        'Polyunsaturated fats',
        'Trans fats',
        'Carbs',
        'Total sugars',
        'Added sugars',
        'Fiber',
        'Sodium',
        'Potassium',
        'Cholesterol'
    ]

    with open(f'{output_filename}.csv', 'w', newline='', encoding='utf-8') as csvfile, \
        open(f'{file_filename}.json', 'r', encoding='utf-8') as jsonfile:

        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
    
        data = json.load(jsonfile)

        if 'FoundationFoods' in data:
            foods = data['FoundationFoods']
        elif 'BrandedFoods' in data:
            foods = data['BrandedFoods']
        elif 'foods' in data:
            foods = data['foods']
        else:
            print('Unexpected JSON structure')
            return

        for food in foods:
            name = food.get("description")
            
            serving_size = 100
            serving_unit = 'g'
            serving_gram_weight = 100
            serving_household_unit = 'N/A'

            if 'foodPortions' in food and food['foodPortions']:
                portion = food['foodPortions'][0]
                serving_size = portion.get('value', 'N/A')
                serving_unit = portion.get('measureUnit', 'N/A').get('name', 'N/A')
                serving_gram_weight = portion.get('gramWeight', "N/A")
            elif 'servingSize' in food:
                serving_size = food.get('servingSize')
                serving_unit = food.get('servingUnit')
                serving_household_unit = food.get('householdServingFullText')

            kcals = None
            proteins = 0
            fats = 0
            saturated_fats = 0
            monounsaturated_fats = 0
            polyunsaturated_fats = 0
            trans_fats = 0
            carbs = 0
            total_sugars = 0
            added_sugars = 0
            fibers = 0
            sodium = 0
            potassium = 0
            cholesterol = 0
            
            if 'foodNutrients' in food:
                for nutrient in food['foodNutrients']:
                    nutrient_id = str(nutrient.get('nutrient', {}).get('id', ''))
                    amount = nutrient.get('amount', 0) or 0
                    amount = float(amount)

                    if nutrient_id == '1008':
                        kcals = amount
                    elif nutrient_id == '1003':
                        proteins = amount
                    elif nutrient_id == '1004':
                        fats = amount
                    elif nutrient_id == '1258':
                        saturated_fats = amount
                    elif nutrient_id == '1292':
                        monounsaturated_fats = amount
                    elif nutrient_id == '1293':
                        polyunsaturated_fats = amount
                    elif nutrient_id == '1257':
                        trans_fats = amount
                    elif nutrient_id == '1005':
                        carbs = amount if amount >= 0 else 0
                    elif nutrient_id == '2000':
                        total_sugars = amount
                    elif nutrient_id == '1235':
                        added_sugars = amount
                    elif nutrient_id == '1079':
                        fibers = amount
                    elif nutrient_id == '1093':
                        sodium = amount
                    elif nutrient_id == '1092':
                        potassium = amount
                    elif nutrient_id == '1253':
                        cholesterol = amount

            if kcals is None or kcals == 0:
                kcals = proteins*4 + (fats + saturated_fats + monounsaturated_fats + polyunsaturated_fats + trans_fats)*9 + carbs*4

            writer.writerow({
                'Name': name, 
                'Serving size': serving_size,  
                'Serving unit': serving_unit, 
                'Serving weight (g)': serving_gram_weight,
                'Calories': kcals,
                'Protein': proteins,
                'Fats': fats,
                'Saturated fats': saturated_fats,
                'Monounsaturated fats': monounsaturated_fats,
                'Polyunsaturated fats': polyunsaturated_fats,
                'Trans fats': trans_fats,
                'Carbs': carbs,
                'Total sugars': total_sugars,
                'Added sugars': added_sugars,
                'Fiber': fibers,
                'Sodium': sodium,
                'Potassium': potassium,
                'Cholesterol': cholesterol
            })

    with open(f'{output_filename}.csv', 'r', encoding='utf-8') as csvfile, \
         open(f'{output_filename}_foodnames.csv', 'w', encoding='utf-8', newline='') as names_csvfile:
        
        reader = csv.reader(csvfile)
        names_writer = csv.DictWriter(names_csvfile, fieldnames=['Name'])
        next(reader, None)
        for row in reader:
            if row:
                names_writer.writerow({'Name': row[0]})

if __name__ == "__main__":
    foundation_filename = "data-usda_foundation"
    foundation_output_filename = "scrapped-usda_foundation"
    branded_filename = "data-usda_branded"
    branded_output_filename = "scrapped-usda_branded"

    extract_food_data(foundation_filename, foundation_output_filename)
    # extract_food_data(branded_filename, branded_output_filename)