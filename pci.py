import requests
import json
import csv

def get_content(unique_name):
    url = f'https://backendapi.pcionline.co.in/api/Common/get_editDoc/Prts%20Profile/{unique_name}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch data for {unique_name}. Status code: {response.status_code}"

def extract_data(response_text):
    try:
        json_data = json.loads(response_text)
        data = json_data.get("message", [])

        # If the data is a string, try converting it to a dictionary
        if isinstance(data, str):
            data = json.loads(data)

        return data
    except json.JSONDecodeError:
        return []

def write_to_csv(csv_output_path, data):
    if not data:
        print("No data to write to CSV.")
        return

    # Dynamically determine fieldnames based on the actual fields present in the data
    fieldnames = list(data[0].keys())

    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in data:
            writer.writerow(entry)

def main():
    file_path = 'text.txt'  # Change this to the path of your text file
    csv_output_path = 'pcid.csv'

    try:
        with open(file_path, 'r') as file:
            unique_names = file.read().splitlines()

        all_data = []

        for name in unique_names:
            result = get_content(name)
            data = extract_data(result)
            print(f"Data for {name}:")
            print(data)
            print("\n" + "="*40 + "\n")  # Separating each result

            all_data.extend(data)

        write_to_csv(csv_output_path, all_data)
        print(f"Data written to {csv_output_path}")

    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")

if __name__ == "__main__":
    main()
