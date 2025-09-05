import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned charger type supply-demand data
data = pd.read_csv('data/cleaned_supply_demand_by_charger_type.csv')

# Basic cleaning for visualization
data = data.dropna(subset=['charger_count', 'EV_Sales_Quantity'])
data = data[data['charger_count'] > 0]

# ---------- Visualization 1 ----------
# Total Charger Counts by Charger Type Name
plt.figure(figsize=(12, 6))
charger_counts = (
    data.groupby('charger_type_name')['charger_count']
    .sum()
    .reset_index()
    .sort_values('charger_count', ascending=False)
)
sns.barplot(data=charger_counts, x='charger_type_name', y='charger_count', palette='viridis')
plt.title('Total Charging Stations by Charger Type')
plt.xlabel('Charger Type')
plt.ylabel('Total Chargers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ---------- Visualization 2 ----------
# Total EV Sales Demand by Charger Type (Approximate)
plt.figure(figsize=(12, 6))
ev_sales = (
    data.groupby('charger_type_name')['EV_Sales_Quantity']
    .sum()
    .reset_index()
    .sort_values('EV_Sales_Quantity', ascending=False)
)
sns.barplot(data=ev_sales, x='charger_type_name', y='EV_Sales_Quantity', palette='magma')
plt.title('Total EV Sales Demand by Charger Type (Approximate)')
plt.xlabel('Charger Type')
plt.ylabel('Total EV Sales')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ---------- Visualization 3 ----------
# Scatter plot of Charger Supply vs EV Demand by Charger Type
plt.figure(figsize=(14, 8))
sns.scatterplot(
    data=data,
    x='charger_count',
    y='EV_Sales_Quantity',
    hue='charger_type_name',
    palette='tab20',
    s=100,
    alpha=0.7
)
plt.title('Charger Supply vs EV Demand by Charger Type')
plt.xlabel('Number of Chargers')
plt.ylabel('EV Sales Quantity')
plt.legend(title='Charger Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
