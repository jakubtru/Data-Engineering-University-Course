"""
Create a DataFrame from a file called proj2_data.csv, knowing that:
• it contains more than one column,
• the separator is either |, ; or ,,
• at least one column contains pure floating-point numbers,
• the decimal part is separated using . or ,,
• the decimal separator does not collide with the column separator,
• thousands are not grouped,
• all columns containing pure floating-point numbers have the same format,
1
• the file also contains text columns.
The DataFrame obtained by loading the file will be referred to as our initial DataFrame.
Save the DataFrame, as imported, to proj2_ex01.pkl.
"""

import pandas as pd
import csv
import pickle
import re
from collections import Counter

with open('proj2_data.csv', newline='') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

long_string = ''.join([item for sublist in data for item in sublist])
counter = Counter(long_string)
separator = counter.most_common(1)[0][0]

df = pd.read_csv('proj2_data.csv', sep=separator, decimal=',', engine='python')
df['tasks_avg'] = df['tasks_avg'].round(2)

df.to_pickle("proj2_ex01.pkl")

"""
The file proj2_scale.txt contains strings, one in each line, forming a scale. Subsequent values
are (implicitly) associated with natural numbers 1, 2, 3, … , 𝑛. For instance, given a file with values:
very bad
bad
average
good
very good
the value very bad should be associated with 1, and the value very good – with 5.
Create a copy of the initial DataFrame. Locate columns in which the values are a subset of the values
loaded from the text file. In these columns, replace the values with their numeric counterparts.
Save the resulting DataFrame to proj2_ex02.pkl.
"""

copy = df.copy(deep=True)

with open('proj2_scale.txt') as file:
    grades = file.read().splitlines()

columns_found = []

for col in copy:
    columns_found.append(col)
    for el in df[col].tolist():
        if el not in grades:
            columns_found.remove(col)
            break

dict_ = {}
n = 1
for grade in grades:
    dict_[grade] = n
    n += 1

for col in columns_found:
    for i in range(len(df[col])):
        copy[col][i] = dict_[df[col][i]]
copy.head()
copy.to_pickle("proj2_ex02.pkl")

"""
Create another copy of the initial DataFrame. Change the type of columns identified in Exercise 2
to categorical. Set the categories for these columns to reflect the entire list loaded from the text
file, even if not all values are present in the source data.
Save the resulting DataFrame to proj2_ex03.pkl.
"""

copy2 = df.copy(deep=True)
for col in columns_found:
    copy2[col] = df[col].astype("category")
    copy2[col] = copy2[col].cat.set_categories(grades)

copy2.to_pickle("proj2_ex03.pkl")

"""
In the initial DataFrame, find columns which:
• contain text data,
• contain no more than 10 unique values,
• only have values consisting of small letters, i.e. the [a-z] range,
• have values that do not appear in the text file loaded in Exercise 2.
For these columns, perform one-hot encoding, obtaining a separate DataFrame with encoded values
for each original column. The column names should match the values within the column, without
any prefixes or suffixes.
For example, for a column that contains 3 distinct values, red, green, and blue, column names in
the resulting DataFrame should be exactly that – red, green, and blue.
Save the DataFrame created for each column to files named proj2_ex05_X.pkl, where X is a
subsequent natural number, e.g. 1, 2, 3, etc. (e.g. proj2_ex05_1.pkl, proj2_ex05_2.pkl).
"""

pattern = '^[a-z]+$'

table1 = df.columns[df.nunique() <= 10]

table2 = []
for col in table1:
    if df[col].dtype == 'object' and df[col].str.match(pattern).all():
        table2.append(col)

table3 = []
for col in table2:
    table3.append(col)
    for x in df[col]:
        if x in grades:
            table3.remove(col)
            break

for col in table3:
    encoded_df = pd.get_dummies(df[col], prefix='', prefix_sep='')
    encoded_df.to_pickle(f'proj2_ex05_{table3.index(col) + 1}.pkl')
