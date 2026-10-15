"""File loading and path-handling functions for HarborFlow.

Create reusable JSON and CSV loaders here. Do not hard-code sample records.
"""
import json
import csv
from pathlib import Path

def load_json_file(file_path):
    #reading json file and return 
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        #print(f"File not found: {file_path}")
        return 1
        
    except json.JSONDecodeError:
        #print(f"Invalid JSON in file: {file_path}")
        return 1
    except ValueError:
        #3print(f"Error reading file {file_path}")
        return 1

def load_csv_file(file_path):
    #reading csv file and return 
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def load_all_in_folder(folderpath):
    """Load all JSON and CSV files in a folder."""
    templist = []
    folder = Path(folderpath)
    for file_path in folder.glob('*'):
        if file_path.suffix == '.json':
            if load_json_file(file_path) != 1:
                templist.append(load_json_file(file_path))

                
        elif file_path.suffix == '.csv':
            if load_csv_file(file_path) != 1:
                print(load_csv_file(file_path))

    return templist
    return print(f"Skipped vessel files: {failed_reads}")

def damaged_files(folderpath):
    """Load all JSON and CSV files in a folder."""
    failed_reads = int()
    folder = Path(folderpath)
    for file_path in folder.glob('*'):
        if file_path.suffix == '.json':
            if load_json_file(file_path) == 1:
                failed_reads += 1
               
        elif file_path.suffix == '.csv':
            if load_csv_file(file_path) == 1:
                failed_reads += 1
    return failed_reads
    