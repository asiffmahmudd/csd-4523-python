import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['year']
    y = data['inflation']

    arr = y.tolist()
    years = x.tolist()
    len_years = len(years)

    min_val = 0
    max_val = 0

    max_year = 1900
    if(max_year == 1940):
        max_year = 1900
        plt.clf()

    if(arr):
        min_val = min(arr)
        max_val = max(arr)
        max_year = years[len_years-1]

    min_year = 1900
    if(max_year > 1930):
        min_year = max_year - 30

    

    plt.cla()
    plt.title('Inflation history' ' (Max rate: ' + str(max_val) + ' Min rate: ' + str(min_val) + ")")
    plt.xlabel('Year')
    plt.ylabel('Inflation rate')
    plt.xlim([min_year, max_year])
    plt.plot(x, y)


ani = FuncAnimation(plt.gcf(), animate, interval=500)

plt.tight_layout()                              
plt.show()