# Ben Hatto - 9.5.25
# This file calculates points using a

import os
import pandas as pd

def concatenateOtherData(path):
    other_data = pd.DataFrame()
    attendance_value = { #in number of points per hour
        "Driving" : 10,
        "Other" : 5
    }

    print("These involve data sources will be used:")
    all_entries = os.listdir(path)
    for entry in all_entries:
        #list all files in data here folder
        if entry.startswith('.'):  # to ignore any hidden file
            continue
        print(os.path.join(path, entry))

        #read as dataframe
        df = pd.read_csv(os.path.join(path, entry), skiprows = 1,
                         names = ["First Name", "Last Name", "NetID", "Activity", "Hours", "Points"])

        #combine to one dataframe
        other_data = pd.concat([other_data, df], ignore_index=True)

    # remove "@msu.edu" from netid column
    other_data["NetID"] = other_data["NetID"].str[:-8]

    for row in other_data.itertuples():
        if row[4] in attendance_value:
            other_data.at[row.Index, other_data.columns[5]] = attendance_value[row[4]] * float(row[5])

    other_data.drop("Activity", axis=1, inplace=True)
    other_data.drop("Hours", axis=1, inplace=True)
    return other_data