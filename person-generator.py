# OPEN GUI

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import os.path
import sys
import csv

# multiprocessing
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import json
import requests

# Set GUI interface
window = tk.Tk()
window.title("Person Generator")
# Set app title
title = tk.Label(
    text="Welcome to Person Generator!",
    foreground="white",
    background="black")
title.pack()

# Divide the window into three sections
frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
frame1.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

frame2 = tk.Frame(master=window, width=100, height=100, bg="yellow")
frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

frame3 = tk.Frame(master=window, width=100, height=100)
frame3.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

# Frame 1: dropdown menu for state selection
dropdown_label = tk.Label(
    frame1, text="Step1: Select the state from the dropdown menu below:")
dropdown_label.pack()


def selected_state(event):
    selected_state = clicked.get()
    print(selected_state)

states = [
    "Alaska",
    "Arizona",
    "California",
    "Colorado",
    "Hawaii",
    "Idaho",
    "Montana",
    "New Mexico",
    "Nevada",
    "Oregon",
    "Utah",
    "Washington",
    "Wyoming"
]

clicked = tk.StringVar()
clicked.set(states[0])
drop = tk.OptionMenu(frame1, clicked, *states, command=selected_state)
drop.pack(pady=20)

# Frame 1: Enter the number of addresses needed
entry_label = tk.Label(
    frame1, text="Step 2: Enter the number of addresses you want to have:")
entry_label.pack()


ent_num = tk.Entry(frame1)
ent_num.pack(pady=20)

def number():
    try:
        int(ent_num.get())
        num_answer.config(
            text="You entered a number. Please select a state now.")
    except ValueError:
        num_answer.config(
            text="You did not enter a number. Please enter a number.")
    # show text of the state input
    my_state = tk.Label(frame1, text=clicked.get())
    my_state.pack()


submit_button = tk.Button(frame1, text="Submit", command=number)
submit_button.pack(pady=5)
num_answer = tk.Label(frame1, text="")
num_answer.pack(pady=20)

# Result: show user's state input
input_label = tk.Label(frame1, text="Your selected state is:")
input_label.pack()


# Frame 2: buttons for generate results, export results, clear input
# button 1: generate result

# event for generating result button

def read_csv():
    # get user input
    selected_state = clicked.get()
    # read csv file
    if selected_state == "Alaska":
        # open ak csv
        csv_file = "ak.csv"
    elif selected_state == "Arizona":
        # open az csv
        csv_file = "az.csv"
    elif selected_state == "California":
        # open ca csv
        csv_file = "ca.csv"
    elif selected_state == "Colorado":
        # open co csv
        csv_file = "co.csv"
    elif selected_state == "Hawaii":
        # open hi csv
        csv_file = "hi.csv"
    elif selected_state == "Idaho":
        # open id csv
        csv_file = "id.csv"
    elif selected_state == "Montana":
        # open mt csv
        csv_file = "mt.csv"
    elif selected_state == "Nex Mexico":
        # open nm csv
        csv_file = "nm.csv"
    elif selected_state == "Nevada":
        # open nv csv
        csv_file = "nv.csv"
    elif selected_state == "Oregon":
        # open or csv
        csv_file = "or.csv"
    elif selected_state == "Utah":
        # open ut csv
        csv_file = "ut.csv"
    elif selected_state == "Washington":
        # open wa csv
        csv_file = "wa.csv"
    elif selected_state == "Wyoming":
        # open wy csv
        csv_file = "wy.csv"
    return csv_file


csv_file = read_csv()


#Get a number from Population generator as the input number

def wait_for_number():
    """Connect to the Client as a listener and wait for the number (1% of the population) to be sent"""
    listener = Listener(('localhost', 6000), authkey=b'success')
    receiving = True
    while receiving:
        conn = listener.accept()
        while True:
            msg = conn.recv()
            if msg == 'close':
                conn.close()
                receiving = False
                break
            else:
                global returned_data
                returned_data = int(msg)
                print(returned_data)
    listener.close()


def generate_results():
    selected_num = int(ent_num.get())
    data = pd.read_csv(csv_file, usecols=['NUMBER',
                                          'STREET',
                                          'UNIT',
                                          'CITY',
                                          'POSTCODE'])
    selected_data = data.sample(selected_num)
    global merged_data
    merged_data = selected_data.assign(
        input_state=clicked.get(),
        input_number_to_generate=int(ent_num.get()),
        output_content_type="street address",
        output_content_value=selected_data.NUMBER.astype(str) + ' ' +
        selected_data.STREET.astype(str) + ', ' +
        selected_data.UNIT.astype(str) + ', ' +
        selected_data.CITY.astype(str) + ', ' +
        clicked.get() + ' ' +
        selected_data.POSTCODE.astype(str)
    )
    # remove previously column
    merged_data.drop(['NUMBER',
                      'STREET',
                      'UNIT',
                      'CITY',
                      'POSTCODE'],
                     inplace=True, axis=1)
    # TO BE FIXED: remove nan from each address
    # drop index number
    merged_data.reset_index(drop=True, inplace=True)
    print(merged_data)
    text_area.insert("1.0", merged_data)
    return merged_data


generate_button = tk.Button(
    frame2,
    text="Generate Results Now!",
    width=20,
    height=5,
    bg="white",
    fg="blue",
    command=generate_results
)
generate_button.grid(row=0, column=0, sticky="nsew")


