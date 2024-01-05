# Rides App

## Background
Previously, the Rides Coordinator would manually parse through these spreadsheets to organize riders into cars.
This is a very time-consuming process that takes about 30-40 minutes every time rides needed to be coordinated.
The completion of this script will save over an hour each week for the Rides Coordinator.

## Objective
Develop a Python script that turns Permanent and Weekly Rides Form outputs into a formatted Google Sheets spreadsheet for drivers.
It will automatically assign riders to drivers every single week with the execution of a Python file.

[Specification Document](https://docs.google.com/document/d/1Ube_m7H2BMxwY900dqZHqWQX3rRoPFq41DLoNI-5r6w/edit?usp=sharing)

[Service Account Setup Tutorial](https://denisluiz.medium.com/python-with-google-sheets-service-account-step-by-step-8f74c26ed28e)

```
usage: rides.py [-h] --day {friday,sunday} [--download | --no-download] [--upload | --no-upload] [--rotate] [--distance {1,2,3,4,5,6,7,8,9}]
                [--vacancy {1,2,3,4,5,6,7,8,9}] [--log {debug,info,warning,error,critical}]

options:
  -h, --help            show this help message and exit
  --day {friday,sunday}
                        choose either 'friday' for CL, or 'sunday' for church
  --download, --no-download
                        choose whether to download Google Sheets data (default: True)
  --upload, --no-upload
                        choose whether to upload output to Google Sheets (default: True)
  --rotate              previous assignments are cleared and drivers are rotated based on date last driven
  --distance {1,2,3,4,5,6,7,8,9}
                        set how many far a driver can be to pick up at a neighboring location before choosing a last resort driver
  --vacancy {1,2,3,4,5,6,7,8,9}
                        set how many open spots a driver must have to pick up at a neighboring location before choosing a last resort driver
  --log {debug,info,warning,error,critical}
                        set a level of verbosity for logging
```

## Setup
To install the required dependencies, run
```bash
pip install -r requirements.txt
```
To run the file, you need the API key in the form of a `service_account.json` file. Contact Eric Pham directly for it.
You will need to place the `service_account.json` file in the `cfg` directory.

## Configurations
In the `cfg` directory, you will find the file `map.txt`.
Additionally, you can add `ignore_drivers.txt` and/or `ignore_riders.txt` to the `cfg` directory.

### ignore_drivers.txt and ignore_riders.txt
Add the phone numbers of the people you want to exclude in the next run of the program, separated by `\n`, or **ENTER**.

### map.txt
This file tells the program how different pickup locations are situated around each other.
The following is an example file for the UCSD campus.
It simulates a path that goes from the southwest side of campus to the east.
```
ELSEWHERE
# West campus
Revelle
Muir
Sixth
Marshall
ERC
Seventh
# East campus
Warren, Pepper Canyon Apts
Rita Atkinson
ELSEWHERE
```
The syntax is as follows.
- `<loc>` : Every location must match how it is used in the Google Forms
  - `Revelle` is accepted, `revelle` is not.
- `#` : Lines starting with `#` are ignored as comments.
- `,` : Locations separated by `,` are considered to be in the same area.
- `\n` or **ENTER** : The number of **ENTER**s denotes how far apart two areas are.
- `ELSEWHERE` : Represents locations not hardcoded into the script. Used for handling exact addresses and unknown locations.
