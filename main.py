import calendar
import colorama
import argparse
import shlex
import pickle

from os import get_terminal_size, system, fdopen
from datetime import datetime, date
from renderer import *
from numpy import reshape
from time import sleep

def required_length(nmin,nmax):
	class RequiredLength(argparse.Action):
		def __call__(self, parser, args, values, option_string=None):
			if not nmin <= len(values) <= nmax:
				msg = "argument -{f}: expected between {nmin} and {nmax} arguments".format(f=self.dest, nmin=nmin, nmax=nmax)
				parser.error(msg)
			setattr(args, self.dest, values)
	return RequiredLength

def addEventToMonthCalendar(monthCalendar, month):
	global EVENTS

	for i in range(0, 5):
		for j in range(0, 7):
			if monthCalendar[i][j].month != month:
				monthCalendar[i][j] = None
			elif monthCalendar[i][j] in EVENTS.keys():
				monthCalendar[i][j] = (monthCalendar[i][j], len(EVENTS[monthCalendar[i][j]]))

	return monthCalendar

def parseCommand(command):
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest="subcommand")

	display = subparsers.add_parser("display")
	display_group = display.add_mutually_exclusive_group()
	display_group.add_argument("-d", nargs="*", action=required_length(0, 3))
	display_group.add_argument("-m", nargs="*", action=required_length(0, 2))
	display_group.add_argument("-y", nargs="*", action=required_length(0, 1))

	cur = subparsers.add_parser("cur")
	cur_group = cur.add_mutually_exclusive_group()
	cur_group.add_argument("-d", action="store_true")
	cur_group.add_argument("-m", action="store_true")
	cur_group.add_argument("-y", action="store_true")

	add = subparsers.add_parser("add")
	add_group = add.add_mutually_exclusive_group()
	add_group.add_argument("-e", nargs=2)

	exit = subparsers.add_parser("exit")	
	
	try:
		return vars(parser.parse_args(shlex.split(command)))
	except:
		return False

def execCommand(command):
	global CMD_WIDTH, CMD_HEIGHT, EVENTS

	if not command:
		return False
	
	system("cls")
	if command["subcommand"] == "cur":
		curDay = datetime.now().day
		curMonth = datetime.now().month
		curYear = datetime.now().year
		if command["m"]:			
			curMonthCalendar = calendar.Calendar(0).monthdatescalendar(curYear, curMonth)
			headerText = "Displaying " + calendar.month_name[curMonth] + " " + str(curYear)
			renderMMMonth(addEventToMonthCalendar(curMonthCalendar, curMonth), CMD_WIDTH, CMD_HEIGHT, headerText)
		if command["y"]:
			curYearCalendar = reshape(calendar.Calendar(0).yeardayscalendar(curYear), (3, 4))
			headerText = "Displaying " + str(curYear)
			renderYMYear(curYearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)
		if command["d"]:
			today = date(curYear, curMonth, curDay)
			renderDMDay(today, CMD_WIDTH, CMD_HEIGHT)

	elif command["subcommand"] == "display":
		dispm = command["m"]
		dispy = command["y"]
		dispd = command["d"]

		if dispm is not None:
			month = datetime.now().month
			year = datetime.now().year
			headerText = "Displaying "
			if len(dispm) == 0:
				headerText += calendar.month_name[month] + " " + str(year)			
			elif len(dispm) == 1:
				month = list(calendar.month_name).index(dispm[0])
				headerText += dispm[0] + " " + str(year)
			elif len(dispm) == 2:
				month = list(calendar.month_name).index(dispm[0])
				year = int(dispm[1])
				headerText += dispm[0] + " " + dispm[1]				
			monthCalendar = calendar.Calendar(0).monthdatescalendar(year, month)
			renderMMMonth(addEventToMonthCalendar(monthCalendar, month), CMD_WIDTH, CMD_HEIGHT, headerText)

		elif dispy is not None:
			year = datetime.now().year
			headerText = "Displaying "
			if len(dispy) == 0:
				headerText += str(year)
			elif len(dispy) == 1:
				year = int(dispy[0])
				headerText += str(dispy[0])
			yearCalendar = reshape(calendar.Calendar(0).yeardayscalendar(year), (3, 4))
			renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

	elif command["subcommand"] == "add":
		day = list(map(int, command["e"][0].split("/")))
		day = date(day[2], day[1], day[0])
		events = command["e"][1].split(",")

		if day in EVENTS.keys():
			EVENTS[day].extend(events)
		else:
			EVENTS[day] = events
		with open("events.pkl", "wb") as f:
			pickle.dump(EVENTS, f)

		renderDMDay(day, CMD_WIDTH, CMD_HEIGHT)

	elif command["subcommand"] == "exit":
		return True

colorama.init()

CMD_WIDTH = get_terminal_size()[0]
CMD_HEIGHT = get_terminal_size()[1]
with open("events.pkl", "rb") as f:
	EVENTS = pickle.load(f)

system("cls")
renderMainPage(CMD_WIDTH, CMD_HEIGHT)
sleep(1)

command = "display -m September 2018"
execCommand(parseCommand(command))
while True:
	command = input("calendar>")
	status = execCommand(parseCommand(command))
	if status:
		break
	elif not status:
		continue