"""HarborFlow operational business rules.

Keep calculations and record-processing logic separate from user interaction
where practical.
"""
import data_access
from datetime import datetime

#task 3 identify priority cargo
def classify_cargo(shipment):
    if shipment.get("hazardous", True) == True:
        return "CONTROLLED", "hazardous cargo"
    if shipment.get("temperature_controlled", False) == True:
        return "COLD CHAIN", "temperature controlled"
    if shipment.get("priority") == "EXPRESS":
        return "EXPEDITE", "express service"
    if shipment.get("weight_kg", 0) >= 5000:
        return "EXPEDITE", "heavy cargo"
    return "STANDARD", "standard service"

def priority_cargo():
    call_id = input("Call ID: ").strip().upper()

    port_calls = data_access.load_port_calls()
    call_exists = False
    for row in port_calls:
        if str(row.get("call_id", "")).strip().upper() == call_id:
            call_exists = True
            break

    if not call_exists:
        print("Port call not found.")
        return                    

    
    manifest = data_access.find_manifest_by_call_id(call_id)
    if manifest is None:
        print("Manifest unavailable.")
        return                   

    
    shipments = data_access.load_all_shipments()
    counts = {
        "CONTROLLED": 0,
        "COLD CHAIN": 0,
        "EXPEDITE": 0,
        "STANDARD": 0
    }
    for sid in manifest.get("shipment_ids", []):
        shipment = data_access.find_shipment_by_id(sid, shipments)
        if shipment is None:
            continue
        category, reason = classify_cargo(shipment)
        counts[category] += 1
        print(f"{sid} {category} {reason}")

    print(f"Category totals: "
          f"CONTROLLED={counts['CONTROLLED']}, "
          f"COLD CHAIN={counts['COLD CHAIN']}, "
          f"EXPEDITE={counts['EXPEDITE']}, "
          f"STANDARD={counts['STANDARD']}")


def export_customer_profile():
    customer_name = input("Customer name: ").strip()
    target = customer_name.lower()

    # 1. Scan all shipments
    shipments = data_access.load_all_shipments()
    matches = [s for s in shipments
               if str(s.get("customer", "")).strip().lower() == target]

    if not matches:
        print("Customer not found.")
        return

    # 2. Sum up all 
    count = len(matches)
    total_weight = sum(float(s.get("weight_kg", 0)) for s in matches)
    express_count = sum(1 for s in matches if s.get("priority") == "EXPRESS")
    destinations = sorted({str(s.get("destination", "")).strip()
                           for s in matches
                           if str(s.get("destination", "")).strip()})
    dest_str = "|".join(destinations)

    # 3. read new csv now 
    rows = data_access.read_customer_profiles()

    new_row = {
        "customer": customer_name,
        "shipment_count": count,
        "total_weight_kg": f"{total_weight:.2f}",
        "express_count": express_count,
        "destinations": dest_str,
    }

    replaced = False
    for i, row in enumerate(rows):
        if str(row.get("customer", "")).strip().lower() == target:
            rows[i] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)

    # 4. rewrite csv
    data_access.write_customer_profiles(rows)
    print("Customer profile updated: exports/customer-profiles.csv")


# ========== Task 8 ==========
def weather_risk():
    # display vessels
    vessels, _ = data_access.load_vessels()
    vessels.sort(key=lambda v: v["name"].lower())
    for v in vessels:
        print(f"- {v['name']}")

    vessel_name = input("Vessel name: ").strip()
    vessel = data_access.find_vessel_by_name(vessel_name, vessels)
    if vessel is None:
        print("Vessel not found.")
        return

    ref_date = None
    while ref_date is None:
        date_str = input("Reference date (YYYY-MM-DD): ").strip()
        try:
            ref_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Error - Date must use YYYY-MM-DD.")

    # collect calls 
    port_calls = data_access.load_port_calls()
    weather_rows = data_access.load_weather()

    # weather lookup：{(port_code, date_str): row}
    weather_lookup = {}
    for row in weather_rows:
        key = (str(row.get("port_code", "")).strip(),
               str(row.get("date", "")).strip())
        weather_lookup[key] = row

    candidates = []
    for row in port_calls:
        if row.get("vessel_id") != vessel["vessel_id"]:
            continue
        date_str = str(row.get("arrival_date", "")).strip()
        try:
            arrival = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Skipping invalid call date: {date_str}")
            continue
        if arrival >= ref_date:
            candidates.append({
                "call_id": str(row["call_id"]).strip().upper(),
                "arrival": arrival,
                "port_code": str(row.get("port_code", "")).strip(),
                "date_str": date_str,
            })

    if not candidates:
        print("No upcoming port calls found.")
        return

    candidates.sort(key=lambda c: (c["arrival"], c["call_id"]))

    for c in candidates:
        pretty = c["arrival"].strftime("%d %B %Y")
        print(f"{vessel['name']} | {c['port_code']} | {pretty}")

        key = (c["port_code"], c["date_str"])
        forecast = weather_lookup.get(key)
        if forecast is None:
            print("Forecast unavailable")
            continue

        try:
            wind = float(forecast["wind_kmh"])
            precip = float(forecast["precipitation_mm"])
            wave = float(forecast["wave_height_m"])
        except (ValueError, KeyError):
            print("Forecast unavailable")
            continue

        print(f"Wind: {wind:.1f} km/h | Rain: {precip:.1f} mm | Waves: {wave:.1f} m")

        recs = []
        if wind >= 45:
            recs.append("Suspend crane operations.")
        if wave >= 2.5:
            recs.append("Arrange tug assistance.")
        if precip >= 8 and wind < 45:
            recs.append("Prepare covered handling.")
        if not recs:
            recs.append("Normal operating plan.")

