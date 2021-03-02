# OPEN GUI

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import os.path
import sys
import csv
import threading

# multiprocessing
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import json
import requests


# Constant variables

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

selected_states = {
    "Alaska": "ak",
    "Arizona": "az",
    "California": "ca",
    "Colorado": "co",
    "Hawaii": "hi",
    "Idaho": "id",
    "Montana": "mt",
    "New Mexico": "nm",
    "Nevada": "nv",
    "Oregon": "or",
    "Utah": "ut",
    "Washington": "wa",
    "Wyoming": "wy"
}

# PART 1: Class to set up GUI VIEW


class GUI_view:
    def set_title(self):
        global window
        window = tk.Tk()
        window.title("Person Generator")
        # Set app title
        title = tk.Label(
            text="Welcome to Person Generator!",
            foreground="white",
            background="black")
        title.pack()

    def set_frames(self):
        # Divide the window into three sections
        global frame1
        frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
        frame1.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        global frame2
        frame2 = tk.Frame(master=window, width=100, height=100, bg="yellow")
        frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        global frame3
        frame3 = tk.Frame(master=window, width=100, height=100)
        frame3.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def set_frame1_dropdown(self):
        # Frame 1: dropdown menu for state selection
        dropdown_label = tk.Label(
            frame1, text="Step1: Select the state from the dropdown menu below:")
        dropdown_label.pack()
        global clicked
        clicked = tk.StringVar()
        clicked.set(states[0])
        print(selected_state)
        drop = tk.OptionMenu(frame1, clicked, *states, command=selected_state)
        drop.pack(pady=20)

    def set_frame1_num_entry(self):
        # Frame 1: Enter the number of addresses needed
        entry_label = tk.Label(
            frame1, text="Step 2: Enter the number of addresses you want to have:")
        entry_label.pack()
        global ent_num
        ent_num = tk.Entry(frame1)
        ent_num.pack(pady=20)

    def set_frame1_num_verify(self):

        # Show result: show user's num input.
        num_answer = tk.Label(frame1, text="")
        num_answer.pack(pady=20)

        # Add a submit button to verify input
        submit_button = tk.Button(
            frame1, text="Submit", command=lambda: verify_num(num_answer))
        submit_button.pack(pady=5)

        # Show Result: show user's state input in the text aera.
        input_label = tk.Label(frame1, text="Your selected state is:")
        input_label.pack()

    def set_frame3_output(self):
        # Frame 3: output area, use rolledtext
        output_label = tk.Label(
            frame3, text="Here are the results. Max displayed rows: 500. Export to see more rows).")
        output_label.pack()
        global text_area
        text_area = scrolledtext.ScrolledText(frame3, height=30)
        text_area.pack()

    def set_output_display(self):
        # set max displayed rows to 500
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 10)

    def set_frame2_button1(self):
        # Button 1: Click to generate results
        generate_button = tk.Button(
            frame2,
            text="Generate Results Now!",
            width=20,
            height=5,
            bg="white",
            fg="blue",
            command=lambda: generate_results(text_area)
        )
        generate_button.grid(row=0, column=0, sticky="nsew")

    def set_frame2_button2(self):
        # Button 2: click to export results to csv with designated headers
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

    def set_frame2_button3(self):
        # Button 3: click to clear and restart
        clear_button = tk.Button(
            frame2,
            text="Clear and Restart",
            width=20,
            height=5,
            bg="white",
            fg="red",
            command=lambda: clear_input(text_area)
        )
        clear_button.grid(row=0, column=2, sticky="nsew")

    def set_frame2_button4(self):
        # Button 4: request data from population generator
        request_button = tk.Button(
            frame2,
            text="Request Data from others",
            width=20,
            height=5,
            bg="white",
            fg="blue",
            command=wait_for_results
        )
        request_button.grid(row=1, column=1, sticky="nsew")


# PART 2: All events for elements on GUI:

# PART 2.1:

# Event for dropdown menu in frame 1
def selected_state(event):
    global selected_state
    selected_state = clicked.get()
    print(selected_state)

# Event for submit button to verify inputs in frame1


def verify_num(verify_area):
    try:
        int(ent_num.get())
        verify_area.config(
            text="You entered a number. Please select a state now.")
    except ValueError:
        verify_area.config(
            text="You did not enter a number. Please enter a number.")
    # show text of the state input
    my_state = tk.Label(frame1, text=clicked.get())
    my_state.pack()


# PART 2.2
# Event for generating result button 1 in frame 2
# PART 2.2-0: find correct csv file to read

def read_csv():
    # read csv file
    for state in selected_states:
        csv_file = selected_states[state] + ".csv"
    return csv_file

# PART 2.2-1 Communication with population generator
# To receive output from the population generator
# Get population number from Population generator


