import json

# From the 61GB JSONL file, retrieves the ones that matches the country/ies

def extract_data_per_country(file_path: str, country: str):
    output_path = f"data-openfoodfacts_{country}.jsonl"

    with open(file_path, 'r', encoding='utf-8') as bulkfile, \
        open(output_path, 'w', encoding='utf-8') as output_file:
        
        for line in bulkfile:
            if not line.strip():
                continue
            try:
                product = json.loads(line)
            except json.JSONDecodeError:
                continue

            countries = product.get('countries', '')

            if isinstance(countries, str):
                countries_list = [c.strip().casefold() for c in countries.split(",")]
            elif isinstance(countries, list):
                countries_list = [c.strip().casefold() for c in countries]
            else:
                countries_list = []

            if country.casefold() in countries_list:
                output_file.write(json.dumps(product) + '\n')


if __name__ == "__main__":
    file_path = "openfoodfacts_bulk.jsonl"

    extract_data_per_country(file_path=file_path, country="argentina")
