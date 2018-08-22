import calendar
import colorama
import argparse
import shlex
import pickle

from os import get_terminal_size, system
from datetime import datetime, date
from renderer import *
from numpy import reshape
from time import sleep

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
	display_group.add_argument("-d", nargs=3)
	display_group.add_argument("-m", nargs=2)
	display_group.add_argument("-y", nargs=1)

	# Used to display the current day, month or year
	cur = subparsers.add_parser("cur")
	cur_group = cur.add_mutually_exclusive_group()
	cur_group.add_argument("-d", action="store_true")
	cur_group.add_argument("-m", action="store_true")
	cur_group.add_argument("-y", action="store_true")

	# Used to add events to specific dates
	event = subparsers.add_parser("event")
	event_group = event.add_mutually_exclusive_group()
	event_group.add_argument("-v", action="store_true")
	event_group.add_argument("-a", nargs=2)

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
	
	system("cls")

	# Handles the "cur" command
	if command["subcommand"] == "cur":
		curDay = datetime.now().day
		curMonth = datetime.now().month
		curYear = datetime.now().year
		headerText = "Displaying "

		if command["m"]:
			curMonthCalendar = calendar.Calendar(0).monthdatescalendar(curYear, curMonth)
			headerText += calendar.month_name[curMonth] + " " + str(curYear)
			renderMMMonth(addEventToMonthCalendar(curMonthCalendar, curMonth), CMD_WIDTH, CMD_HEIGHT, headerText)
		elif command["y"]:
			curYearCalendar = reshape(calendar.Calendar(0).yeardayscalendar(curYear), (3, 4))
			headerText += str(curYear)
			renderYMYear(curYearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)
		elif command["d"]:
			temp = date(curYear, curMonth, curDay)
			headerText += str(curDay) + " " + month_name[curMonth] + " " + str(curYear)
			# The body of a day contains only the events of that day, hence None is no events.
			if temp in EVENTS.keys():
				renderDMDay(EVENTS[temp], CMD_WIDTH, CMD_HEIGHT, headerText)
			else:
				renderDMDay(None, CMD_WIDTH, CMD_HEIGHT, headerText)

	elif command["subcommand"] == "display":
		dispd = command["d"]
		dispm = command["m"]
		dispy = command["y"]

		headerText = "Displaying "

		if dispd is not None:
			pass
		elif dispm is not None:
			month = list(calendar.month_name).index(dispm[0])
			year = int(dispm[1])
			headerText += calendar.month_name[month] + " " + str(year)
			monthCalendar = calendar.Calendar(0).monthdatescalendar(year, month)
			renderMMMonth(addEventToMonthCalendar(monthCalendar, month), CMD_WIDTH, CMD_HEIGHT, headerText)
		elif dispy is not None:
			year = int(dispy[0])
			headerText += str(year)
			yearCalendar = reshape(calendar.Calendar(0).yeardayscalendar(year), (3, 4))
			renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)


	elif command["subcommand"] == "event":
		if command["a"] is not None:
			pass
		elif command["v"]:
			renderEventList(EVENTS, CMD_WIDTH, CMD_HEIGHT, "Displaying Event List")
		# day = list(map(int, command["e"][0].split("/")))
		# day = date(day[2], day[1], day[0])
		# events = command["e"][1].split(",")

		# if day in EVENTS.keys():
		# 	EVENTS[day].extend(events)
		# else:
		# 	EVENTS[day] = events
		# with open("events.pkl", "wb") as f:
		# 	pickle.dump(EVENTS, f)

		# renderDMDay(day, CMD_WIDTH, CMD_HEIGHT)

	elif command["subcommand"] == "exit":
		return True



# Init colorama so ANSI sequences are converted to Windows equivalents
colorama.init()

# Get initial CMD dimensions and events from file
CMD_WIDTH = get_terminal_size()[0]
CMD_HEIGHT = get_terminal_size()[1]
with open("events.pkl", "rb") as f:
	EVENTS = pickle.load(f)

# Clear screen and render main page
system("cls")
renderMainPage(CMD_WIDTH, CMD_HEIGHT)
sleep(1)

# Default command is the current month.
command = "event -v"
execCommand(parseCommand(command))
# while True:
# 	command = input("calendar>")
# 	status = execCommand(parseCommand(command))
# 	if status:
# 		break
# 	elif not status:
# 		continue