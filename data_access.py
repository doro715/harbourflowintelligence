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

# ----------read json and csv files---------
def load_json_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def load_csv_file(path):
    rows = []
    with open(path, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

#-----------load data in different files
def load_all_manifests():
    """read manifests/ all json。retun list[dict]。"""
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


def ensure_sanitized_dir():
    SANITIZED_DIR.mkdir(parents=True, exist_ok=True)


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
