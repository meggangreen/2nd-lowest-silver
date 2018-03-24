""" You have been given a CSV file, slcsp.csv, which contains the ZIP Codes in
    the first column. Fill in the second column with the rate (see below) of the
    corresponding SLCSP. Your answer is the modified CSV file, plus any source
    code used.

    Write your code in your best programming language.

    The order of the rows in your answer file must stay the same as how they
    appeared in the original slcsp.csv.

    It may not be possible to determine a SLCSP for every ZIP Code given. Check
    for cases where a definitive answer cannot be found and leave those cells
    blank in the output CSV (no quotes or zeroes or other text).

"""

def get_rate_areas(file_path):
    """ Returns dictionary of ZIP codes and their state, rate area tuples. """

    zipcodes = {}

    with open(file_path) as file:
        lines = file.readlines()

    for line in lines:
        zipcode, state, _, _, rate_area = line.strip().split(',')
        zipcodes[zipcode] = zipcodes.get(zipcode, [])
        zipcodes[zipcode].append((state, rate_area))

    return zipcodes

