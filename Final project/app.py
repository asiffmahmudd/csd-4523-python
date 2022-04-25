# Name: Asif Mahmud
# ID: C0837117

#************** PLEASE READ ************#
# run the data_generator.py file first
# then run app.py file

#importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# setting the style of the graph for a better interface which is available in the package
plt.style.use('fivethirtyeight')

# this method is called everytime there's a data change in the source file with an interval of 100 ms
def animate(i):
    data = pd.read_csv('data.csv') # getting the data from the csv file in the same directory
    x = data['year'] # data of years for the x axis
    y = data['inflation'] # data of inflation rate for y axis

    inflation_list = y.tolist() # converting the inflation data to a list
    years_list = x.tolist() # converting the years data to a list
    len_years = len(years_list) # getting teh length of the years list

    # these are the two variables for showing minimum and maximum value of the inflation rate in the graph
    min_val = 0 # setting minimum value to 0
    max_val = 0 # setting maximum value to 0

    # these two are used to show 30 data on the graph at a time
    max_year = 1900 # setting the default value
    min_year = 1900 # setting the default value

    # condition for checking the maximum year and then resetting it to the beginning value
    if(max_year == 2022):
        max_year = 1900 # setting the year to the beginning value
        plt.clf() # this function is used to clear the current figure so that the next read can plot a new figure without any overlap

    # checking if the list exists
    if(inflation_list):
        min_val = min(inflation_list) # getting the minimum value of inflation rate
        max_val = max(inflation_list) # getting the maximum value of the inflation rate
        max_year = years_list[len_years-1] # getting the maximum year in the data source till now

    # setting the minimum year to show for plotting 30 data at a time
    if(max_year > 1930):
        min_year = max_year - 30 # setting minimum year

    

    plt.cla() # this function clears an axes which is currently active in the current figure
    # setting the title of the figure
    plt.title('Inflation history')
    plt.xlabel('Year') # label for x axis
    plt.ylabel('Inflation rate (Max rate: ' + str(max_val) + ' Min rate: ' + str(min_val) + ")") # label for y axis and also showing the maximum and minimum inflation rate here
    plt.xlim([min_year, max_year]) # limiting the value for x axis to show 30 data at a time
    plt.plot(x, y) # plotting the data

# plt.gcf() - Gets the current figure. If no current figure exists, a new one is created using figure().
# FuncAnimation - Makes an animation by repeatedly calling a function func. In this case the animate function
# the interval is set to 100 ms so that the animate function will be called with a 400 ms interval
ani = FuncAnimation(plt.gcf(), animate, interval=400) 

plt.tight_layout() # this function is for adjusting the padding between and around subplots for a better view                             
plt.show() # showing the graph to the user