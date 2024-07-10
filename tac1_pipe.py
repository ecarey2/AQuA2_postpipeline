import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import glob
import os


##### Step 1: Getting user input to set up conversions and excel file imports #######

# Get user input for phone or behavior camera used to set conversion rate
user_input = input("Please enter behavior or phone to indicate which type of camera was used for behavior recording: ")
print("You entered: ", user_input)

if user_input == 'phone':
    conversion = 29.77

else:
    conversion = 17.39


'''select_excel_file function: This function gets user input for the file path 
and name of behavior sheet to load in'''
def select_excel_file():
    # Create the main application window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to select an Excel file
    file_path = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=(("Excel files", "*.xlsx *.xls"), ("All files", "*.*"))
    )
    
    if file_path:
        print("Selected file:", file_path)
        return file_path
    else:
        print("No file selected.")
        return None

# Call the function to open the file selection dialog and get the file path
file_path = select_excel_file()

if file_path:
    # Read the selected Excel file into a pandas DataFrame
    xls = pd.ExcelFile(file_path)
    print("Dataframe loaded successfully.")
    
else:
    print("No Excel file to load.")


# separate excel sheets into different data frames by getting user input
#***** MODIFY HERE: for different animals change 'TGP#1_before' to correct name of sheet wanting to analyze

def select_sheets():
    sheet = input('Enter first Excel sheet to analyze, be sure spelling is correct: ')
    return sheet


def more_input():
    user_input = input('Analyze other sheets (Enter y or n)?: ')
    if user_input == 'y':
       sheet = input('Enter next Excel sheet name to analyze:') 
    else:
        sheet = 'No additional sheet'
    return sheet

    

### Getting user input to load in more excel sheets to analyze
sheet1 = select_sheets()
sheet2 = more_input()

if sheet2 == 'No additional sheet':
    print('No additional sheets were loaded')
else:
    sheet3 = more_input()


df1 = pd.read_excel(xls, sheet1)
#renaming the first row in each sheet as the column names
df1.columns = df1.iloc[0]
df1 = df1[1:]

if sheet2 != 'No additional sheet':
    df2 = pd.read_excel(xls, sheet2)
    df2.columns = df2.iloc[0]
    df2 = df2[1:]


if sheet2 != 'No additional sheet':
    
    df3= pd.read_excel(xls, sheet3)
    df3.columns = df3.iloc[0]
    df3 = df3[1:]


print(df1.head(2))

# *******Step 2: reading in the csv files of events detected by AQuA2 to plot *******

#will have to define manually or have user input how many trials
#make sure folders set up like "data1, data2 ...., data28

#get user input for number of trials
def data_input():
    user_input = input('Enter number of trials to analyze: ')
    trials = user_input
    return trials

trials_number = int(data_input())

for i in range(trials_number):
    folders = []

    folders.append(f'/Users/erincarey/Documents/bphon/traces/data{i+1}')
    #folder_path2 = f'/Users/erincarey/Documents/bphon/traces/data'


######### 6-4-24 work on reading in all plots and correlating to behavior then saving along with picture rep of event from AQUA2 video

''' excel_loop function Loops through all the event excel sheets and saves df/f plots correlated to behavior'''

def excel_loop(traces_folder):
    #for i, data in enumerate(csv_files):
        # Initialize an empty list to store DataFrames
    data_frames = []

    csv_files = [f for f in os.listdir(traces_folder) if f.endswith('.csv')]

    if 'data1' in traces_folder:
        title =1
    else:
        title =2

        # Loop through the list of CSV files and read each into a DataFrame
    for file in csv_files:
        file_path = os.path.join(traces_folder, file)
        df = pd.read_csv(file_path)
        data_frames.append(df)
    
    for i, data in enumerate(data_frames):
        x= sns.lineplot(data= data[['dff']], dashes = False)

        ####### work on this not outputting to correct data 

        x.set(xlabel ="Frame", ylabel = "dF/F", title =f'Brush Event {i+1}')
        line = df1['Onset'].iloc[0]

        #print(line)
        x.axvline(x=line, color="black", linestyle="--") # figure out how to plot the behavior onset
        plt.legend(loc='upper left')
        plt.ylim(-.05,.1)

         # Save the plot
        
        plot_file_path = os.path.join(traces_folder, f'Data{title} dff_plot_Event{i+1}.png')
        plt.savefig(plot_file_path)
        plt.close()

for i in range(len(folders)):
    excel_loop(folders[i])
#excel_loop(folder_path2)


''' Goes through AQuA2 video to find frame of movie correlated to df/f curve and plots next to trace'''


'''x= sns.lineplot(data= data_frames[0][['dff']], dashes = False)
x.set(xlabel ="Frame", ylabel = "dF/F", title ='Brush Data 1')
x.axvline(x=499, color="black", linestyle="--")
plt.legend(loc='upper left')
plt.show()'''

#work on getting event outlined traced
# save plots 

#### Filtering step for what events to exclude or analyze all 

## Group left and right sides 