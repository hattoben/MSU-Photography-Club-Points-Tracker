from involve import concatenateInvolveData
from events import concatenateEventsData
from other import concatenateOtherData
import pandas as pd

involve_data = concatenateInvolveData("../involve data here")
events_data = concatenateEventsData("../events data here")
other_data = concatenateOtherData("../other data here")
data = pd.concat([involve_data, events_data, other_data])

unique_names = dict()

for row in data.itertuples():
    if row[1] not in unique_names:
        unique_names[row[1]] = [row[1], row[2], row[5]]
    elif row[1] in unique_names:
        unique_names[row[1]][2] += float(row[5])

grand_total = pd.DataFrame.from_dict(unique_names, orient='index', columns=["First Name", "Last Name", "Grand Total"])
grand_total = grand_total.sort_values(by = "Grand Total", ascending = False)

grand_total.to_csv("../points total.csv")
print("Success!!!")