import os
import sys

def ask_question(question):
    while True:
        response = input(question)
        if response == "y":
            return
        elif response == "n":
            exit()

input_str = ""
output = ""
# No argument provided: print help
if len(sys.argv) == 1:
    print("First argument is the path to the input file. The optional second argument is the path to the output directory/file")
    exit()
# One argument provided
elif len(sys.argv) == 2:
    # Is it a valid file?
    if not os.path.isfile(sys.argv[1]):
        print("Input is not a file or does not exist")
        exit()
    input_str = sys.argv[1]
    # Generate output path based on input
    output = os.path.splitext(input_str)[0] + ".xlsx"
    # Does the output file already exist?
    if os.path.isfile(output):
        ask_question(f"Output file '{output}' already exists. It will be overwritten. Do you want to continue? (y/n) ")
# Two arguments provided
elif len(sys.argv) == 3:
    # Is the input valid?
    if not os.path.isfile(sys.argv[1]):
        print("Input is not a file or does not exist")
        exit()
    input_str = sys.argv[1]
    # Does the output already exist?
    if os.path.isfile(sys.argv[2]):
        output = sys.argv[2]
        ask_question(f"Output file '{output}' already exists. It will be overwritten. Do you want to continue? (y/n) ")
    # Is the output path a directory?
    elif os.path.isdir(sys.argv[2]):
        filename = os.path.basename(os.path.splitext(input_str)[0]) + ".xlsx"
        output = os.path.join(sys.argv[2], filename)
        # Does the output file already exist?
        if os.path.isfile(output):
            ask_question(f"Output file '{output}' already exists. It will be overwritten. Do you want to continue? (y/n) ")
    # Is the output path a valid path to a non-existent file?
    elif os.path.isdir(os.path.dirname(sys.argv[2])):
        output = sys.argv[2]
    # Crappy output path
    else:
        print("Output path is invalid")
        exit()
# We don't do more than 2 arguments here
else:
    print("More than two arguments provided")
    exit()

print(f"Output to '{output}'")

import tabula
import pandas
import re

def numeric_part_of_string(s):
    return int(re.compile(r"\d+").findall(s)[0])

mapping = {
    "001": ["Aerospace Engineering", "AE"],
    "002": ["Chemical Engineering", "CL"],
    "004": ["Civil Engineering", "CE"],
    "005": ["Computer Science and Engineering", "CS"],
    "007": ["Electrical Engineering", "EE"],
    "010": ["Mechanical Engineering", "ME"],
    "011": ["Metallurgical Engineering and Materials Science", "MM"],
    "026": ["Engineering Physics", "EP"],
    "D07": ["Electrical Engineering Dual", "EED"],
    "D10": ["Mechanical Engineering Dual", "MED"],
    "D11": ["Metallurgical Engineering and Materials Science Dual", "MMD"],
    "D17": ["Energy Science and Engineering", "EN"],
    "D18": ["Environmental Science & Engineering Dual", "ES"],
    "B03": ["Chemistry", "CH"],
    "B08": ["Humanities and Social Sciences", "EO"],
    "B09": ["Mathematics", "MA"]
}

# Get a list of dataframes; one dataframe for each table in each page
dfs = tabula.read_pdf(input_str, pages = "all")

for df in dfs:
    # Drop the first column in each dataframe
    df.drop(df.columns[0], axis = 1, inplace = True)

    # Set the correct column lables
    df.set_axis(["Roll Number", "Name", "Division", "Tutorial", "Lab"], axis = 1, inplace = True)

# Because of some long names, the tails of those names get split into two tables
# This function is to remove the first row of the dataframe at index and append its name to the dataframe at index - 1
def join_split_name(dfs, index):
    current_df = dfs[index]
    ending = current_df["Name"][0]
    current_df.drop(0, inplace = True)
    current_df.reset_index(inplace = True)
    current_df.drop(current_df.columns[0], axis = 1, inplace = True)
    column = dfs[index - 1]["Name"]
    partial_name = column[len(column) - 1]
    dfs[index - 1]["Name"][len(column) - 1] = partial_name + " " + ending

# # These are the places of anomaly
# for i in [12, 13, 29, 37, 38]:
#     join_split_name(dfs, i)

for df in dfs:
    # Get rid of the Ds, Ts, and the Ps
    for column in ["Division", "Tutorial", "Lab"]:
        df[column] = df[column].apply(numeric_part_of_string)
    
    # Convert all the roll numbers to strings if at all some of them are numbers
    df["Roll Number"] = df["Roll Number"].apply(lambda x: str(x))

    # Remove '\r' in the names
    # df["Name"] = df["Name"].apply(lambda s: s.replace("\r", " "))

    # Add the course and course code
    branch_number = df["Roll Number"][0][2:5]
    try:
        branch_info = mapping[branch_number]
    except KeyError:
        print(f"What does course number '{branch_number}' at index {i} mean?")
        raise
    else:
        df["Branch"] = branch_info[0]
        df["Branch Code"] = branch_info[1]

result = pandas.concat(dfs).reset_index()
result.drop(result.columns[0], axis = 1, inplace = True)
result.to_excel(output, index = False)