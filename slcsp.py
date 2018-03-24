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

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import pathlib

def get_file_lines(file_path):
    """ Returns lines of text from file. """

    with open(file_path) as text:
        lines = text.readlines()

    return lines


def get_rate_areas(zips_csv):
    """ Returns dictionary of ZIP codes and their state, rate area tuples. """

    rate_areas = {}

    lines = get_file_lines(zips_csv)

    for line in lines:
        zip_code, state, _, _, rate_area = line.strip().split(',')
        rate_areas[zip_code] = rate_areas.get(zip_code, set([]))
        rate_areas[zip_code].add((state, rate_area))

    return rate_areas


def get_silver_rates(plans_csv):
    """ Returns dictionary of state rate areas and their sorted list of silver
        plan rates.

    """

    silver_rates = {}

    lines = get_file_lines(plans_csv)

    for line in lines:
        _, state, metal, rate, rate_area = line.strip().split(',')
        # Only grab Silver plan silver_rates
        if metal.lower() != 'silver':
            continue
        silver_rates[(state, rate_area)] = silver_rates.get((state, rate_area), [])
        silver_rates[(state, rate_area)].append(float(rate))

    silver_rates = {area: sorted(rates) for area, rates in silver_rates.items()}

    return silver_rates


def get_slcsp_rates(silver_rates):
    """ Returns dictionary of state rate areas and 2nd-lowest silver rate. """

    slcsp_rates = {}

    for rate_area, rates in silver_rates.items():
        # Skip if rate area has no plan rates
        if len(rates) < 1:
            continue
        elif len(rates) == 1:
            slcsp_rates[rate_area] = rates[0]
        else:
            # Get second-lowest rate
            for j in range(len(rates)):
                if rates[j+1] > rates[j]:
                    slcsp_rates[rate_area] = rates[j+1]
                    break

    return slcsp_rates


def get_slcsp_for_zip(slcsp_csv, rate_areas, slcsp_rates):
    """ Returns text list of ZIP codes and their corresponding SLCSP values. """


    # Make a list of the ZIP codes to look up
    zips_slcsp = [line.strip() for line in get_file_lines(slcsp_csv)]
    if len(zips_slcsp) < 1:
        return None

    # Assuming each ZIP code in zips_slcsp is now '00000,',
    # look up each one and get its rate
    for i in range(len(zips_slcsp)):
        # Skip if ZIP not found OR if ZIP has more than one rate area
        zip_code = zips_slcsp[i][:-1]
        if len(rate_areas.get(zip_code, [])) != 1:
            continue
        # Make a list of one without modifying the set
        rate_area = list(rate_areas[zip_code])[0]

        zips_slcsp[i] += str(slcsp_rates.get(rate_area, ""))

    return zips_slcsp


def replace_empty_slcsp_file_with_full(slcsp_csv, zips_csv, plans_csv):
    """ Given a file that contains only ZIP codes (slcsp_csv), overwrites it
        with another file containing the original file's ZIP codes and any found
        corresponding SLCSP rate values.

    """

    if not slcsp_csv or not zips_csv or not plans_csv:
        return None

    # Get rate areas for each ZIP code in zips_csv
    rate_areas = get_rate_areas(zips_csv)
    # Get SLCSP rates for each rate area from plans_csv
    slcsp_rates = get_slcsp_rates(get_silver_rates(plans_csv))
    # Get corresponding SLCSP for each ZIP code in slcsp_csv
    zips_slcsp = get_slcsp_for_zip(slcsp_csv, rate_areas, slcsp_rates)

    # Make temporary file and write to it;
    # example from https://stackoverflow.com/a/39110
    temp, abs_path = mkstemp()
    with fdopen(temp, 'w') as new_file:
        for each_zip_slcsp in zips_slcsp:
            new_file.write(each_zip_slcsp + "\n")
    # Remove original file
    remove(slcsp_csv)
    # Move temp file to orignal file location
    move(abs_path, slcsp_csv)


def has_all_files(file_names):
    """ Returns True/False if all necessary files are in program folder. """

    if not file_names:
        return False

    missing = 0
    dir_files = set([f.name for f in pathlib.Path('.').glob('*.csv')])
    # import pdb; pdb.set_trace()

    for f_name in file_names:
        if f_name not in dir_files:
            missing += 1

    return missing == 0


################################################################################

if __name__ == '__main__':

    file_names = ("slcsp.csv", "zips.csv", "plans.csv")
    if has_all_files(file_names):
        slcsp_csv, zips_csv, plans_csv = file_names
        replace_empty_slcsp_file_with_full(slcsp_csv, zips_csv, plans_csv)
        print("\nProcess complete. Please check '{}'.\n".format(slcsp_csv))
    else:
        print("\nEnsure the necessary files are in the program folder.")
        for f_name in file_names:
            print(f_name)
        print("\n")
