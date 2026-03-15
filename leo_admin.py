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
                print(f"Date must be on or after {mindate:%d/%m/%Y}, Please try again.")
                continue
            
            elif (maxdate != None and entered_date > maxdate):
                print(f"Date must be on or before {maxdate:%d/%m/%Y}, Please try again.")
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
    members.append([new_id, fname, famname, birthdate, email])
    print(f"Member {fname} {famname} added with ID {new_id}.")

def list_locations_and_observations():
    pass

def list_members_and_ages():
      pass

def disp_menu():
    """
    Displays the menu and current date.  No parameters required.
    """
    print("==== WELCOME TO LINCOLN ENTOMOLOGY OBSERVERS SYSTEM ===")
    print(" 1 - List Members")
    print(" 2 - List Members and their Observations")
    print(" 3 - List Members and their Ages")
    print(" 4 - Add New Observation")
    print(" 5 - Add New Location")
    print(" 6 - Add New Member")
    print(" X - eXit (stops the program)")


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
        pass
    elif response == "5":
        pass
    elif response == "6":
        add_new_member()
    elif response.upper() != "X":
        print("\n*** Invalid response, please try again (enter 1-6 or X)")

    print("")

print("\n=== Thank you for using the LINCOLN ENTOMOLOGY OBSERVERS SYSTEM! ===\n")