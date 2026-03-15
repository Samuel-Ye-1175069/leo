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
    """Prompt the user to enter a valid name and return it as a string."""
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


def input_email(input_prompt: str) -> str:
    """Prompt until the user enters a valid email string."""
    # Use a regular expression to validate email format. 
    import re
    # The regex pattern checks for a typical email structure: local part, @ symbol, domain part, and top-level domain.
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    while True:
        # Prompt user and strip whitespace from input.
        value = input(input_prompt).strip()
        if not value:
            # If we reach here, it means the user entered an empty string. Notify user and loop again.
            print("Email cannot be blank. Please enter your email.")
            continue
        # If we reach here, it means the user entered a non-empty string. Now validate it against the email regex pattern.
        if pattern.match(value):
            return value
        # If we reach here, it means the email format is invalid. Notify user and loop again.
        print("Invalid email format. Example: user@example.com")
        

def list_all_members():
    """
    Lists member details.
    This is an example of how to produce basic output."""
    format_str = "{: <5} {: <15} {: <15} {: <14} {: <20}"            # Use the same format_str for column headers and rows to ensure consistent spacing. 
    display_formatted_row(["ID","First Name","Family Name","Birth Date","e-Mail"],format_str)     # Use the display_formatted_row() function to display the column headers with consistent spacing
    for member in members:
        id = member[0]
        fname = member[1]
        famname = member[2]
        birthdate = member[3].strftime("%d %b %Y")
        email = member[4]

        display_formatted_row([id,fname,famname,birthdate, email],format_str)     # Use the display_formatted_row() function to display each row with consistent spacing
    input("\nPress Enter to continue.")


def add_new_member():
    """Prompt for member details and add a new member, with validation.
     This function validates that the first name and family name are not empty and only contain allowed characters (letters, space, dash, single quote).
     It also validates that the email is in a valid format and is not a duplicate of an existing member's email (case-insensitive).
     The birth date is validated using the input_date() function, with a reasonable range (not in the future and not too far in the past).
     """
    fname = input_name("Enter First Name: ")
    famname = input_name("Enter Family Name: ")
    email = input_email("Enter e-Mail Address: ")
    # Duplication check: ensure no existing member has same email (case-insensitive)
    email_lower = email.lower()
    for member in members:
        if member[4].lower() == email_lower:
            print(f"Email {email} is already registered for {member[1]} {member[2]}. Member not added.")
            return

    birthdate = input_date("Enter Birth Date", date(1900, 1, 1), date.today() + timedelta(days=1))
    new_id = unique_id()
    # Add new member to the members list as a list [id, first name, family name, birth date, email]
    members.append([new_id, fname, famname, birthdate, email])
    print(f"Member {fname} {famname} added with ID {new_id}.")
    input("\nPress Enter to continue.")
    

def add_new_location():
    """Prompt for a location name and add it, with validation.
     This function validates that 
        - the location name is not empty 
        - is at least 3 characters long 
        - only contains allowed characters (letters, numbers, spaces, dash, single quote, slash)
        - is not a duplicate of an existing location (case-insensitive)
        If the location is valid and added successfully, it also initializes an empty list of observations for that location in the observations dictionary."""
    while True:
        location_name = input("Enter Location Name: ").strip()
        # Validate that the location name is not empty.
        if not location_name:
            print("Location name cannot be blank. Please enter a location.")
            continue
        # Validate that the location name is at least 3 characters long.
        if len(location_name) < 3:
            print("Location name must be at least 3 characters.")
            continue
        # Validate that the location name only contains allowed characters (letters, numbers, spaces, dash, single quote, slash).
        if not all(char.isalnum() or char in " -'/" for char in location_name):
            print("Location name may only include letters, numbers, spaces, hyphens, and apostrophes.")
            continue
        # Duplicate check (case-insensitive)
        existing_names = [loc_name.lower() for (_, loc_name) in locations]
        if location_name.lower() in existing_names:
            print("This location already exists. Please enter a different location.")
            continue
        break

    new_id = unique_id()
    locations.append((new_id, location_name)) # Add new location to the locations list as a tuple (id, name)
    observations[new_id] = [] # Initialize an empty list of observations for the new location in the observations dictionary
    print(f"Location '{location_name}' added with ID {new_id}.")
    input("\nPress Enter to continue.")


