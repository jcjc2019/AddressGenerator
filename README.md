# Address Generator

## Overview

An address generator that randomly selects and generates a given number of addresses from one of the 13 US state in the West. All data comes from [https://www.kaggle.com/openaddresses/openaddresses-us-west](https://www.kaggle.com/openaddresses/openaddresses-us-west). This is a desktop app made via Python and Tkinter.

## Current Features

- Generate a given number of random addresses.
- Export the results to CSV files.

## Build with

- [Python 3](https://www.python.org/downloads/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pandas](https://pandas.pydata.org/)
- All data files in this repo come from [https://www.kaggle.com/openaddresses/openaddresses-us-west](https://www.kaggle.com/openaddresses/openaddresses-us-west).

## To start the app locally

- Step 1: `git clone` the repo to your local machine.
- Step 2: enter `python person-generator.py` to open up the python GUI interface. You can also enter `python person-generator.py input.csv` to automatically create an `output.csv` without working with the GUI (just close the GUI to get the `output.csv` file for the given input file). (The current `input.csv` in the repo is set to randomly choose 10 addresses from Alaska.)
- Step 3: choose state and number of addresses you need. Click `Submit` to validate your input. When you are ready, click `Generate Results Now!` to generate a list of addresses that will be shown in the textbox. Then you can click `Export Results to CSV` to get a .CSV file with the results.
- Step 4: To restart the above step, click `Clear and Restart` to select a new state and enter a new number of addresses you want.

## Video Demo

- Click [here ](https://www.youtube.com/watch?v=Tca-zadEUzE)to check out the video demo.
