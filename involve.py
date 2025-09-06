# Ben Hatto - 9.5.25
# This file combines multiple sources of data - multiple invovle@state attendance involve data - into
# one dataframe for ease of calculation

import os
import pandas as pd

def concatenateInvolveData(path):
    involve_data = pd.DataFrame()
    attendance_value = 5

    print("These involve data will be used:")
    all_entries = os.listdir(path)
    for entry in all_entries:
        #import list all csv involve data
        print(os.path.join(path, entry))

        #read as dataframe
        df = pd.read_csv(os.path.join(path, entry), usecols = [0, 1, 2], skiprows = 6,
                         names = ["First Name", "Last Name", "NetID"])

        #combine to one dataframe
        involve_data = pd.concat([involve_data, df], ignore_index=True)

    # remove "@msu.edu" from netid column
    involve_data["NetID"] = involve_data["NetID"].str[:-8]

    df_unique = (
        involve_data.groupby(["First Name", "Last Name", "NetID"])
        .size()  # count rows in each group
        .reset_index(name="Attendance")  # turn into a column
    )

    # multiply by 5 to get points, then add points column
    df_unique["Points"] = df_unique["Attendance"] * attendance_value

    # Sort by highest count
    involve_data = df_unique.sort_values(by="Attendance", ascending=False).reset_index(drop=True)
    return involve_data