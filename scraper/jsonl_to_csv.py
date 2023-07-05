import locale
import sys
import json
import csv
import getopt


def transform_jsonl_to_csv(jsonl_file, csv_file):
    # Read the JSONL file and transform it into CSV format
    with open(jsonl_file, 'r', encoding='utf-8') as jsonl_file:
        json_data = []
        for line in jsonl_file:
            data = json.loads(line)
            json_data.append(data)

        field_names = set()
        for data in json_data:
            field_names.update(data.keys())

        with open(csv_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(json_data)


def main(argv):
    # Default values for command line arguments
    jsonl_file = None
    csv_file = None

    try:
        # Parsing command line arguments
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Usage: python jsonl_to_csv.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: python jsonl_to_csv.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            jsonl_file = arg
        elif opt in ("-o", "--ofile"):
            csv_file = arg

    # Check if both input and output files are provided
    if jsonl_file is None or csv_file is None:
        print('Please provide the input and output file names.')
        print('Usage: python jsonl_to_csv.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    # Transform the JSONL file to CSV
    transform_jsonl_to_csv(jsonl_file, csv_file)

    print(f"Transformation complete. The JSONL file '{jsonl_file}' has been transformed to CSV format in '{csv_file}'.")


if __name__ == "__main__":
    main(sys.argv[1:])
