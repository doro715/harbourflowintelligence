"""File loading and path-handling functions for HarborFlow.

Create reusable JSON and CSV loaders here. Do not hard-code sample records.
"""
import json
import csv
from pathlib import Path

def load_json_file(file_path):
    #reading json file and return 
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def load_csv_file(file_path):
    #reading csv file and return 
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

