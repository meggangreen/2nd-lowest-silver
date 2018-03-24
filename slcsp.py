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
        rate_areas[zip_code] = rate_areas.get(zip_code, [])
        rate_areas[zip_code].append((state, rate_area))

    return rate_areas


def get_silver_rates(plans_csv):
    """ Returns dictionary of state, rate areas and their sorted list of silver
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
        silver_rates[(state, rate_area)].append(int(rate))

    silver_rates = {area: sorted(rates) for area, rates in plans.items()}

    return silver_rates


def get_slcsp_rates(silver_rates):
    """ Returns dictionary of state, rate areas and the second-lowest rate. """

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
        rate_area = rate_areas[zip_code][0]

        zips_slcsp[i] += slcsp_rates.get(str(rate_area), "")

    return zips_slcsp


def replace_empty_slcsp_file_with_full(slcsp_csv, zips_csv, plans_csv):
    """    Example code for making a temporary file and replacing another file with
        it from StackOverflow: https://stackoverflow.com/a/39110

    """

    if not slcsp_csv or not zips_csv or not plans_csv:
        return None

    # Get rate areas for each ZIP code in zips_csv
    rate_areas = get_rate_areas(zips_csv)
    slcsp_rates = get_slcsp_rates(get_silver_rates(plans_csv))
    zips_slcsp = get_slcsp_for_zip(slcsp_csv, rate_areas, slcsp_rates)

    # Make temporary file and write to it
    temp, abs_path = mkstemp()
    with fdopen(temp, 'w') as new_file:
        for each_zip_slcsp in zips_slcsp:
            new_file.write(each_zip_slcsp)
    # Remove original file
    remove('tester.csv')  # remove(slcsp_csv)
    # Move temp file to orignal file location
    move(abs_path, 'tester.csv')  # move(abs_path, slcsp_csv)


def has_all_files(file_names):
    """ Returns True/False if all necessary files are in program folder. """

    missing = 0

    for f_name in file_names:
        if f_name not in pathlib.Path('.').glob():
            missing += 1

    return missing == 0


################################################################################

if __name__ == '__main__':

    file_names = ("slcsp.csv", "zips.csv", "plans.csv")
    if has_all_files(file_names):
        slcsp_csv, zips_csv, plans_csv = file_names
        replace_empty_slcsp_file_with_full(slcsp_csv, zips_csv, plans_csv)
        print("\n\nProcess complete. Please check 'tester.csv'.".format(slcsp_csv))
    else:
        print("\n\nEnsure the necessary files are in the program folder.")
        for f_name in file_names:
            print(f_name)

