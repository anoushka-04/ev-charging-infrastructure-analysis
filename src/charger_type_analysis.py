import pandas as pd
from rapidfuzz import process, fuzz

# Load raw datasets
charging_df = pd.read_csv('data/ev-charging-stations-india.csv')
ev_sales_df = pd.read_csv('data/EV_Dataset.csv')
population_state_df = pd.read_csv('data/state_wise_population__2019.csv')

# Standardize state names (lowercase and strip)
charging_df['state'] = charging_df['state'].str.lower().str.strip()
ev_sales_df['state'] = ev_sales_df['State'].str.lower().str.strip()
population_state_df['state'] = population_state_df['State'].str.lower().str.strip()

# Official list of Indian states (can be extended)
official_states = [
    'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chhattisgarh', 'goa',
    'gujarat', 'haryana', 'himachal pradesh', 'jharkhand', 'karnataka', 'kerala',
    'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
    'odisha', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura',
    'uttar pradesh', 'uttarakhand', 'west bengal', 'delhi', 'jammu and kashmir',
    'ladakh'
]

# Function to fuzzy match state names to official list
def clean_state_name(name, choices=official_states, scorer=fuzz.ratio, threshold=80):
    if pd.isna(name):
        return None
    match, score, _ = process.extractOne(name, choices, scorer=scorer)
    if score >= threshold:
        return match
    else:
        return name  # or None if you want to discard unmatched

# Apply fuzzy matching to clean state names
charging_df['state_clean'] = charging_df['state'].apply(lambda x: clean_state_name(x))
ev_sales_df['state_clean'] = ev_sales_df['state'].apply(lambda x: clean_state_name(x))
population_state_df['state_clean'] = population_state_df['state'].apply(lambda x: clean_state_name(x))

# Use cleaned state names in further processing
# Clean charging station 'type' column: remove missing or invalid entries
charging_df = charging_df[charging_df['type'].notna()]

# Convert charger type to numeric (for consistency)
charging_df['type'] = pd.to_numeric(charging_df['type'], errors='coerce')
charging_df = charging_df[charging_df['type'].notna()]

# Aggregate charger counts by cleaned state and charger type
charger_type_counts = charging_df.groupby(['state_clean', 'type']).size().reset_index(name='charger_count')

# Aggregate EV sales quantity by cleaned state
sales_per_state = ev_sales_df.groupby('state_clean')['EV_Sales_Quantity'].sum().reset_index()

# Merge charger counts with EV sales demand by cleaned state
supply_demand_overall = pd.merge(charger_type_counts, sales_per_state, left_on='state_clean', right_on='state_clean', how='left')

# Fill missing EV sales with zero
supply_demand_overall['EV_Sales_Quantity'] = supply_demand_overall['EV_Sales_Quantity'].fillna(0)

# Calculate charger-to-demand ratio
supply_demand_overall['charger_to_demand_ratio'] = supply_demand_overall.apply(
    lambda row: row['charger_count'] / row['EV_Sales_Quantity'] if row['EV_Sales_Quantity'] > 0 else None,
    axis=1
)

# Charger type mapping dictionary
charger_type_map = {
    '6.0': 'Level 1 AC (Slow Charger)',
    '7.0': 'Level 2 AC (Fast Charger)',
    '8.0': 'Level 2 AC (Fast Charger) - Variant',
    '10.0': 'Level 3 DC (Rapid Charger)',
    '11.0': 'Level 1 AC (Slow Charger) - Variant',
    '12.0': 'Level 2 AC (Fast Charger) - Variant 2',
    '13.0': 'Level 3 DC (Rapid Charger) - Variant',
    '14.0': 'Level 3 DC (Ultra Fast)',
    '15.0': 'Bharat AC-001',
    '16.0': 'Bharat DC-001',
    '17.0': 'CCS Type 2',
    '18.0': 'CHAdeMO',
    '19.0': 'Type 2 AC',
    '20.0': 'GB/T AC',
    '21.0': 'GB/T DC',
    '22.0': 'Tesla Supercharger',
    '23.0': 'Other AC Charger',
    '24.0': 'Other DC Charger'
}

# Format 'type' column and map to charger type names
supply_demand_overall['type_str'] = supply_demand_overall['type'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else None)
supply_demand_overall['charger_type_name'] = supply_demand_overall['type_str'].map(charger_type_map).fillna('Unknown')

# Clean population data similarly
population_state_df = population_state_df[['state_clean', 'total_population']]
population_state_df['total_population'] = pd.to_numeric(population_state_df['total_population'], errors='coerce')
population_state_df = population_state_df.dropna(subset=['total_population'])

# Save cleaned datasets
supply_demand_overall.to_csv('data/cleaned_supply_demand_by_charger_type.csv', index=False)
population_state_df.to_csv('data/cleaned_population_by_state.csv', index=False)

# Debug info
print("Sample cleaned states in charger data:", charging_df['state_clean'].unique()[:10])
print("Sample cleaned states in EV sales data:", ev_sales_df['state_clean'].unique()[:10])
print("Sample supply-demand data preview:")
print(supply_demand_overall.head())
