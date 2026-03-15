from leo_data import members, insects, locations, observations
from leo_data import unique_id, display_formatted_row
from datetime import datetime,timedelta,date

def input_date(input_prompt : str, mindate : date = None , maxdate : date = None) -> date:
    """Prompt the user to enter a valid date and return datetime.date.

    The function accepts multiple formats:
    - "31-12-2024" or "31/12/2024" or "31.12.2024"
    - "2024-12-31" or "2024/12/31" or "2024.12.31"
    - "31-12-24" or "31/12/24" or "31.12.24" (2-digit year)
    It validates returned date against optional min/max bounds.

    Args:
      mindate: If provided, user date must be >= this date.
      maxdate: If provided, user date must be <= this date.

    Returns:
      A datetime.date object from valid input.
    """

    # Keep asking until a valid date is entered.
    while True:
        
        # Prompt user with min/max date info if provided.
        # Provide an example for clarity in prompt.
        # Clean up input by stripping whitespace.
        entered_str = input(f"{input_prompt} after {mindate:%d/%m/%Y} and before {maxdate:%d/%m/%Y} (e.g., 31/12/2024): ").strip()       
        entered_date = None # Initialize to None to detect if parsing succeeded.
        
        # Try parsing the entered string with multiple date formats until one succeeds.
        # entered_date will be set to a datetime.date if parsing succeeds, or remain None if all formats fail.
        for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y/%m/%d","%d-%m-%Y", "%d-%m-%y", "%Y-%m-%d", "%d.%m.%Y", "%d.%m.%y", "%Y.%m.%d"):
            try:
                entered_date = datetime.strptime(entered_str, fmt).date()
                break
            except ValueError:
                continue
            
        # Validate the entered date against min/max bounds if parsing succeeded.
        if entered_date != None:
            print(f"You entered: {entered_date:%d/%m/%Y}")
            
            if (mindate != None and entered_date < mindate):
                print(f"Date must be after {mindate:%d/%m/%Y}, Please try again.")
                continue
            
            elif (maxdate != None and entered_date > maxdate):
                print(f"Date must be before {maxdate:%d/%m/%Y}, Please try again.")
                continue
            
            # If we reach here, it means the date is valid. Notify user and return the date.
            else:
                print(f"Valid date entered: {entered_date:%d/%m/%Y}")
                return entered_date
            
        # If we reach here, it means parsing failed. Notify user and loop again.
        else:
            print("Invalid date format. Please try again.")


def input_name(input_prompt: str) -> str:
    """Prompt until the user enters a non-empty validated name."""
    while True:
        # Prompt user and strip whitespace from input.
        entered_str = input(input_prompt).strip()
        
        # Validate that the name is not empty and only contains allowed characters (letters, space, dash, single quote).
        if not entered_str:
            print("Name cannot be blank. Please enter your name.")
            continue
        for char in entered_str:
            if not (char.isalpha() or char in " -'"):
                # If we reach here, it means the name contains invalid characters. Notify user and loop again.
                print("Name can only include letters, space, dash, single quote.")
                break
            
        # If we reach here, it means the name is valid. Notify user and return the name.    
        else:
                print("Valid name entered:", entered_str)
                return entered_str
    


def input_email(prompt: str) -> str:
    """Prompt until the user enters a valid email string."""
    # Use a regular expression to validate email format. 
    import re
    # The regex pattern checks for a typical email structure: local part, @ symbol, domain part, and top-level domain.
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    while True:
        # Prompt user and strip whitespace from input.
        value = input(prompt).strip()
        if not value:
            # If we reach here, it means the user entered an empty string. Notify user and loop again.
            print("Email cannot be blank. Please enter your email.")
            continue
        # If we reach here, it means the user entered a non-empty string. Now validate it against the email regex pattern.
        if pattern.match(value):
            return value
        # If we reach here, it means the email format is invalid. Notify user and loop again.
        print("Invalid email format. Example: user@example.com")


def list_locations_and_observations():
    """Display locations and their observations in a simple table."""
    format_str = "{: <8} {: <20} {: <12} {: <25} {: <20} {: <12}"
    display_formatted_row(["Loc ID", "Location", "Member ID", "Member Name", "Insect", "Date"], format_str)

    member_by_id = {m[0]: f"{m[1]} {m[2]}" for m in members}
    insect_by_id = {i[0]: i[1] for i in insects}
    location_by_id = {l[0]: l[1] for l in locations}

    # Iterate through observation groups by location id (from observations dict)
    for loc_id, loc_obs in observations.items():
        loc_name = location_by_id.get(loc_id, "Unknown Location")
        if not loc_obs:
            display_formatted_row([loc_id, loc_name, "", "", "", ""], format_str)
            continue

        for member_id, insect_id, obs_date in loc_obs:
            member_name = member_by_id.get(member_id, "")
            insect_name = insect_by_id.get(insect_id, "")
            obs_date_text = obs_date.strftime("%d/%m/%Y") if obs_date else ""
            display_formatted_row([loc_id, loc_name, member_id, member_name, insect_name, obs_date_text], format_str)

    input("\nPress Enter to continue.")

def add_new_observation():
    """Add a new observation with validation for member, insect, location and date."""
    member_ids = {m[0] for m in members}
    insect_ids = {i[0] for i in insects}
    location_ids = {l[0] for l in locations}

    # Show only relevant members list before asking member ID
    print("\nMembers:")
    display_formatted_row(["ID", "First Name", "Family Name", "Email"], "{: <5} {: <15} {: <15} {: <25}")
    for m in members:
        display_formatted_row([m[0], m[1], m[2], m[4]], "{: <5} {: <15} {: <15} {: <25}")

    while True:
        try:
            member_id = int(input("Enter member ID: ").strip())
        except ValueError:
            print("Enter a valid number for member ID.")
            continue
        if member_id not in member_ids:
            print("Member ID not found. Please use an existing ID from the member list above or add a new member.")
            continue
        break

    # Show insects before asking insect ID
    print("\nInsects:")
    display_formatted_row(["ID", "Insect Name"], "{: <5} {: <30}")
    for i in insects:
        display_formatted_row([i[0], i[1]], "{: <5} {: <30}")

    while True:
        try:
            insect_id = int(input("Enter insect ID: ").strip())
        except ValueError:
            print("Enter a valid number for insect ID.")
            continue
        if insect_id not in insect_ids:
            print("Insect ID not found. Please use an existing ID from the insect list above.")
            continue
        break

    # Show locations before asking location ID
    print("\nLocations:")
    display_formatted_row(["ID", "Location Name"], "{: <5} {: <30}")
    for l in locations:
        display_formatted_row([l[0], l[1]], "{: <5} {: <30}")

    while True:
        try:
            location_id = int(input("Enter location ID: ").strip())
        except ValueError:
            print("Enter a valid number for location ID.")
            continue
        if location_id not in location_ids:
            print("Location ID not found. Please use an existing ID from the location list above or add a new location.")
            continue
        break

    observation_date = input_date("Enter observation date", date(2020, 1, 1), date.today() + timedelta(days=1))
    observations.setdefault(location_id, []).append((member_id, insect_id, observation_date))
    print(f"Observation added: member {member_id}, insect {insect_id}, location {location_id}, date {observation_date:%d/%m/%Y}.")
    input("\nPress Enter to continue.")
    
    
addition = add_new_observation()

