import pandas, pickle, re
from math import isnan

def remove_first_column(df):
    df.drop(df.columns[0], axis = 1, inplace = True)

def add_column_labels(df):
    df.set_axis(["Roll Number", "Name", "Division", "Tutorial", "Lab"], axis = 1, inplace = True)

def remove_NaNs(df):
    column = df["Name"]
    for i in range(len(column)):
        if not isinstance(column[i], str) and isnan(column[i]):
            df.drop(i, inplace = True)

def numerify_division_tutorial_lab(df):
    def find_number(s):
        if not isinstance(s, str) and isnan(s):
            return 0
        return int(re.compile(r"\d+").findall(s)[0])
    for column in ["Division", "Tutorial", "Lab"]:
        df[column] = df[column].apply(find_number)

def remove_newline_from_names(df):
    df["Name"] = df["Name"].apply(lambda s: s.replace("\r", " "))

def stringify_roll_number(df):
    def roll_number_to_string(s):
        if isinstance(s, str):
            return s
        return str(int(s))
    df["Roll Number"] = df["Roll Number"].apply(roll_number_to_string)
    df.reset_index(drop = True, inplace = True)

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
    "B09": ("Mathematics", "MA"),
    "U13": ("BDes", "DE")
}

def add_branch_and_branch_codes(df):
    branch_number = df["Roll Number"][0][2:5]
    branch_info = mapping[branch_number]
    df["Branch"] = branch_info[0]
    df["Branch Code"] = branch_info[1]

def cleanup(dfs):
    for df in dfs:
        remove_first_column(df)
        add_column_labels(df)
        remove_NaNs(df)
        numerify_division_tutorial_lab(df)
        remove_newline_from_names(df)
        stringify_roll_number(df)
        add_branch_and_branch_codes(df)