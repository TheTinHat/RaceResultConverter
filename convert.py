import pandas as pd
import requests
import re

url = input("Enter the StartLineTiming URL: ")

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

if url[-1] == "/":
    url = url[0:-1]

# If URL ends in a number, remove it
if url.split("/")[-1].isnumeric():
    url = "/".join(url.split("/")[0:-1])

# If URL doesn't end in 'page', add it
if url.split("/")[-1] != "page":
    url = "/".join([url, "page"])

# Fetch first page and convert it to a dataframe
print("Fetching page 1")
results = requests.get(url, headers=header).content
df = pd.read_html(results)[0]

# Attempt to paginate
paginate = True
page_num = 2
while paginate:
    # Add page number to url
    print(f"Fetching page {page_num}")
    url_paginated = "/".join([url, str(page_num)])

    # Try fetching the paginated page and loading it into a dataframe
    try:
        results = requests.get(
            url_paginated, allow_redirects=False, headers=header
        ).content
        page_df = pd.read_html(results)[0]
    except:
        paginate = False
        continue

    # Append page dataframe to main dataframe
    df = pd.concat([df, page_df])
    page_num += 1

# Rename some columns
if 'Chip Time' in df.columns:
    df = df.rename(
        columns={
            "Race #": "bib",
            "City": "city",
            "Place": "place",
            "Name": "full_name",
            "Chip Time": "time",
        }
    )
elif 'Gun Time' in df.columns:
    df = df.rename(
        columns={
            "Race #": "bib",
            "City": "city",
            "Place": "place",
            "Name": "full_name",
            "Gun Time": "time",
        }
    )

# Convert some columns
df["gender"] = df["Division"].astype(str).str[0]
df["place"] = df["place"].str.split(pat="/", n=0, expand=True)[0]
df[["city", "state"]] = df["city"].str.split(pat=", ", n=1, expand=True)
df[["last", "first"]] = df["full_name"].str.split(pat=", ", n=1, expand=True)
df["last"] = df["last"].str.title()
df["age"] = df["Division"].str.slice(1, 3)
df["age"] = pd.to_numeric(df["age"], errors='coerce')

# Drop rows that don't have division (i.e. age and gender)
df = df[df["Division"].notna()]

# Fill cells without data with 'NA'
df = df.fillna("NA")
df.loc[df['age'] == "NA", 'age'] = 0

# Remove numbers and special characters from names
df['last'] = df['last'].apply(lambda string: re.sub(r"[^a-zA-Z]+", ' ', string))
df['first'] = df['first'].apply(lambda string: re.sub(r"[^a-zA-Z]+", ' ', string))
df['city'] = df['city'].apply(lambda string: re.sub(r"[^a-zA-Z]+", ' ', string))

# Drop rows that are DNF as ultrasignup errors out if time is zero.
df = df[df["place"] != "DNF"]
df = df[df["place"] != "NA"]

# Reorganize columns and trim down dataframe
df = df[["place", "time", "first", "last", "age", "gender", "city", "state", "bib"]]

print(df)

# Save to file
df.to_csv("race_results.csv", index=False)
print("Saved to race_results.csv")