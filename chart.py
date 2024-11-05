import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the external file
data = pd.read_csv('fdata.csv')

# Aggregate the data based on country
country_counts = data['Country'].value_counts()
top_countries = country_counts.head(10)
other_countries_count = country_counts[10:].sum()
top_countries['Others'] = other_countries_count

# Plotting a pie chart
plt.figure(figsize=(10, 7))
plt.pie(top_countries, labels=top_countries.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  
plt.title('Distribution of Customers by Country')
plt.show()