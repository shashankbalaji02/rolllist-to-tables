import pandas
import re
from math import isnan

def remove_first_column(df):
    df.drop(df.columns[0], axis = 1, inplace = True)

def add_column_labels(df):
    if df[df.columns[0]][0] == "Number":
        df.drop(0, inplace = True)
        df.reset_index(drop = True, inplace = True)
    elif df.columns[0] == "Roll\rNumber":
        pass
    else:
        df.loc[-1] = list(df)
        df.index = df.index + 1
        df.sort_index(inplace = True) 
    df.set_axis(["Roll Number", "Name", "Division", "Tutorial", "Lab"], axis = 1, inplace = True)

def remove_newline_from_names(df):
    df["Name"] = df["Name"].apply(lambda s: s.replace("\r", " "))

def remove_NaNs(df):
    column = df["Roll Number"]
    length = len(column)
    j = 1
    for i in range(length):
        if not isinstance(column[i], str) and isnan(column[i]):
            df["Name"][i - j] = df["Name"][i - j] + " " + df["Name"][i]
            df.drop(i, inplace = True)
            j = j + 1
        else:
            j = 1

def numerify_division_tutorial_lab(df):
    for column in ["Division", "Tutorial", "Lab"]:
        df[column] = df[column].apply(lambda s: int(re.compile(r"\d+").findall(s)[0]))

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

def add_branch_and_branch_codes(df):
    branch_number = df["Roll Number"][0][2:5]
    branch_info = mapping[branch_number]
    df["Branch"] = branch_info[0]
    df["Branch Code"] = branch_info[1]

def stringify_roll_number(df):
    df["Roll Number"] = df["Roll Number"].apply(lambda x: str(x))

def cleanup(dfs):
    for df in dfs:
        remove_first_column(df)
        add_column_labels(df)
        remove_newline_from_names(df)
        remove_NaNs(df)
        numerify_division_tutorial_lab(df)
        stringify_roll_number(df)
        add_branch_and_branch_codes(df)