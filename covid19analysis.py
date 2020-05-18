from math import ceil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')

df['new_cases'] = df['cases'].diff()
df['rolling_avg_week'] = df['new_cases'].rolling(7).mean()

df.dropna(inplace=True)

df = df[df['date'] >= '2020-03-01'].reset_index()
df.drop('index', axis=1, inplace=True)

print(df.head())

plt.figure(figsize=(20, 10))
plt.bar(df.date, df['new_cases'], color='salmon')
ax = plt.gca()
plt.xticks(rotation=45)
for i, label in enumerate(ax.get_xaxis().get_ticklabels()):
    if i % 7 != 0:
        label.set_visible(False)

sns.regplot(x=df.index, y='rolling_avg_week', data=df, order=16, ci=None, color='red')

plt.title('US COVID-19 New Cases By Day')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.show()

last_week = df.tail(7)['rolling_avg_week']
m = (last_week.iloc[6] - last_week.iloc[0]) / 6
b = last_week.iloc[6]

five_thousand = ceil((5000 - b) / m)
print('Based on current weekly trends, it would take ' + str(
    five_thousand) + ' days until the average number of new daily cases in the'
                     ' US is at 5000 or less.')

five_hundred = ceil((500 - b) / m)
print('Based on current weekly trends, it would take ' + str(
    five_hundred) + ' days until the average number of new daily cases in the'
                    ' US is at 500 or less.')

print('Disclaimer: This program is not designed nor intended to offer a prediction for when the COVID-19 crisis would '
      'subside. It is merely intended to highlight the current trends in the number of new cases.')

print('All data used is from The New York Times COVID-19 database.')
