import pickle
import pandas
import re
from math import isnan

file = open("dfs", "rb")
dfs = pickle.load(file)
file.close()

def split_roll_number_name(df, index):
    roll_numbers = []
    names = []
    roll_name = df[df.columns[index]]

    for i in range(len(roll_name)):
        split_entry = roll_name[i].split(' ')
        roll_numbers.append(split_entry[1])
        names.append(' '.join(split_entry[2:]))

    del df[df.columns[index]]
    df.insert(index, "Roll Numbers", roll_numbers)
    df.insert(index + 1, "Names", names)

def split_division_tutorial_lab(df, index):
    divisions = []
    tutorials = []
    labs = []
    divison_tutorial_lab = df[df.columns[index]]

    for i in range(len(divison_tutorial_lab)):
        if not isinstance(divison_tutorial_lab[i], str) and isnan(divison_tutorial_lab[i]):
            divisions.append(float("nan"))
            tutorials.append(float("nan"))
            labs.append(float("nan"))
        else:
            split_entry = divison_tutorial_lab[i].split(' ')
            divisions.append(' '.join(split_entry[:2]))
            tutorials.append(' '.join(split_entry[2:4]))
            labs.append(' '.join(split_entry[4:]))

    del df[df.columns[index]]
    df.insert(index, "Division", divisions)
    df.insert(index + 1, "Tutorial", tutorials)
    df.insert(index + 2, "Lab", labs)

def split_division_tutorial(df, index):
    divisions = []
    tutorials = []
    divison_tutorial_lab = df[df.columns[index]]

    for i in range(len(divison_tutorial_lab)):
        if not isinstance(divison_tutorial_lab[i], str) and isnan(divison_tutorial_lab[i]):
            divisions.append(float("nan"))
            tutorials.append(float("nan"))
        else:
            split_entry = divison_tutorial_lab[i].split(' ')
            divisions.append(' '.join(split_entry[:2]))
            tutorials.append(' '.join(split_entry[2:]))

    del df[df.columns[index]]
    df.insert(index, "Division", divisions)
    df.insert(index + 1, "Tutorial", tutorials) 

def split_merged_rows(df):
    if len(df.columns) == 2:
        split_roll_number_name(df, 0)
        split_division_tutorial_lab(df, 2)
    if len(df.columns) == 3:
        split_roll_number_name(df, 0)
        split_division_tutorial(df, 2)
    elif len(df.columns) == 4:
        try:
            split_roll_number_name(df, 0)
        except AttributeError:
            split_division_tutorial_lab(df, 3)

def remove_first_column(df):
    if len(df.columns) == 6:
        df.drop(df.columns[0], axis = 1, inplace = True)

def add_column_labels(df):
    df.set_axis(["Roll Number", "Name", "Division", "Tutorial", "Lab"], axis = 1, inplace = True)

def remove_NaNs(df):
    column = df["Division"]
    for i in range(len(column)):
        if not isinstance(column[i], str) and isnan(column[i]):
            df.drop(i, inplace = True)

def numerify_division_tutorial_lab(df):
    for column in ["Division", "Tutorial", "Lab"]:
        df[column] = df[column].apply(lambda s: int(re.compile(r"\d+").findall(s)[0]))

for df, i in zip(dfs, range(len(dfs))):
    try:
        split_merged_rows(df)
        remove_first_column(df)
        add_column_labels(df)
        remove_NaNs(df)
        numerify_division_tutorial_lab(df)
    except IndexError:
        print(i)