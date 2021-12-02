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
dfs = tabula.read_pdf("/mnt/d/Downloads/Roll-List.pdf", pages = "all")

for df in dfs:
    # Drop the first column in each dataframe
    df.drop(df.columns[0], axis = 1, inplace = True)

    # Set the correct column lables
    df.set_axis(["Roll Number", "Name", "Division", "Tutorial", "Lab"], axis = 1, inplace = True)

    length = len(df["Lab"])
    i = 0
    while i < length:
        if df["Lab"][i] == float("NaN"):
            df["Name"][i - 1] = df["Name"][i - 1] + " " + df["Name"][i]
            df.drop(i, inplace = True)
            i = i - 1
            length = length - 1
        i = i + 1