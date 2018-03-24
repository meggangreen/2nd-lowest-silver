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

    with open(file_path) as text:
        lines = text.readlines()

    for line in lines:
        zip_code, state, _, _, rate_area = line.strip().split(',')
        zip_codes[zip_code] = zip_codes.get(zip_code, [])
        zip_codes[zip_code].append((state, rate_area))

    return zip_codes


def get_silver_rates(file_path):
    """ Returns dictionary of state, rate areas and their sorted list of silver
        plan rates.

    """

    plan_rates = {}

    with open(file_path) as text:
        lines = text.readlines()

    for line in lines:
        _, state, metal, rate, rate_area = line.strip().split(',')
        # Only grab Silver plan plan_rates
        if metal.lower() != 'silver':
            continue
        plan_rates[(state, rate_area)] = plan_rates.get((state, rate_area), [])
        plan_rates[(state, rate_area)].append(int(rate))

    plan_rates = {area: sorted(rates) for area, rates in plans.items()}

    return plan_rates


def get_slcsp(plan_rates):
    """ Returns dictionary of state, rate areas and the second-lowest rate. """

    slcsp_rates = {}

    for rate_area, rates in plan_rates.items():
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


def fill_slcsp_for_zip(file_path, zip_codes, slcsp_rates):
    """ Replaces ZIP codes-only CSV file with a CSV file containing ZIP codes
        and their corresponding SLCSP values.

        Example code for making a temporary file and replacing another file with
        it from StackOverflow: https://stackoverflow.com/a/39110

    """

    # Make a list of the ZIP codes to look up
    with open(file_path) as text:
        lookup_zips = [line.strip() for line in text.readlines()]
    if len(lookup_zips) < 1:
        return None

    # Assuming each ZIP code in lookup_zips is now '00000,',
    # look up each one and get its rate
    for i in range(len(lookup_zips)):
        # Skip if ZIP not found OR if ZIP has more than one rate area
        zip_code = lookup_zips[i][:-1]
        if len(zip_codes.get(zip_code, [])) != 1:
            continue
        rate_area = zip_codes[zip_code][0]

        lookup_zips[i] += slcsp_rates.get(str(rate_area), "")


    # Make temporary file and write to it
    temp, abs_path = mkstemp()
    with fdopen(temp, 'w') as new_file:
            new_file.write(zip_code + ',' + slcsp)

    # Remove original file
    remove(file_path)

    # Move temp file to orignal file location
    move(abs_path, file_path)
