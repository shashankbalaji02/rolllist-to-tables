import argparse
import os
from functools import reduce

supported_years = [2018, 2019, 2020, 2021]
year_string = reduce(lambda s, i: str(s) + ", " + str(i), supported_years)

def year(y):
    y = int(y)
    if y not in supported_years:
        raise argparse.ArgumentTypeError(f"only {year_string} are supported")
    return y

def infile(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError("invalid path")

def outfile(path):
    if os.path.isdir(path) or os.path.isdir(os.path.dirname(os.path.abspath(path))):
        return path
    else:
        raise argparse.ArgumentTypeError("invalid path")

parser = argparse.ArgumentParser(description = "Convert IITB roll-list PDFs into XLSX")
parser.add_argument("year", help = f"year of the roll-list to convert. {year_string} supported", type = year)
parser.add_argument("infile", help = "path to roll-list", type = infile)
parser.add_argument("-o", "--output", help = "path to output directory or file. If the input is path/to/file.pdf, then the default output is path/to/file.xlsx", type = outfile)