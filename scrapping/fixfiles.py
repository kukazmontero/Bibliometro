import os
import json

def read_files(directory):
    data = {}
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            # dejar en minuscula content 
            content = content.lower()
            data[content] = []

    return data

if __name__ == "__main__":
    directory_path = "results"

    result_data = read_files(directory_path)

    json_result = json.dumps(result_data, indent=4, ensure_ascii=False)

    with open("output.json", "w", encoding='utf-8') as output_file:
        output_file.write(json_result)

    print("JSON data written to output.json")
