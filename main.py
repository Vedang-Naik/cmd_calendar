import calendar
import colorama
import argparse
import shlex
import pickle
import os
import datetime
import numpy
import time

from renderer import *

# Modifies the default calendar list returned by Calendar.monthdatescalendar().
def addEventToMonthCalendar(monthCalendar, month):
	global EVENTS

	for i in range(0, 5):
		for j in range(0, 7):
			if monthCalendar[i][j].month != month: # If the day is not in the month, replace with None.
				monthCalendar[i][j] = None
			elif monthCalendar[i][j] in EVENTS.keys(): # If this day has an event, make tuple of day and event
				monthCalendar[i][j] = (monthCalendar[i][j], len(EVENTS[monthCalendar[i][j]]))

	return monthCalendar

# Set up parsing of the command statement into its components.
def parseCommand(command):
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest="subcommand")

	# Used to display a specific day, month or year.
	display = subparsers.add_parser("display")
	display_group = display.add_mutually_exclusive_group()
	display_group.add_argument("-m", nargs=1)
	display_group.add_argument("-y", nargs=1)

	# Used to display the current day, month or year
	cur = subparsers.add_parser("cur")
	cur_group = cur.add_mutually_exclusive_group()
	cur_group.add_argument("-m", action="store_true")
	cur_group.add_argument("-y", action="store_true")

	# Used to add events to specific dates
	event = subparsers.add_parser("event")
	event_group = event.add_mutually_exclusive_group()
	event_group.add_argument("-a", nargs=2)
	event_group.add_argument("-s", nargs=1)

	# Used to close the application safely.
	exit = subparsers.add_parser("exit")	
	
	try:
		return vars(parser.parse_args(shlex.split(command)))
	except:
		return False # If parsing fails, return false so that execCommand() can catch and quit.

# Executes parsed commands.
def execCommand(command):
	global CMD_WIDTH, CMD_HEIGHT, EVENTS

	# Catches failed command parsing from parseCommand()
	if not command:
		return False
	
	os.system("cls")

	# Handles the "cur" command
	if command["subcommand"] == "cur":
		curMonth = datetime.datetime.now().month
		curYear = datetime.datetime.now().year
		headerText = "Displaying "

		if command["m"]:
			curMonthCalendar = calendar.Calendar(0).monthdatescalendar(curYear, curMonth)
			headerText += calendar.month_name[curMonth] + " " + str(curYear)
			renderMMMonth(addEventToMonthCalendar(curMonthCalendar, curMonth), CMD_WIDTH, CMD_HEIGHT, headerText)
		elif command["y"]:
			curYearCalendar = numpy.reshape(calendar.Calendar(0).yeardayscalendar(curYear), (3, 4))
			headerText += str(curYear)
			renderYMYear(curYearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

	elif command["subcommand"] == "display":
		dispm = command["m"]
		dispy = command["y"]
		headerText = "Displaying "

		if dispm is not None:
			date = list(map(int, dispm[0].split("/")))
			month, year = date
			headerText += calendar.month_name[month] + " " + str(year)
			monthCalendar = calendar.Calendar(0).monthdatescalendar(year, month)
			renderMMMonth(addEventToMonthCalendar(monthCalendar, month), CMD_WIDTH, CMD_HEIGHT, headerText)
		elif dispy is not None:
			year = int(dispy[0])
			headerText += str(year)
			yearCalendar = numpy.reshape(calendar.Calendar(0).yeardayscalendar(year), (3, 4))
			renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

	elif command["subcommand"] == "event":
		add = command["a"]
		search = command["s"]

		if add is not None:
			date = list(map(int, add[0].split("/")))
			date = datetime.date(date[2], date[1], date[0])
			event = add[1].strip()
			if date in EVENTS.keys():
				EVENTS[date].append(event)
			else:
				EVENTS[date] = [event]
			with open("events.pkl", "wb") as f:
				pickle.dump(EVENTS, f)

		elif search is not None:
			date = list(map(int, search[0].split("/")))
			date = datetime.date(date[2], date[1], date[0])
			if date in EVENTS.keys():
				monthCalendar = calendar.Calendar(0).monthdatescalendar(date.year, date.month)
				renderMMMonth(addEventToMonthCalendar(monthCalendar, date.month), CMD_WIDTH, CMD_HEIGHT, "Search Results")
				renderEventSearchBox(date, monthCalendar, EVENTS[date][:], CMD_WIDTH, CMD_HEIGHT)
			else:
				pass

	elif command["subcommand"] == "exit":
		return True


# Init colorama so ANSI sequences are converted to Windows equivalents
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
command = "event -s 23/08/2018"
execCommand(parseCommand(command))
while True:
	command = input("calendar>")
	status = execCommand(parseCommand(command))
	if status:
		break
	elif not status:
		continue