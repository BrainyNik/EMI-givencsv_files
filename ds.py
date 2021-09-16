"""--------To Compute EMI's  From the given file of data-----

    Step 1:
    Write a function to  Download the Csv files from respective urls

   Step 2 :
   Write a function to PARSE(Convert String datatype of file into Float(to perform operations)

   step 3:
      Write a function Which converts data from file into an Dictionary and Store /returns it in an array

   Step 4:
      Write a function That read data from array Compute EMI's and then write it back in the form of dictionary


   step 5:
   Write a function that will create a New .txt file and store the given output of __Step 3__  In Given format


"""

import urllib.request
import math


# Sub-functions

def parse_headers(header_line):
    """to split headers from the file"""
    return header_line.strip().split(',')


def parse_values(data_line):
    """to convert txt into float"""

    values = []
    for item in data_line.strip().split(','):
        if item == "":
            values.append(0.0)

        else:
            values.append(float(item))

    return values


def create_item_dict(values, headers):
    """to store the file into a dictionary """
    result = {}
    for value, header in zip(values, headers):
        result[header] = value
    return result


# Main functions

# Step 1
def download():
    """Step 1"""

    url1 = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw' \
           '/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans1.txt '
    url2 = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw' \
           '/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans2.txt '
    url3 = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw' \
           '/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans3.txt '

    urllib.request.urlretrieve(url1, 'loan1.txt')
    urllib.request.urlretrieve(url2, 'loan2.txt')
    urllib.request.urlretrieve(url3, 'loan3.txt')
    print("File has been downloaded successfully...\n")


# Step 2
def read_csv(path):
    """Step 2"""
    result = []
    # open the file in read mode
    with open(path, 'r') as f:
        # get a list of lines
        lines = f.readlines()

        # Parse the header
        headers = parse_headers(lines[0])

        # loop aver the remaining lines

        for data_line in lines[1:]:
            # Parse values
            values = parse_values(data_line)
            # Create a Dictionary using values and headers
            item_dict = create_item_dict(values, headers)

            # Add dictionary to the result

            result.append(item_dict)
    return result


# Step 3
def loan_emi(amount, duration, rate, down_payment=0):
    """Step 3"""

    """Calculates equal monthly installment for a loan
    
    Arguments :
        amount : Total amount to be append (loan+down payment)
        duration : Duration of the loan
        rate : Rate of interest (monthly)
        down_payment (optional) : Initial payment(deducted from amount)
    """

    loan_amount = amount - down_payment
    try:
        emi = loan_amount * rate * ((1 + rate) ** duration) / (((1 + rate) ** duration) - 1)
    except ZeroDivisionError:
        emi = loan_amount / duration
    emi = math.ceil(emi)
    return emi


# Step 4
def compute_emis(loan):
    for loan in loan:
        loan['emi'] = loan_emi(loan['amount'],
                               loan['duration'],
                               loan['rate'] / 12,
                               loan['down_payment'])


# Step 5
def write_csv(items, path):
    # open a file in write mode
    with open(path, 'w') as fl:
        # Return  if there is nothing to write
        if len(items) == 0:
            return
        # Write headers in first line
        headers = list(items[0].keys())
        fl.write(','.join(headers) + '\n')

        # write one item per  line
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            fl.write((','.join(values) + '\n'))


download()
for i in range(1, 4):
    loans = read_csv('loan{}.txt'.format(i))
    compute_emis(loans)
    write_csv(loans, 'emis{}.txt'.format(i))
