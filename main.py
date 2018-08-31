# ---- PROJECT DESCRIPTION ----
# CMD_CALENDAR is an attempt to make a calendar system with events and reminders on the command line. It is akin to a very-simplified Google Calendar, Windows Calendar, etc.
# FEATURES: 1. The calendar of any month or year can be displayed here (Gregorian only, infinitely extended in both directions).
#           2. Events can be added to any particular day. One can search for events and delete them.
# USAGE: Start main.py using python. At the calendar> prompt, enter the specific command to do whatever you wish to do. calendar> -h will provide help.
# PLANS: 1. Reminders for events through either email or desktop notifications are planned. 
#        2. A more colourful UI might be implemented.
# 
# WORKING: 1. Once main.py starts up, it shows the calendar for the current month and an input prompt.
#          2. The user enters a argument at the prompt. This is error-checked and parsed by parseCommand()
#          3. The parsed command is sent to execCommand(), which carries out the user's operation.
#             -> If command parsing fails, the error will be displayed, followed by the next prompt.
#             -> If the input is invalid, the error page is shown, followed by the next prompt.
#          4. Once the operation is done, the prompt is displayed again for the next command.
#          5. Steps 2-4 continue for ever until the user inputs "exit" or closes the program in some other fashion.

import calendar # In-built: Used for getting the calendars for any month or year.
import colorama # pip installed: Used for enabling ANSI sequences for cursor positioning and colours in Windows.
import argparse # In-built: Used for argument parsing.
import shlex # In-built: Extends argparse to strings which resemble arguments.
import pickle # In-built: Used to store the events dictionary offline.
import os # In-built: Used to get the CMD dimensions and clear the screen.
import datetime # In-built: Used for manipulating dates easily.
import numpy # pip installed: Used for reshaping an array in one place; it will be removed once a better way is found.
import time # In-built: Used for the sleep function; if you do not want the main page to be displayed, you can delete this.

from renderer import renderMainPage, renderMMMonth, renderYMYear, renderEventSearchBox, renderError

# --- FUNCTION ----
# DESC: Adds events to days and removes days not in a month for a list of dates in a month.
# INPUT: The calendar list returned by calendar.Calendar(0).monthdatescalendar
# RETURN: The modified calendar list if successful, which it should always be.
# -----------------
def addEventToMonthCalendar(monthCalendar, month):
    global EVENTS
    for i in range(0, len(monthCalendar)):
        for j in range(0, 7):
            if monthCalendar[i][j].month != month: # If the day is not in the month, replace with None.
                monthCalendar[i][j] = None
            elif monthCalendar[i][j] in EVENTS.keys(): # If this day has an event, make tuple of day and event
                monthCalendar[i][j] = (monthCalendar[i][j], len(EVENTS[monthCalendar[i][j]]))
    return monthCalendar

# --- FUNCTION ----
# DESC: Set up parsing of the command statement into its components.
# INPUT: Takes in a command and parses it.
# RETURN: False if the parsing fails, else the dictionary of the parsed command.
# -----------------
def parseCommand(command):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    # This subcommand group will handle the displaying of months and years. 
    display = subparsers.add_parser("display", help="Display the calendar of a month or year.")
    display_group = display.add_mutually_exclusive_group()
    # display -m will display the calendar for a given month.
    # display -m will default to the present day if no argumets are provided.
    display_group.add_argument("-m", nargs="?", const=datetime.datetime.now().strftime("%m-%Y"), type=str, help="Display the calendar of a specific month, input as mm-yyyy.", metavar="MONTH-DATE")
    # display -y will display the calendar for a given year.
    # display -y will default to present year if no arguments are provided.
    display_group.add_argument("-y", nargs="?", const=datetime.datetime.now().strftime("%Y"), type=str, help="Display the calendar of a specific year, input as yyyy.", metavar="YEAR")
        
    # This subcommand group will handles various actions concerning events.
    event = subparsers.add_parser("event", help="Add, delete and search for events.")
    event_group = event.add_mutually_exclusive_group()
    # event -a will add events to specific dates.
    event_group.add_argument("-a", nargs=2, help="Add an event to a particular day.", metavar=("DATE", "EVENT"))
    # event -s will display all the events for a particular day.
    # event -s will default to the present day if no argumets are provided.
    event_group.add_argument("-s", nargs="?", const=datetime.datetime.now().strftime("%d-%m-%Y"), type=str, help="Search for events on a specific day.", metavar=("DATE"))
    # event -d will delete an event from a day.
    event_group.add_argument("-d", nargs=2, help="Delete an event on a specific day.", metavar=("DATE", "EVENT_INDEX"))

    # This subcommand will close the application safely.
    exit = subparsers.add_parser("exit", help="Exit the application safely.")
    
    # If parsing fails, return false so that execCommand() can catch and quit.
    try:
        return vars(parser.parse_args(shlex.split(command)))
    except:
        return False

