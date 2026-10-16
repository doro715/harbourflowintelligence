"""HarborFlow Assignment 2 starter entry point."""
<<<<<<< HEAD
import data_access  
=======
import datetime

import data_access
>>>>>>> bd25c79f9777eccce05295b1299317a40a77ee1a
import operations
import text_tools
import json

def main():
    """Run the HarborFlow Port Intelligence Console."""
    # TODO: implement the persistent menu and orchestrate the services.
    menuchoice = "0"
    print("HARBORFLOW PORT INTELLIGENCE")
    print("1. List registered vessels")
    print("2. Inspect a vessel manifest")
    print("3. Identify priority cargo")
    print("4. Export a customer operations profile")
    print("5. Find port calls by month")
    print("6. Sanitize an incident report")
    print("7. Analyze the longest stable event sequence")
    print("8. Assess weather risk for upcoming calls")
    print("9. Search incident reports")
    print("10. Close console")
<<<<<<< HEAD

    while menuchoice != "10":

=======

    

    while menuchoice != "10":
>>>>>>> bd25c79f9777eccce05295b1299317a40a77ee1a
        menuchoice = input("Select service: ")

        if menuchoice == "1":
            listed_registered_vessels()

        elif menuchoice == "2":
            "Task 2: Inspect a vessel manifest"

        elif menuchoice == "3":
            "Task 3: Identify priority cargo"
            operations.priority_cargo()
        elif menuchoice == "4":
            "Task 4: Export a customer operations profile"
            operations.export_customer_profile()
        elif menuchoice == "5":
            month = 0
            while month < 1 or month > 12:
                try:
                    month = int(input("Month (1-12): "))
                    if 1 <= month <= 12:
                        port_calls_by_month(month)
                    else:
                        print("Invalid input. Please enter a number between 1 and 12.")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 12.")

        elif menuchoice == "6":
            "Task 6: Sanitize an incident report"

        elif menuchoice == "7":
            "Task 7: Analyze the longest stable event sequence"

        elif menuchoice == "8":
            "Task 8: Assess weather risk for upcoming calls"
            operations.weather_risk()
        elif menuchoice == "9":
            "Task 9: Search incident reports"

        elif menuchoice == "10":
            print("Closing console. Goodbye!")

        else:
            print("Invalid menu choice. Please try again.")
<<<<<<< HEAD
            pass
        
=======


    pass

#task 1
def listed_registered_vessels():
    vessels = data_access.load_all_in_folder("dataset/vessels")
    for vessel in vessels:
        print(f"- {vessel["name"]} | IMO {vessel["imo"]} | {vessel["capacity_teu"]} TEU")
    print(f"Skipped vessel files: {data_access.damaged_files("dataset/vessels")}")

#task 3
def classified_cargo():
    """Identify priority cargo."""

#task 5
def port_calls_by_month(month):
    port_calls = data_access.load_csv_file("dataset/port_calls.csv")
    vessels = data_access.load_all_in_folder("dataset/vessels")
    resolved_list = []
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for port_call in port_calls:
        unknown_vessels = True
        for vessel in vessels:
            if port_call["vessel_id"] == vessel["vessel_id"]:
                unknown_vessels = False
                if valid_date(port_call["arrival_date"]):
                    resolved_list.append((port_call["arrival_date"], vessel["name"], port_call["port_code"], port_call["call_id"]))                    
                else:
                    print(f"Invalid date format for port call {port_call['call_id']}: {port_call['arrival_date']}")
        if unknown_vessels:
            print(f"{port_call["vessel_id"]} is an unknown vessel.")

    #for date, name, port, call_id in resolved_list:
    #    print(f"- {date} | {name} | {port} | {call_id}")
    #print(int(resolved_list[3][0].split('-')[1]))
    print(f"Port calls in {months[month-1]}:")      
    has_printed_month = False
    sorted_resolved_list = sorted(resolved_list, key=lambda x: (x[0], x[1]))  # Sort by date and vessel name
    for date in sorted_resolved_list:        
        if int(date[0].split('-')[1]) == month:
            print(f"- {date[0]} | {date[1]} | {date[2]} | {date[3]}")
            has_printed_month = True
    if not has_printed_month:
        print(f"No port calls found.")


                  
    #print(f"{int(resolved_list[0][0].split('-')[1])}")
    
def valid_date(date_string):
    try:
        datetime.date.fromisoformat(date_string) #yyyy-mm-dd
        return True
    except ValueError:
        return False


>>>>>>> bd25c79f9777eccce05295b1299317a40a77ee1a
if __name__ == "__main__":
    main()
