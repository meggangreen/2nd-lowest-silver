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

    zip_codes = {}

    with open(file_path) as file:
        lines = file.readlines()

    for line in lines:
        zip_code, state, _, _, rate_area = line.strip().split(',')
        zip_codes[zip_code] = zip_codes.get(zip_code, [])
        zip_codes[zip_code].append((state, rate_area))

    return zip_codes


def get_silver_rates(file_path):
    """ Returns dictionary of state, rate areas and their silver plan rates. """

    rates = {}

    with open(file_path) as file:
        lines = file.readlines()

    for line in lines:
        _, state, metal, rate, rate_area = line.strip().split(',')
        # Only grab Silver plan rates
        if metal.lower() != 'silver':
            continue
        rates[(state, rate_area)] = rates.get((state, rate_area), [])
        rates[(state, rate_area)].append(int(rate))

    return rates


def fill_slcsp_for_zip(file_path, zip_codes, rates):
    """ Replaces ZIP codes-only CSV file with a CSV file containing ZIP codes
        and their corresponding SLCSP values.

        Example code for making a temporary file and replacing another file with
        it from StackOverflow: https://stackoverflow.com/a/39110

    """

    with open(file_path) as file:
        lines



    temp, abs_path = mkstemp()
    with fdopen(temp, 'w') as new_file:
