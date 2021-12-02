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

mapping = {
    "001": ("Aerospace Engineering", "AE"),
    "002": ("Chemical Engineering", "CL"),
    "004": ("Civil Engineering", "CE"),
    "005": ("Computer Science and Engineering", "CS"),
    "007": ("Electrical Engineering", "EE"),
    "010": ("Mechanical Engineering", "ME"),
    "011": ("Metallurgical Engineering and Materials Science", "MM"),
    "026": ("Engineering Physics", "EP"),
    "D07": ("Electrical Engineering Dual", "EED"),
    "D10": ("Mechanical Engineering Dual", "MED"),
    "D11": ("Metallurgical Engineering and Materials Science Dual", "MMD"),
    "D17": ("Energy Science and Engineering", "EN"),
    "D18": ("Environmental Science & Engineering Dual", "ES"),
    "B03": ("Chemistry", "CH"),
    "B08": ("Humanities and Social Sciences", "EO"),
    "B09": ("Mathematics", "MA")
}

def remove_first_column(df):
    df.drop(df.columns[0], axis = 1, inplace = True)

def add_column_labels(df):
    # Duplicate the very first entry in the dataframe
    df.loc[-1] = list(df)
    df.index = df.index + 1
    df.sort_index(inplace = True)
    # Set the correct column lables
    df.set_axis(["Roll Number", "Name", "Division", "Tutorial", "Lab"], axis = 1, inplace = True)

def remove_newline_from_names(df):
    df["Name"] = df["Name"].apply(lambda s: s.replace("\r", " "))

def join_split_name(df1, df2):
    if df2["Roll Number"][0].startswith("Unnamed"):
        last_name = df2["Name"][0]
        df2.drop(0, inplace = True)
        df2.reset_index(drop = True, inplace = True)
        column = df1["Name"]
        first_name = column[len(column) - 1]
        df1["Name"][len(column) - 1] = first_name + " " + last_name

def numerify_division_tutorial_lab(df):
    for column in ["Division", "Tutorial", "Lab"]:
        df[column] = df[column].apply(lambda s: int(re.compile(r"\d+").findall(s)[0]))

def stringify_roll_number(df):
    df["Roll Number"] = df["Roll Number"].apply(lambda x: str(x))

def add_branch_and_branch_codes(df):
    branch_number = df["Roll Number"][0][2:5]
    branch_info = mapping[branch_number]
    df["Branch"] = branch_info[0]
    df["Branch Code"] = branch_info[1]

# Get a list of dataframes; one dataframe for each table in each page
dfs = tabula.read_pdf(input_str, pages = "all")

for df in dfs:
    remove_first_column(df)
    add_column_labels(df)
    remove_newline_from_names(df)

for (df1, df2) in zip(dfs, dfs[1:]):
    join_split_name(df1, df2)

for df in dfs:
    numerify_division_tutorial_lab(df)
    stringify_roll_number(df)
    add_branch_and_branch_codes(df)

pandas.concat(dfs).to_excel(output, index = False)