# --- FUNCTION ----
# DESC: Executes parsed commands received by parseCommand() 
# INPUT: Takes a parsed command dictionary and executes it.
# RETURN: False if parseCommand returns False, True if the user inputs exit and None otherwise.
# -----------------
def execCommand(command):
    global CMD_WIDTH, CMD_HEIGHT, EVENTS

    # Catches failed command parsing from parseCommand()
    if not command:
        return False

    os.system("cls")
    if command["subcommand"] == "display":
        dispm = command["m"]
        dispy = command["y"]
        headerText = "Displaying "

        if dispm is not None:
            # Prevents alphabets, etc. by catching the int()'s exception
            try:
                date = list(map(int, dispm.split("-")))

                # Checks if there are two numbers for the month and year in the date.
                if len(date) != 2:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Please use display -m in the form mm-yyyy.")
                    return None
                month, year = date

                 # Checks if the day, month and year are in the right bounds.
                if not (1 <= month <= 12 and year > 0):
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Enter a month number between 1 and 12, inclusive, and a positive integer year.")
                    return None
            except:
                renderError(CMD_WIDTH, CMD_HEIGHT, "Perhaps you did not use a '-' to seperate the month and year?")
                return None
            
            # Add the month and year to the header
            # Then, get the dates for the specified month, runAddEventToMonthCalendar() (please refer above) and render.
            headerText += calendar.month_name[month] + " " + str(year)
            monthCalendar = calendar.Calendar(0).monthdatescalendar(year, month)
            renderMMMonth(addEventToMonthCalendar(monthCalendar, month), CMD_WIDTH, CMD_HEIGHT, headerText)

        elif dispy is not None:
            # Same code as dispm, please refer above.
            try:
                year = int(dispy)
                if year <= 0:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Please enter a positive integer year.")
                    return None
            except:
                renderError(CMD_WIDTH, CMD_HEIGHT, "Please enter valid numbers.")
                return None
            
            # Add the year to the header
            # Then, get the dates for the specified year and render its calendar.
            headerText += str(year)
            yearCalendar = numpy.reshape(calendar.Calendar(0).yeardayscalendar(year), (3, 4))
            renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

    elif command["subcommand"] == "event":
        add = command["a"]
        search = command["s"]
        delete = command["d"]

        if add is not None:
            # Same code as dispm, please refer above.
            try:
                date = list(map(int, add.split("-")))
                if len(date) != 3:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "You have not provided a valid day, month or year.")
                    return None
                day, month, year = date
                
                # Make sure that the date entered is valid i.e. catch February 30th, etc.
                try:
                    date = datetime.date(year, month, day)
                except:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Your date, like February 30th, is invalid.")
                    return None
            except:
                renderError(CMD_WIDTH, CMD_HEIGHT, "Perhaps you did not use a '-' to seperate the month and year?")
                return None
            
            # Check if the event string is empty.
            if add[1]:
                renderError(CMD_WIDTH, CMD_HEIGHT, "Please enter a non-blank event.")
                return None
            event = add[1].strip()

            # Append to the event list for the specified date if it exists, else create a new list with this event.
            # Then, save the updated dictionary of events to events.pkl.
            if date in EVENTS.keys():
                EVENTS[date].append(event)
            else:
                EVENTS[date] = [event]            
            with open("events.pkl", "wb") as f:
                pickle.dump(EVENTS, f)

        elif search is not None:
            # Same code as for dispm, please refer above. 
            try:
                date = list(map(int, search.split("-")))                
                if len(date) != 3:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "You have not provided a valid day, month or year.")
                    return None
                day, month, year = date               
                try:
                    date = datetime.date(year, month, day)
                except:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Your date, like February 30th, is invalid.")
                    return None
            except:
                renderError(CMD_WIDTH, CMD_HEIGHT, "Perhaps you did not use a '-' to seperate the day, month and year?")
                return None
            
            # Checks if events exist in the specified day's events list.
            if date in EVENTS.keys():
                monthCalendar = calendar.Calendar(0).monthdatescalendar(date.year, date.month)
                renderMMMonth(addEventToMonthCalendar(monthCalendar, date.month), CMD_WIDTH, CMD_HEIGHT, "Search Results")
                renderEventSearchBox(date, monthCalendar, EVENTS[date][:], CMD_WIDTH, CMD_HEIGHT)
            else:
                renderError(CMD_WIDTH, CMD_HEIGHT, "No events were found on this day.")
                return None

        elif delete is not None:
            try:
                date = list(map(int, delete[0].split("-")))                
                if len(date) != 3:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "You have not provided a valid day, month or year.")
                    return None
                day, month, year = date               
                try:
                    date = datetime.date(year, month, day)
                except:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Your date, like February 30th, is invalid.")
                    return None
            except:
                renderError(CMD_WIDTH, CMD_HEIGHT, "Perhaps you did not use a '-' to seperate the day, month and year?")
                return None
            
            if date in EVENTS.keys():
                try:
                    index = int(delete[1])
                    if not 0 < index < len(EVENTS[date]) + 1:
                        renderError(CMD_WIDTH, CMD_HEIGHT, "Your index must be in between 0 and " + str(len(EVENTS[date] + 1)))
                        return None
                except:
                    renderError(CMD_WIDTH, CMD_HEIGHT, "Please enter a valid numerical character.")
                    return None
                EVENTS[date].pop(index - 1)
                with open("events.pkl", "wb") as f:
                    pickle.dump(EVENTS, f)
            else:
                renderError(CMD_WIDTH, CMD_HEIGHT, "There are no events on this day.")
                return None

    elif command["subcommand"] == "exit":
        return True

    return None


# ==== Driver Code ====

# Init colorama so ANSI sequences can be used.
colorama.init()

# Get initial CMD dimensions and events from file
CMD_WIDTH = os.get_terminal_size()[0]
CMD_HEIGHT = os.get_terminal_size()[1]
with open("events.pkl", "rb") as f:
    EVENTS = pickle.load(f)

# Clear screen and render main page
os.system("cls")
renderMainPage(CMD_WIDTH, CMD_HEIGHT)
time.sleep(1)

# Default command is the current month.
command = "display -m"
execCommand(parseCommand(command))
while True:
    command = input("calendar>")
    status = execCommand(parseCommand(command))
    if status:
        break
    elif not status:
        continue
    
# =====================