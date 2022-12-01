# Rides App

```
USAGE:
python rides.py <--friday | --sunday> <--clear | --no-clear> [[FLAG] ...]

FLAG
    --help                Shows usage
    --debug               Prints out debug statements while running
    --no-fetch            Prevents new sheet data from being fetched
    --no-update           Prevents the output sheet from being updated
    --rotate              Previous assignments are cleared and drivers are rotated based on date last driven
    --edit                Previous assignments are retained and new assignments are appended
    --friday              Assigns rides for Friday College Life
    --sunday              Assigns rides for Sunday service
    --threshold=<num>     Sets how many open spots a driver must have to spontaneously pick up at a neighboring location. The default is 2.
```

[Specification Document](https://docs.google.com/document/d/1Ube_m7H2BMxwY900dqZHqWQX3rRoPFq41DLoNI-5r6w/edit?usp=sharing)

## Setup
To install the required dependencies, run
```bash
pip install -r requirements.txt
```
To run the file, you need the API key. Contact me (Eric Pham) directly for it.

## Configurations
In the `cfg` directory, you will find the file `map.txt`.
Additionally, you can add `ignore_drivers.txt` and/or `ignore_riders.txt` to the `cfg` directory.

### ignore_drivers.txt and ignore_riders.txt
Add the phone numbers of the people you want to exclude in the next run of the program, separated by `\n`, or **ENTER**.

### map.txt
This tells the program how different pickup locations are situated around each other.
The syntax is as follows.
- `<loc>` : Every location must match how it is used in the Google Forms
  - `Revelle` is accepted, `revelle` is not.
- `#` : Lines starting with `#` are ignored as comments.
- `,` : Locations separated by `,` are considered to be in the same area.
- `\n` or **ENTER** : The number of **ENTER**s denotes how far apart two areas are.
- `ELSEWHERE` : Represents locations not hardcoded into the script. Used for handling exact addresses and unknown locations.
