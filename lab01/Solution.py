""" EXERCISE 1

File proj1_ex01.csv is a properly formed CSV file, with fields separated using commas (,) and
with column headers. Load it into a DataFrame.
Create a file called ex01_fields.json, which contains information all the columns in the file
you read. The file should contain an array of dictionaries with the following items:
• column name (key: name),
• percentage of missing values (key: missing, values in the range [0.0, 1.0]),
• data type as a string with the following values key: type:
– int for integer types,
– float for floating-point types,
– other for all other types.
An example JSON file could look like this:
[
    {
        "name": "id",
        "missing": 0.0,
        "type": "int"
    },
    {
        "name": "title",
        "missing": 0.2,
        "type": "other"
    },
    {
        "name": "result",
        "missing": 0.73,
        "type": "float"
    }
]
"""

import pandas as pd
import json
import numpy as np
import re

df = pd.read_csv('lab1_ex01.csv')
table = []

for col in df.columns:
    if df[col].dtype == 'int64':
        d_type = 'int'
    elif df[col].dtype == 'float64':
        d_type = 'float'
    else:
        d_type = 'other'
    table.append({'name': col, 'missing': df[col].isnull().sum() / len(df), 'type': d_type})

with open('ex01_fields.json', 'w') as file:
    json.dump(table, file)

""" EXERCISE 2

Compute statistics for all columns in your dataframe.
For numeric columns include:
• the count of non-empty values (count),
• the average (mean),
• the standard deviation (std),
• the minimum (min) and maximum (max) values,
• the the 25th, 50th, and 75th percentiles (attribute names: 25%, 50% and 75%, respectively).
For non-numeric columns include:
• the count of non-empty values (count),
• the number of unique values (unique),
• the most common value (top) and its frequency (number of occurrences; freq).
Save the result to a JSON file called ex02_stats.json which contains a dictionary at the top level;
the keys in the dictionary are column names, and the values are dictionaries with keys as described
above, e.g.:
{
    "some_number":{
        "count":6.0,
        "mean":-0.5009940002,
        "std":0.8839385203,
        "min":-1.5552904133,
        "25%":-1.2470386925,
        "50%":-0.4162433767,
        "75%":0.1799426841,
        "max":0.5271122589
    },
    "some_string":{
        "count":7,
        "unique":3,
        "top":"good",
        "freq":3,
    }
}
In the inner dictionaries, keys with null values are allowed, e.g. a dictionary for a numeric column
may contain the unique and top attributes.
"""

dict_ = {}

for col in df.columns:
    if df[col].dtype == np.int64 or df[col].dtype == np.float64:
        dict_[col] = {'count': df[col].value_counts(),
                      'mean': df[col].notnull().mean(),
                      'std': df[col].notnull().std(),
                      'min': df[col].notnull().min(),
                      '25%': df[col].quantile(0.25),
                      '50%': df[col].quantile(0.50),
                      '75%': df[col].quantile(0.75),
                      'max': df[col].notnull().max()}
    else:
        print(df[col].value_counts().idxmax())
        dict_[col] = {'count': df[col].value_counts(),
                      'unique': df[col].nunique(),
                      'top': df[col].value_counts().idxmax(),
                      'freq': df[col].value_counts().max()}

s = pd.Series(dict_).to_json()
with open('ex02_stats.json', 'w') as file:
    file.write(s)

"""
EXERCISE 3

Rename (“normalize”) the columns in the dataframe, so that they (sort of) follow the PEP 8
guidelines for variable names.
Apply the following rules:
• keep only characters which belong to the [A-Za-z0-9_ ] class (capital and small letters,
digits, underscore and space),
• convert all letters to lowercase,
• replace all spaces with underscores (_).
Make the changes in your DataFrame persistent.
Save the DataFrame with the new columns to ex03_columns.csv (don’t include the index)
"""


for col in df.columns:
    new_col = re.sub(r'[^\w\s]', '', col)
    new_col = new_col.lower()
    new_col = new_col.replace(' ', '_')
    df = df.rename(columns={col: new_col})

df.to_csv('ex03_columns.csv')

""" EXERCISE 4

Write the data in the DataFrame to various output formats.
Create an MS Excel file called ex04_excel.xlsx, which contains the column headers, but not the
index values.
Create a JSON file called ex04_json.json, which contains an array of rows stored as dictionaries,
each with the DataFrame columns as keys (and values as values, obviously), e.g.:
[
    {
        "one":0.3485539245,
        "two":"-0.14509562920877161",
        "three":"-0.012336991474672475",
        "four":9,
        "five":"red",
        "six":"good",
        "seven":"quarrelsome",
        "eight":"2016-05-26 09:33:42"
    },
    {
        "one":-1.4938530178,
        "two":"0.12436946488785079",
        "three":"1.4611100361038865",
        "four":4,
        "five":"red",
        "six":"bad",
        "seven":"doctor",
        "eight":"2016-12-03 18:55:52"
    }
]
Create a pickle file called ex04_pickle.pkl with the DataFrame.
"""

df = pd.read_csv('lab1_ex01.csv')
df.to_excel('ex04_excel.xlsx', index=False)

r = df.to_dict('records')
with open('ex04_json.json', 'w') as file:
    json.dump(r, file)
df.to_pickle('ex04_pickle.pkl')

""" EXERCISE 5

Load the DataFrame pickled in file lab1_ex05.pkl.
Select the following items from the DataFrame:
• the 2nd and 3rd columns (regardless of their names),
• rows whose index values begin with the letter v.
Save the result to a Markdown table stored in file ex05_table.md. Include the result, but don’t
put anything in cells with missing values (i.e. prevent nan from being printed there).
"""

df = pd.read_pickle('lab1_ex05.pkl')
df2 = df.iloc[df.index.str.startswith('v'), 1:3]
df2 = df2.fillna('')

df3 = df.iloc[1:3]
df3 = df3.fillna('')

with open('ex05_table.md', 'w') as file:
    file.write(df2.to_markdown())
    file.write(df3.to_markdown())

""" EXERCISE 6

Pandas DataFrames are two-dimensional structures. However, data in JSON files often has a
hierarchical structure, e.g. objects (dictionaries) are nested within objects.
File lab1_ex06.json contains an array with such hierarchical objects (the structure of each array
element is the same).
Using the data in the file, create a Pandas DataFrame, which contains a flattened version of the
data. For nested dictionaries, the column names should have the keys separated using dots (.).
E.g., for the following entry:
[
    {
    "brand": "Audi",
    "name": "Q5",
    "model": 2023,
        "engine": {
        "type": "Diesel",
        "displacement": "2.0L",
        "power": "190 hp",
        "environmental": {
                "euro": 6,
                "filter": "DPF"
            }
        }
    },
]
the resulting columns should be:
    • brand,
    • model,
    • year,
    • engine.type,
    • engine.displacement,
    • engine.power,
    • engine.environmental.euro,
    • engine.environmental.filter.
Save the resulting DataFrame to pickle file ex06_pickle.pkl.
"""

with open('lab1_ex06.json', 'r') as file:
    x = json.load(file)

df = pd.json_normalize(x, sep='.', max_level=2)
df = df[['brand', 'model', 'year', 'engine.type', 'engine.displacement', 'engine.power', 'engine.environmental.euro',
         'engine.environmental.filter']]
df.to_pickle('ex06_pickle.pkl')
