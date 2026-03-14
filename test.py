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
    


def input_email(prompt: str) -> str:
    """Prompt until the user enters a valid email string."""
    import re
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    while True:
        value = input(prompt).strip()
        if not value:
            print("Email cannot be blank. Please enter your email.")
            continue
        if pattern.match(value):
            return value
        print("Invalid email format. Example: user@example.com")



email = input_email("Enter your email: ")
print("You entered:", email)
