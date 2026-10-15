"""File loading and path-handling functions for HarborFlow.

Create reusable JSON and CSV loaders here. Do not hard-code sample records.
"""
import json
from pathlib import Path
import csv

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
def load_vessels(directory=None):
    """返回 (valid_list, skipped_filename_list)"""
    if directory is None:
        directory = VESSELS_DIR
    required = ["vessel_id", "name", "imo", "capacity_teu"]
    valid, skipped = [], []
    for path in sorted(directory.glob("*.json")):
        try:
            rec = load_json_file(path)
        except (FileNotFoundError, json.JSONDecodeError):
            skipped.append(path.name)
            continue
        if not all(f in rec for f in required):
            skipped.append(path.name)
            continue
        valid.append(rec)
    return valid, skipped

def load_all_manifests():
    """读 manifests/ 下所有 json。返回 list[dict]。坏文件跳过。"""
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


def write_sanitized_text(incident_id, text):
    ensure_sanitized_dir()
    path = SANITIZED_DIR / f"{incident_id}-sanitized.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path




