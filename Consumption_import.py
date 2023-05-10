import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# imports the full salient stats csv in the form it was downloaded from USGS
salient_stats = pd.read_csv('mcs2022-alumi_salient.csv')

# imports the import source dataset built in previous steps downloaded from USGS
import_source_raw = pd.read_csv("Import_Source_Pct.csv")

# sets the commodity based on the value in teh commodity column of the salient stats csv
commodity = salient_stats['Commodity'][0]

# extracts the rows where the metal name in import source matches the commodity name in the salient stats
import_source = import_source_raw[import_source_raw['Metal'] == commodity]

# subsets the import_source subset for specific columns needed to build stacked bar chart
import_source_slice = import_source[['Percentage', 'Country', 'Category']]

# outputs list of columns, used for EDA

# creates variable for consumption column within salient stats csv
consumption = salient_stats['Consump_kt']

salient_stats['Consumption'] = salient_stats['Consump_kt']

# calculates the volume of imports using net import reliance based on consumption from salient stats
salient_stats['calculated_imports'] = consumption * salient_stats['NIR_pct'] / 100

# calculates the volume of consumption that was not imported that will be used in the stacked barchart

salient_stats['non_imported_consumption'] = consumption - salient_stats['calculated_imports']

# subsets salient stats using calculated imports for use in viz
imports_by_year = salient_stats[['Year', 'Consumption', 'calculated_imports', 'non_imported_consumption']]

# melts the imports_by_year df to allow plotting of three columns as variables
melted_df = pd.melt(imports_by_year, id_vars='Year' )

fig = px.line(melted_df, x='Year', y='value',color='variable')
fig.show()


import_source_slice['country_amount'] = salient_stats['calculated_imports'] * import_source_slice['Percentage'] /100
import_source_slice['Commodity'] = commodity


#columns = import_source_slice.columns.values.tolist()


fig2 = px.bar(import_source_slice, x="Commodity", y="country_amount", color="Category", title="Stacked Bar Chart")
fig2.show()


#print(columns)