def wait_for_results():
    """Connect to the Client as a listener and wait for the number (1% of the population) to be sent"""
    listener = Listener(('localhost', 6000), authkey=b'success')
    receiving = True
    while receiving:
        conn = listener.accept()
        while True:
            msg = conn.recv()
            if msg == 'close':
                send_results(conn)
                conn.close()
                listener.close()
                receiving = False
                break
            else:
                global returned_data
                returned_data = str(msg)
                print(returned_data)
                # simply print out returned data in text area.
                text_area.insert(
                    "1.0", "Data from Population Generator is:" + returned_data)


def async_wait_call():
    wait_thread = threading.Thread(
        target=wait_for_results, name="Await", args=[])
    wait_thread.start()

# PART 2.2-2 FUNCTIONS TO GENERATE RESULTS:


def generate_results(text_area):
    state = clicked.get()
    num = int(ent_num.get())
    global formatted_data
    formatted_data = format_data(merge_data(randomize_data(num), state, num))
    global sent_data
    sent_data = csv_to_json(formatted_data)
    # insert data to display area
    text_area.insert("1.0", formatted_data)

# 1) Randomly select data from the given csv.


def randomize_data(num):
    """Randomly select data"""
    selected_num = num
    usecols = ['NUMBER', 'STREET', 'UNIT', 'CITY', 'POSTCODE']
    csv_file = read_csv()
    data = pd.read_csv(csv_file, usecols=usecols)
    selected_data = data.sample(selected_num)
    return selected_data

# 2) Merge data into required output.


def merge_data(data, state, num):
    """Merge data"""
    merged_data = data.assign(
        input_state=state,
        input_number_to_generate=num,
        output_content_type="street address",
        output_content_value=data.NUMBER.astype(str) + ' ' +
        data.STREET.astype(str) + ', ' +
        data.UNIT.astype(str) + ', ' +
        data.CITY.astype(str) + ', ' +
        state + ' ' +
        data.POSTCODE.astype(str)
    )
    return merged_data

# 3) Format data into required csv format.


def format_data(data):
    """Format data into required csv format."""
    # remove previously column
    removed_cols = ['NUMBER', 'STREET', 'UNIT', 'CITY', 'POSTCODE']
    data.drop(removed_cols, inplace=True, axis=1)
    # drop index number
    data.reset_index(drop=True, inplace=True)
    return data

# 4) Convert data into json file for sending to other's app.


def csv_to_json(csv):
    """convert merged_data to json file for sending to population generator."""
    parsed = json.loads(csv.to_json(orient="index"))
    json_data = json.dumps(parsed, indent=4)
    return json_data

# 5) convert to csv file


def export_results():
    # create a new output csv file with new headers
    formatted_data.to_csv("output.csv", index=False)
    # message to allow users to know the file is ready.
    file_exists = os.path.exists('output.csv')
    if file_exists == True:
        messagebox.showinfo(
            "CSV File Ready", "Congrats! Your CSV file is now in the same directory as the program.")

# PART 2.3: Event for button 3 to clear text input in frame 2


def clear_input(text_area):
    ent_num.delete(0, 'end')  # clear number entry box
    text_area.delete("1.0", "end")  # clear output result text box

# PART 2.4: Send data to population generator
# Send json results to population generator


def send_results(connect):
    # Connect to the Person Generator:
    if connect:
        # sent_data is the merged data converted into json file.
        connect.send(sent_data)
        connect.send('close')
    else:
        print("Error occurred while connecting to Population Generator.")


# PART 4: NO-GUI MODE: Command line app to read input.csv and export output.csv


# Functions for command line mode

def auto_open_csv():
    # open input.csv
    inputFile = open(sys.argv[1], 'rb')
    # outputFile = open(sys.argv[2], 'wb')
    df = pd.read_csv(inputFile)
    print("Importing input.csv")
    # get values of input state and numbers from input.csv
    global state
    state = df['input_state'][0]
    global num
    num = df['input_number_to_generate'][0]
    # get correct csv
    read_csv()


def generate_csv_results():
    print("Randomly selecting data...")
    selected_data = randomize_data(num)
    global merged_data
    merged_data = merge_data(selected_data, state, num)
    formatted_data = format_data(merged_data)
    print(formatted_data)
    print("Finished selecting data.")
    formatted_data.to_csv("output.csv", index=False)
    print("Your CSV file is ready in the same directory as program.")


def mode_switch():
    """Check to see if there is an input file"""
    if len(sys.argv) > 1:
        # Read CSV file and process it:
        auto_open_csv()
        generate_csv_results()
    else:
        """If no input file, create GUI"""
        view = GUI_view()
        view.set_title()
        view.set_frames()
        view.set_frame1_dropdown()
        view.set_frame1_num_entry()
        view.set_frame1_num_verify()
        view.set_frame3_output()
        view.set_output_display()
        view.set_frame2_button1()
        view.set_frame2_button2()
        view.set_frame2_button3()
        view.set_frame2_button4()
        async_wait_call()
        # Run  the event loop
        window.mainloop()
    exit()


if __name__ == '__main__':

    mode_switch()
