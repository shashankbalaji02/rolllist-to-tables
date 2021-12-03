import re
import pandas

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

def cleanup(dfs):
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