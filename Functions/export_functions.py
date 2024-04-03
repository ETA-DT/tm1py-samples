"""
This python Scripts gathers differents export functions to generate output files
"""

# function to write each element from a list in a row
def write_elem_by_row(file, list, empty_row_start = True, empty_row_end = True):
    if empty_row_start:
        file.writerow([])
    for elem in list:
        file.writerow([elem])
    if empty_row_end:
        file.writerow([])

