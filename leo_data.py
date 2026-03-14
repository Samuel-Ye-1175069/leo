# [id, first_name, family_name, birthdate ,email address]
from datetime import date
import uuid


members = [ 
	[816, 'Simon', 'Charles', date(1981,7,15), 'simon@charles.nz'],
	[343, 'Charlie', 'Charles', date(1998,1,25), 'charlie@charles.nz'],
	[810, 'Kate', 'McArthur', date(1998,9,30), 'K_McArthur94@gmail.com'],
	[786, 'Jack', 'Hopere', date(1972,2,10), 'Jack643@gmail.com'],
	[801, 'Chloe', 'Mathewson', date(1985,3,15), 'Chloe572@gmail.com'],
	[121, 'Kate', 'McLeod', date(1999,7,15), 'KMcLeod112@gmail.com']
]

insects = [
    (1, "Huhu beetle (Prionoplus reticularis)"),
    (2, "Mānuka beetle (Pyronota festiva)"),
    (3, "New Zealand giraffe weevil (Lasiorhynchus barbicornis)"),
    (4, "Red admiral / Kahukura (Vanessa gonerilla)"),
    (5, "Yellow admiral / Kōwhaiwhai (Vanessa itea)"),
    (6, "Common copper butterfly / Raupō (Lycaena salustius)"),
    (7, "New Zealand praying mantis (Orthodera novaezealandiae)"),
    (8, "New Zealand stick insect (Acanthoxyla geisovii)"),
    (9, "Auckland tree wētā (Hemideina thoracica)"),
    (10, "Cook Strait giant wētā (Deinacrida rugosa)"),
    (11, "Marlborough green geometer moth (Chloroclystis bilineolata)"),
    (12, "Forest ringlet butterfly (Dodonidia helmsii)")
]

locations = [(1, "Ashley Dene Farm"), (34, "Lincoln University Campus"), (67, "Reids Pitt"), (76, "Mahoe Reserve")]

observations = {
    1: [(816, 7, date(2024, 5, 20))], 
    2: [(343, 1, date(2024, 5, 21)), (810, 3, date(2024, 5, 22))], 
    3: [(786, 2, date(2024, 5, 23))], 
    4: [(801, 6, date(2024, 5, 24))], 
    5: [(121, 4, date(2024, 5, 25))],
    34: [], 
    67: [], 
    76: [(121, 1, date(2025, 7, 26))]
}


def unique_id():
    """
    This will return a unique id number"""

    unique_id = uuid.uuid4().time_hi_version
    return unique_id
    

def display_formatted_row(row, format_str):
    """
    row is a list or tuple containing the items in a single row.
    format_str uses the following format, with one set of curly braces {} for each column:
       eg, "{: <10}" determines the width of each column, padded with spaces (10 spaces in this example)
       <, ^ and > determine the alignment of the text: < (left aligned), ^ (centre aligned), > (right aligned)
    The following example is for 3 columns of output: left-aligned 5 characters wide; centred 10 characters; right-aligned 15 characters:
        format_str = "{: <5}  {: ^10}  {: >15}"
    Make sure the column is wider than the heading text and the widest entry in that column,
        otherwise the columns won't align correctly.
    You can also pad with something other than a space and put characters between the columns, 
        eg, this pads with full stops '.' and separates the columns with the pipe character '|' :
           format_str = "{:.<5} | {:.^10} | {:.>15}"
    """
    # Convert a tuple to a list, to allow updating of values
    if type(row) == tuple: 
        row = list(row)
    # Loop through each item in the row, changing to "" (empty string) if value is None and converting all other values to string
    #   (Extra info:  enumerate() places a loop counter value in index to allow updating of the correct item in row)
    for index,item in enumerate(row):
        if item is None:      # Removes any None values from the row_list, which would cause the print(*row_list) to fail
            row[index] = ""       
        else:    
            row[index] = str(item)
    # Apply the formatting in format_str to all items in row
    print(format_str.format(*row))

