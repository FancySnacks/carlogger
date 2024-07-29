
# Carlogger

Track any work you perform on your car, keep a maintenance log, list of parts and schedule future repairs. 


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![Tests](https://github.com/FancySnacks/carlogger/actions/workflows/actions.yml/badge.svg)

## Features

- console interface as well GUI interface
- add multiple cars
- create entry logs based on maintenance you've done
- schedule future entry logs, one-time or repeating, with looping based on either time or mileage
- keep logs segregated in components and collections for tidy organization
- export data to json, text or csv file formats


## Installation

To use this module you have to download this repository locally on your machine.

### Prerequisites

```
Python >= 3.11  
customtkinter==5.2.2
pillow==10.4.0
```  
  
#### Optional (testing-only)

```
pytest>=7.3.1
pytest-cov>=4.0.0
```

To use this module, you'll need to have Python installed on your computer. You can download the latest version of Python from the [official Python website](https://www.python.org/downloads/).  

**`OPTIONAL:`** If you want to use and manage tests you also need a Pytest module, once/if you have Python installed on your computer, open up command line tool and type the following:  

```bash
pip install pytest
```

**`NOTE:`**  Make sure that you have PIP package manager installed on your device.  
  
  
### Repository Download

Once you have Python installed, you can clone this repository using the command:

```bash
git clone https://github.com/FancySnacks/carlogger
```
  
### Module Installation  
  
You can also download this module via PIP command:  
```bash
pip install https://github.com/FancySnacks/carlogger.git
```
## Usage/Examples

For help, type into the console

```bash
carlogger -h
```

Output:

```
usage: carlogger [-args]

Choose 'carlogger --gui' for visual interface.

positional arguments:
  {add,read,delete,update,import,export}
                        Subcommands
    add                 Add new car, collection, component or log entry.
    read                Return car info, collection/component list or log entries by specifying the car.
    delete              Delete specified car, collection, component or log entry.
    update              Update data of car, collection, component or entry.
    import              Import file and save as new item.
    export              Export item to file.

options:
  -h, --help            show this help message and exit
  --gui                 Open graphical user interface for this app.
  --printargs           Print parsed arguments to the console.

```
 
The program uses different modes for different actions:  

`add [car, collection, component, entry]` - add a new item to target parent (apart from car which is on top of the hierarchy)  
`delete [car, collection, component, entry]` - delete target item and it's directory
`read [car, collection, component, entry]` - print item info to the console  
`update [car, collection, component, entry]` - update item values  
`import [car, collection, component, entry]` - create new item from file
`export [car, collection, component, entry]` - export item to a file  

For GUI, enter  

```bash
carlogger --gui
```

Example usage:

```bash
carlogger add car --name CarTestPytest --manufacturer Skoda --model Roomster --year 2002 --mileage 198000
// creates new car and directory

carlogger add collection --name Engine --car CarTestPytest
// add new collection to target car, collections contain components or other collections

carlogger add collection --name "Turbocharger" --car CarTestPytest --parent Engine
// add nested/child collection to previously made collection

carlogger add collection --name "Intake" --car CarTestPytest --parent Turbocharger
// add nested/child collection to previously made collection

carlogger add component --name "Spark_Plug" --car CarTestPytest --collection Engine
/add component to target collection, components contain log entries

carlogger add component --name Airflow --car CarTestPytest --collection Turbocharger

carlogger add entry --car "CarTestPytest" --collection "Engine" --component "Spark_Plug" --desc "Replaced all spark plugs." --mileage 198000 --category "swap" --custom "part=Bosch Double Iridium"
// add new entry with custom info that mentions swapped part

carlogger add scheduled_entry --car CarTestPytest --collection Engine --component "Spark_Plug" --desc "Spark plug swap." --mileage 0 --category "swap" --rule 'mileage' --frequency 1200
//add a future log entry, scheduled by mileage, due in 1200 mil or km

carlogger add scheduled_entry --car CarTestPytest --collection Engine --component "Spark_Plug" --desc "Spark plug check." --mileage 0 --category "check" --repeating --rule 'date' --frequency 30
//add a scheduled log entry, scheduled by date, due in 30 days
```


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Running Tests

To run tests, run the following command while in main directory

```bash
  pytest ./tests
```


## Contributing

Contributions are always welcome!

If you'd like to contribute to this repository, please fork the repository and create a new branch for your changes. Once you've made your changes, submit a pull request and your changes will be reviewed.

