from parse_input import parser
import os

args = parser.parse_args()
year = args.year
infile = args.infile
output = args.output
filename = os.path.basename(os.path.splitext(infile)[0])

if output is None:
    output = os.path.splitext(infile)[0] + ".xlsx"
elif os.path.isdir(output):
    output = os.path.join(output, filename + ".xlsx")

if os.path.isfile(output):
    while True:
        response = input("The output file already exists. It will be overwritten. Do you want to continue? (y/n) ")
        if response == "y":
            break
        elif response == "n":
            exit()

print(f"Output to '{output}'")

import tabula
import pandas
from importlib import import_module
try:
    dfs = tabula.read_pdf(infile, pages = "all")
except BaseException:
    print("Sorry, infile cannot be converted :(")
    exit()
cleanup = import_module(f"cleanup_{year}")
try:
    cleanup.cleanup(dfs)
except BaseException:
    print("Sorry, infile cannot be converted :(")
    exit()
pandas.concat(dfs).to_excel(output, index = False)