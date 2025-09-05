import pandas as pd

# Load datasets (update filenames as needed)
charging_df = pd.read_csv('data/ev-charging-stations-india.csv')
ev_sales_df = pd.read_csv('data/EV_Dataset.csv')
population_state_df = pd.read_csv('data/state_wise_population__2019.csv')

# Now the rest of your existing analysis code can follow here, e.g.
charging_df['state'] = charging_df['state'].str.lower().str.strip()
ev_sales_df['state'] = ev_sales_df['State'].str.lower().str.strip()
population_state_df['state'] = population_state_df['State'].str.lower().str.strip()

# Aggregate charging stations count per state (previous aggregation)
stations_per_state = charging_df.groupby('state').size().reset_index(name='stations_count')

# Aggregate EV sales per state (previous aggregation)
sales_per_state = ev_sales_df.groupby('state')['EV_Sales_Quantity'].sum().reset_index()

# Merge stations count and sales by state
state_merged = pd.merge(stations_per_state, sales_per_state, on='state', how='inner')

# Merge population data by state
final_df = pd.merge(state_merged, population_state_df[['state', 'total_population']], on='state', how='left')

# Calculate per capita metrics in overall merged data
final_df['stations_per_capita'] = final_df['stations_count'] / final_df['total_population']
final_df['sales_per_capita'] = final_df['EV_Sales_Quantity'] / final_df['total_population']

