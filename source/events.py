# Ben Hatto - 9.5.25
# This file calculates point totals from the events attendance spreadsheet

import re
import unicodedata
import os
import pandas as pd

    # Name normalization helper
def normalize_name(x: str) -> str:
    s = str(x).strip()
    # remove accents/diacritics
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    # keep only letters, spaces, apostrophes, hyphens
    s = re.sub(r"[^A-Za-z\s'\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.title()
    # take only the first token (everything before the first space)
    if " " in s:
        s = s.split(" ")[0]
    return s

def concatenateEventsData(path):
    events_data = pd.DataFrame()
    attendance_value = 10 #per hr - if the points value of event changes, change me!!!

    print("These events data sources will be used:")
    all_entries = os.listdir(path)
    for entry in all_entries:
        if entry.startswith('.'):  # to ignore any hidden file
            continue

        # list all files in events data here folder
        print(os.path.join(path, entry))

        #read as dataframe
        df = pd.read_csv(os.path.join(path, entry), usecols = [3, 5], skiprows = 10,
                         names = ["First Name", "Hours"])
        #drop NaN
        df = df.dropna()

        events_data = pd.concat([events_data, df])

    # remove "@msu.edu" from netid column
    #involve_data["NetID"] = involve_data["NetID"].str[:-8]

    # Ensure Hours is numeric (handles "2 hours", "1.5", etc.)
    events_data["Hours"] = (
        events_data["Hours"].astype(str).str.extract(r"(\d+\.?\d*)")[0]
        .pipe(pd.to_numeric, errors="coerce")
    )

    #squish duplicate names into one row for each person

    # Apply normalization
    events_data["First Name"] = events_data["First Name"].map(normalize_name)

    # Aggregate to one row per cleaned name with total hours
    events_data = (events_data.groupby("First Name", as_index=False, dropna=False)
           .agg(Hours=("Hours", "sum")))

    # calculate points earned
    events_data["Points"] = events_data["Hours"] * attendance_value

    #sort descending
    events_data = events_data.sort_values(by="Points", ascending=False).reset_index(drop=True)
    return events_data