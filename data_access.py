"""File loading and path-handling functions for HarborFlow.

Create reusable JSON and CSV loaders here. Do not hard-code sample records.
"""
import json
from pathlib import Path
import csv
import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "dataset"
VESSELS_DIR = DATASET_DIR / "vessels"
MANIFESTS_DIR = DATASET_DIR / "manifests"
SHIPMENTS_DIR = DATASET_DIR / "shipments"
INCIDENTS_DIR = DATASET_DIR / "incidents"
PORT_CALLS_FILE = DATASET_DIR / "port_calls.csv"
WEATHER_FILE = DATASET_DIR / "weather.csv"
EXPORTS_DIR = PROJECT_ROOT / "exports"

EXPORTS_DIR = PROJECT_ROOT / "exports"
SANITIZED_DIR = EXPORTS_DIR / "sanitized"
CUSTOMER_PROFILES_FILE = EXPORTS_DIR / "customer-profiles.csv"

#-----------load data in different data files
def load_all_manifests():
    """read manifests/ all json。return list[dict]。"""
    manifests = []
    for path in sorted(MANIFESTS_DIR.glob("*.json")):
        try:
            rec = load_json_file(path)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        if isinstance(rec, dict) and "call_id" in rec:
            manifests.append(rec)
    return manifests
    
def find_manifest_by_call_id(call_id, manifests=None):
    if manifests is None:
        manifests = load_all_manifests()
    target = call_id.strip().upper()
    for m in manifests:
        if str(m.get("call_id", "")).strip().upper() == target:
            return m
    return None

def load_all_shipments():
    shipments = []
    for path in sorted(SHIPMENTS_DIR.glob("*.json")):
        try:
            rec = load_json_file(path)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        if isinstance(rec, dict) and "shipment_id" in rec:
            shipments.append(rec)
    return shipments

def load_vessels():
    vessels_dir = Path("dataset/vessels")
    vessels_list = {}

    for json_file in vessels_dir.glob("*.json"):
        try:
            with open(json_file, "r") as file:
                vessels_list[json_file.stem] = json.load(file)
        except json.JSONDecodeError:
            print("Invalid JSON:", json_file.name)

    return vessels_list

def find_vessel_by_name(name,vessels=None):
    if vessels is None:
        vessels = load_vessels()
    target = name.strip().lower()

    if isinstance(vessels, dict):
        search_space = vessels.values()
    else:
        search_space = vessels

    for v in search_space:
        if v["name"].strip().lower() == target:
            return v
    else:
        return None

def find_shipment_by_id(shipment_id, shipments=None):
    if shipments is None:
        shipments = load_all_shipments()
    target = shipment_id.strip().upper()
    for s in shipments:
        if str(s.get("shipment_id", "")).strip().upper() == target:
            return s
    return None

def load_all_incidents():
    incidents = []
    for path in sorted(INCIDENTS_DIR.glob("*.json")):
        try:
            record = load_json_file(path)
        except(FileNotFoundError,json.JSONDecodeError):
            continue
        if "incident_id" in record:
            incidents.append(record)
        return incidents
    
def load_port_calls():
    return load_csv_file(PORT_CALLS_FILE)

def call_id_exists_in_port_calls(call_id, port_calls=None):
    if port_calls is None:
        port_calls = load_port_calls()
    target = call_id.strip().upper()
    for row in port_calls:
        if str(row.get("call_id", "")).strip().upper() == target:
            return True
    return False

def load_weather():
    return load_csv_file(WEATHER_FILE)

def ensure_exports_dir():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def write_customer_profiles(rows):
    """rows: list[dict]:customer, shipment_count, total_weight_kg, express_count, destinations"""
    ensure_exports_dir()
    header = ["customer", "shipment_count", "total_weight_kg",
              "express_count", "destinations"]
    with open(CUSTOMER_PROFILES_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def read_customer_profiles():
    if not CUSTOMER_PROFILES_FILE.exists():
        return []
    return load_csv_file(CUSTOMER_PROFILES_FILE)

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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        # print(f"File not found: {file_path}")
        return 1
    except csv.Error:
        #print(f"Invalid CSV in file: {file_path}")
        return 1
    except ValueError:
        #print(f"Error reading file {file_path}")
        return 1

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
                templist.append(load_csv_file(file_path))

    return templist

def damaged_files(folderpath):
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
    
