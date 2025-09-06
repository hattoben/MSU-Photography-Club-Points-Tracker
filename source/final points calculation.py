from involve import concatenateInvolveData
from events import concatenateEventsData
import pandas as pd

involve_data = concatenateInvolveData("involve data here")
events_data = concatenateEventsData("events data here")

grand_total = pd.concat([involve_data, events_data])
print(grand_total)