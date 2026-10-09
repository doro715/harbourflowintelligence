"""HarborFlow Assignment 2 starter entry point."""


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
    print("Select service:")

    while menuchoice != "10":
        if menuchoice == "1":
            "Task 1: List registered vessels"

        elif menuchoice == "2":
            "Task 2: Inspect a vessel manifest"

        elif menuchoice == "3":
            "Task 3: Identify priority cargo"

        elif menuchoice == "4":
            "Task 4: Export a customer operations profile"

        elif menuchoice == "5":
            "Task 5: Find port calls by month"

        elif menuchoice == "6":
            "Task 6: Sanitize an incident report"

        elif menuchoice == "7":
            "Task 7: Analyze the longest stable event sequence"

        elif menuchoice == "8":
            "Task 8: Assess weather risk for upcoming calls"

        elif menuchoice == "9":
            "Task 9: Search incident reports"

        else:
            print("Invalid menu choice. Please try again.")


    pass


if __name__ == "__main__":
    main()