def add_new_observation():
    """Prompt for observation details and add a new observation , with validation.
     This function validates that the member ID, insect ID, and location ID entered by the user exist in the respective lists.
     It also validates that the observation date is within a reasonable range (not in the future and not too far in the past).
     The function displays the list of members, insects, and locations to the user before prompting for the respective IDs, to assist with valid input.
     If the observation is valid, it adds it to the observations dictionary under the correct location ID as a tuple (member_id, insect_id, observation_date).
     """
    member_ids = {m[0] for m in members}
    insect_ids = {i[0] for i in insects}
    location_ids = {l[0] for l in locations}

    # Show only relevant members list before asking member ID
    print("\nMembers:")
    display_formatted_row(["ID", "First Name", "Family Name", "Email"], "{: <5} {: <15} {: <15} {: <25}")
    for m in members:
        display_formatted_row([m[0], m[1], m[2], m[4]], "{: <5} {: <15} {: <15} {: <25}")

    # Validate member ID input: must be an integer and exist in member_ids set. Loop until valid input is received.
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

    # Validate insect ID input: must be an integer and exist in insect_ids set. Loop until valid input is received.
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

    # Validate location ID input: must be an integer and exist in location_ids set. Loop until valid input is received.
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

    # Validate observation date input using the input_date() function, with a reasonable range (not in the future and not too far in the past).
    observation_date = input_date("Enter observation date", date(2020, 1, 1), date.today() + timedelta(days=1))
    # If we reach here, it means all inputs are valid. Add the new observation to the observations dictionary under the correct location ID.
    # setdefault() is used to ensure that there is a list for the location_id key in the observations dictionary.
    observations.setdefault(location_id, []).append((member_id, insect_id, observation_date))
    print(f"Observation added: member {member_id}, insect {insect_id}, location {location_id}, date {observation_date:%d/%m/%Y}.")
    input("\nPress Enter to continue.")


def list_locations_and_observations():
    format_str = "{: <8} {: <27} {: <11} {: <20} {: <12} {: <20}"
    # Display column headers with consistent spacing using display_formatted_row() function.
    display_formatted_row(["Loc ID", "Location", "Member ID", "Member Name", "Date", "Insect"], format_str)
    
    # Create lookup dictionaries for member names, insect names, and location names by their IDs.
    # Using id as the key allows for efficient lookup when displaying observations.
    member_by_id = {m[0]: f"{m[1]} {m[2]}" for m in members}
    insect_by_id = {i[0]: i[1] for i in insects}
    location_by_id = {l[0]: l[1] for l in locations}

    # Iterate through observation groups by location id (from observations dict)
    for loc_id, loc_obs in observations.items():
        # Get location name from lookup, or use "Unknown Location" if ID not found (shouldn't happen if data is consistent).
        loc_name = location_by_id.get(loc_id, "Unknown Location") 
        # If there are no observations for this location, display the location with empty observation fields and continue to next location.
        if not loc_obs:
            display_formatted_row([loc_id, loc_name, "", "", "", ""], format_str)
            continue
        # If there are observations, iterate through each observation for this location and display the details.
        for member_id, insect_id, obs_date in loc_obs:
            member_name = member_by_id.get(member_id, "")
            insect_name = insect_by_id.get(insect_id, "")
            obs_date_text = obs_date.strftime("%d/%m/%Y") if obs_date else ""
            # Display the observation details in a formatted row using display_formatted_row() function for consistent spacing.
            display_formatted_row([loc_id, loc_name, member_id, member_name, obs_date_text, insect_name], format_str)

    input("\nPress Enter to continue.")


def list_members_and_ages():
    """Display each member with their current age in years."""
    today = date.today()
    format_str = "{: <7} {: <12} {: <12} {: <14} {: <5}"           
    display_formatted_row(["ID", "First Name", "Family Name", "Birth Date", "Age"], format_str)     
    for member in members:
        member_id = member[0]
        fname = member[1]
        famname = member[2]
        birthdate = member[3]

        # age calculation: subtract years and adjust for whether birthday has passed this year
        # I've tried to use timedelta.days // 365 to calculate age, but it doesn't work correctly because it doesn't account for leap years and varying month lengths. 
        # So instead, I calculate age by subtracting birth year from current year and then adjusting based on whether the birthday has occurred yet this year.
        age = today.year - birthdate.year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        display_formatted_row([member_id, fname, famname, birthdate.strftime("%d %b %Y"), age], format_str)     
    input("\nPress Enter to continue.")


def disp_menu():
    """
    Displays the menu and current date.  No parameters required.
    """
    print("==== WELCOME TO LINCOLN ENTOMOLOGY OBSERVERS SYSTEM ===")
    print(" 1 - List Members")
    print(" 2 - List Locations and their Observations")
    print(" 3 - List Members and their Ages")
    print(" 4 - Add New Observation")
    print(" 5 - Add New Location")
    print(" 6 - Add New Member")
    print(" X - Exit (stops the program)")


# ------------ This is the main program ------------------------

# Don't change the menu numbering or function names in this menu.
# Although you can add arguments to the function calls, if you wish.
# Repeat this loop until the user enters an "X" or "x"
response = ""
while response.upper() != "X":
    disp_menu()
    # Display menu for the first time, and ask for response
    response = input("Please enter menu choice: ")    
    if response == "1":
        list_all_members()
    elif response == "2":
        list_locations_and_observations()
    elif response == "3":
        list_members_and_ages()
    elif response == "4":
        add_new_observation()
    elif response == "5":
        add_new_location()
    elif response == "6":
        add_new_member()
    elif response.upper() != "X":
        print("\n*** Invalid response, please try again (enter 1-6 or X)")

    print("")

print("\n=== Thank you for using the LINCOLN ENTOMOLOGY OBSERVERS SYSTEM! ===\n")