# button 2: export results to csv with designated headers

def export_results():
    # create a new output csv file with new headers
    merged_data.to_csv("output.csv", index=False)
    # message to allow users to know the file is ready.
    file_exists = os.path.exists('output.csv')
    if file_exists == True:
        messagebox.showinfo(
            "CSV File Ready", "Congrats! Your CSV file is now in the same directory as the program.")


export_button = tk.Button(
    frame2,
    text="Export Result to CSV",
    width=20,
    height=5,
    bg="white",
    fg="green",
    command=export_results
)
export_button.grid(row=0, column=1, sticky="nsew")


# button 3: clear input button
def clearInput():
    ent_num.delete(0, 'end')  # clear number entry box
    text_area.delete("1.0", "end")  # clear output result text box


clear_button = tk.Button(
    frame2,
    text="Clear and Restart",
    width=20,
    height=5,
    bg="white",
    fg="red",
    command=clearInput
)
clear_button.grid(row=0, column=2, sticky="nsew")

# Frame 3: output area, use rolledtext
output_label = tk.Label(
    frame3, text="Here are the results. Max displayed rows: 500. Export to see more rows).")
output_label.pack()

text_area = scrolledtext.ScrolledText(frame3, height=30)
text_area.pack()

# set max displayed rows to 500
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 10)

# Run  the event loop
window.mainloop()

# Command line app to read input and export output

class auto_open_csv:
    def auto_open_csv(self):
        # open input.csv
        inputFile = open(sys.argv[1], 'rb')
        # outputFile = open(sys.argv[2], 'wb')
        df = pd.read_csv(inputFile)
        print("Import input.csv")
        # get values of input state and numbers from input.csv
        state = df['input_state'][0]
        num = df['input_number_to_generate'][0]
        global correct_csv
        if state == "Alaska":
            # open ak csv
            correct_csv = "ak.csv"
        elif state == "Arizona":
            # open az csv
            correct_csv = "az.csv"
        elif state == "California":
            # open ca csv
            correct_csv = "ca.csv"
        elif state == "Colorado":
            # open co csv
            correct_csv = "co.csv"
        elif state == "Hawaii":
            # open hi csv
            correct_csv = "hi.csv"
        elif state == "Idaho":
            # open id csv
            correct_csv = "id.csv"
        elif state == "Montana":
            # open mt csv
            correct_csv = "mt.csv"
        elif state == "Nex Mexico":
            # open nm csv
            correct_csv = "nm.csv"
        elif state == "Nevada":
            # open nv csv
            correct_csv = "nv.csv"
        elif state == "Oregon":
            # open or csv
            correct_csv = "or.csv"
        elif state == "Utah":
            # open ut csv
            correct_csv = "ut.csv"
        elif state == "Washington":
            # open wa csv
            correct_csv = "wa.csv"
        elif state == "Wyoming":
            # open wy csv
            correct_csv = "wy.csv"
        results = pd.read_csv(correct_csv, usecols=['NUMBER',
                                                    'STREET',
                                                    'UNIT',
                                                    'CITY',
                                                    'POSTCODE'])
        print("Randomly selecting data...")
        # copy code from above generate function
        selected_data = results.sample(num)
        global auto_data
        auto_data = selected_data.assign(
            input_state=state,
            input_number_to_generate=num,
            output_content_type="street address",
            output_content_value=selected_data.NUMBER.astype(str) + ' ' +
            selected_data.STREET.astype(str) + ', ' +
            selected_data.UNIT.astype(str) + ', ' +
            selected_data.CITY.astype(str) + ', ' +
            clicked.get() + ' ' +
            selected_data.POSTCODE.astype(str)
        )
        # remove previously column
        auto_data.drop(['NUMBER',
                        'STREET',
                        'UNIT',
                        'CITY',
                        'POSTCODE'],
                       inplace=True, axis=1)
        # TO BE FIXED: remove nan from each address
        # drop index number
        auto_data.reset_index(drop=True, inplace=True)
        print(auto_data)
        print("Finished selecting data.")
        # copy from above export function
        outputFile = auto_data.to_csv("output.csv", index=False)
        # writer = csv.writer(outputFile)
        print("Your CSV file is ready in the same directory as program.")


obj = auto_open_csv()
obj.auto_open_csv()


# To send data to population generator
# convert csv data to json format
def csv_to_json(csvFilePath, jsonFilePath):
    # convert csv file to json
    jsonArray = []
    # get output csv
    with open(csvFilePath, encoding='utf-8') as csvfile:
        csvReader = csv.DictReader(csvfile)
    for row in merged_data:
        jsonArray.append(row)
    # convert json array to json string
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonfile:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonfile.write(jsonString)

# Send results to population generator
def send_results():
    csvFilePath = r'output.csv'
    jsonFilePath = r'output.json'
    # convert merged_data to json format
    json_data = csv_to_json(csvFilePath, jsonFilePath)
    print(json_data)
    # Connect to Population Generator:
    connect = Client(('localhost', 6000), authkey=b'success')
    if connect:
        connect.send(json_data)
        connect.send("close")
        connect.close()
        # Waiting for the Response
        wait_for_response()
    else:
        print("Error occurred while connecting to Population Generator.")

