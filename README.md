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
USAGE:
python rides.py <--friday | --sunday> [[FLAG] ...]

FLAG
    --friday              Assigns rides for Friday College Life
    --sunday              Assigns rides for Sunday service
    --rotate              Previous assignments are cleared and drivers are rotated based on date last driven
    --edit                Previous assignments are retained and new assignments are appended
    --no-fetch            Prevents new sheet data from being fetched
    --no-update           Prevents the output sheet from being updated
    --threshold=<num>     Sets how many open spots a driver must have to spontaneously pick up at a neighboring location. The default is 2.
    --help                Shows usage
    --debug               Prints out debug statements while running
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
