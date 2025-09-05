import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

final_df = pd.read_csv('data/ev_analysis_combined.csv')


print(final_df.head())  # Quick preview to confirm successful load

#Charging Stations Count by State
plt.figure(figsize=(12,6))
sns.barplot(data=final_df.sort_values('stations_count', ascending=False), x='state', y='stations_count')
plt.xticks(rotation=90)
plt.title('Charging Stations Count by State')
plt.xlabel('State')
plt.ylabel('Number of Charging Stations')
plt.tight_layout()
plt.show()

#Bar Chart for EV Sales by State
plt.figure(figsize=(12,6))
sns.barplot(data=final_df.sort_values('EV_Sales_Quantity', ascending=False), x='state', y='EV_Sales_Quantity')
plt.xticks(rotation=90)
plt.title('EV Sales by State')
plt.xlabel('State')
plt.ylabel('Number of EV Sales')
plt.tight_layout()
plt.show()

# Scatter Plot of Per Capita Metrics
plt.figure(figsize=(10,6))
sns.scatterplot(data=final_df, x='stations_per_capita', y='sales_per_capita', hue='state')
plt.title('EV Sales Per Capita vs Charging Stations Per Capita by State')
plt.xlabel('Charging Stations Per Capita')
plt.ylabel('EV Sales Per Capita')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.tight_layout()
plt.show()

#Trendline to Scatter Plot
plt.figure(figsize=(12, 7))
# First, plot the colored scatterplot
ax = sns.scatterplot(
    data=final_df,
    x='stations_per_capita',
    y='sales_per_capita',
    hue='state',
    s=80,
    palette='tab20'
)

# Then, overlay the trend line (regression line) on the same axes
sns.regplot(
    data=final_df,
    x='stations_per_capita',
    y='sales_per_capita',
    scatter=False,
    ax=ax,
    color='black',   # Trendline color for visibility
    line_kws={'linewidth':2}
)

plt.title('EV Sales Per Capita vs Charging Stations Per Capita by State (with Trendline)')
plt.xlabel('Charging Stations Per Capita')
plt.ylabel('EV Sales Per Capita')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='State')

# Annotate each point with abbreviated state code
for i, row in final_df.iterrows():
    ax.text(row['stations_per_capita'], row['sales_per_capita'], row['state'][:3].upper(), fontsize=7)

plt.tight_layout()
plt.show()