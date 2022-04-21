import glob
import pandas as pd
import matplotlib.pyplot as plt
from  matplotlib.ticker import FuncFormatter
import seaborn as sb
import numpy as np

international_path = 'data/International'
international_files = glob.iglob(international_path + "/*.csv")

# Create empty dataframe
international_df = pd.DataFrame()
# Consolidate data into one frame
for f in international_files:
    df = pd.read_csv(f)
    # Split dataframe into multiple frames, by month
    splitByMonth = [y for x, y in df.groupby('MONTH', as_index=False)]
    for frame in splitByMonth:
        # Sum the number of passengers, distanced travelled, etc.
        numPassengers = frame['PASSENGERS'].sum()
        distanceTravelled = frame['DISTANCE'].sum()
        numUniqueAirlines = frame['UNIQUE_CARRIER_NAME'].nunique()
        numUniqueDestinations = frame['DEST'].nunique()
        Year = frame['YEAR'].iloc[0]
        month = frame['MONTH'].iloc[0]

        # Add the information into a dictionary to store
        dict = {'Number of Passengers': numPassengers, 'Total distance':distanceTravelled, 'Number of Carriers':numUniqueAirlines,
                'Number of Destinations':numUniqueDestinations, 'Year':Year,'Month':month}
        # Append to final dataframe
        international_df = international_df.append(dict,ignore_index=True)


international_df = international_df.sort_values('Year')
international_df['Year'] = international_df['Year'].astype(int)

""" BAR PLOT """
sb.set(rc = {'figure.figsize':(18,8)})
sb.set_style("white")

# Plot yearly number of carriers
plot = sb.barplot(data=international_df, x="Year", y="Number of Carriers",palette="rocket",ci=None)
sb.despine()
plt.savefig('carriers.png')
plt.clf() # clear figure

""" LINE GRAPH """

# Convert month column from numbers to names
international_df['Month Name'] = pd.to_datetime(international_df['Month'], format='%m').dt.month_name().str.slice(stop=3)

# Plot number of passengers
plot = sb.relplot(data=international_df, x="Year", y="Number of Passengers", hue="Month Name", kind="line",palette="magma")
plot.set(xlim=(1991, 2021))
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x))) # Make x ticks int instead of float
plt.savefig('line-chart.png')
plt.clf() # clear figure

""" HEAT MAP """

# Remove rows with missing data
international_df.dropna(inplace=True)
# Remove unnecessary columns
international_df = international_df.filter(['Year', 'Month','Number of Passengers'])

international_df['Year'] = pd.to_numeric(international_df.Year, errors='coerce')
# Group by month and Year, get the average
international_df = international_df.groupby(['Month', 'Year']).mean()
international_df = international_df.unstack(level=0)

# Plot heatmap
ax = sb.heatmap(international_df)

ax.xaxis.tick_top() # put ye labels at top of chart
xticks_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(np.arange(12), labels=xticks_labels)
# Remove Axis Labels
plt.xlabel('')
plt.ylabel('')
plt.savefig('heatmap.png')



