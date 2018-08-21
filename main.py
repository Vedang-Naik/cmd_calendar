import calendar
import colorama
import argparse
import shlex
import sys

from multiprocessing import Process, Queue
from os import get_terminal_size, system, fdopen
from datetime import datetime, date
from renderer import *
from numpy import reshape
from time import sleep

def getEvents(filename):
	events = {}
	with open(filename, "r") as f:
		for line in f:
			day = list(map(int, line.strip().split(":")[0].split(" ")))
			day = date(day[0], day[1], day[2])
			events[day] = line.strip().split(":")[1].split(",")
	return events

def required_length(nmin,nmax):
	class RequiredLength(argparse.Action):
		def __call__(self, parser, args, values, option_string=None):
			if not nmin<=len(values)<=nmax:
				msg='argument -{f}: expected between {nmin} and {nmax} arguments'.format(
					f=self.dest,nmin=nmin,nmax=nmax)
				parser.error(msg)
			setattr(args, self.dest, values)
	return RequiredLength

def parseCommand(COMMAND):
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
	
	try:
		return parser.parse_args(shlex.split(COMMAND))
	except:
		return -1

def execCommand(COMMAND, CMD_WIDTH, CMD_HEIGHT, EVENTS):
	if COMMAND == -1:
		return
	COMMAND = vars(COMMAND)
	if COMMAND["subcommand"] == "cur":
		if COMMAND["m"]:
			month = datetime.now().month
			year = datetime.now().year
			monthCalendar = calendar.Calendar(0).monthdatescalendar(year, month)
			for i in range(0, 5):
				for j in range(0, 7):
					if monthCalendar[i][j] in EVENTS.keys():
						monthCalendar[i][j] = (monthCalendar[i][j], len(EVENTS[monthCalendar[i][j]]))

			headerText = "Displaying " + calendar.month_name[month] + " " + str(year)

			system("cls")
			renderMMMonth(monthCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)
		if COMMAND["y"]:
			year = datetime.now().year
			yearCalendar = calendar.Calendar(0).yeardayscalendar(year)
			yearCalendar = reshape(yearCalendar, (3, 4))
			headerText = "Displaying " + str(year)

			system("cls")
			renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

	elif COMMAND["subcommand"] == "display":
		dispm = COMMAND["m"]
		dispy = COMMAND["y"]
		if dispm is not None:
			if len(dispm) == 0:
				month = datetime.now().month
				year = datetime.now().year
				monthCalendar = calendar.Calendar(0).monthdayscalendar(year, month)
				headerText = "Displaying " + calendar.month_name[month] + " " + str(year)

				system("cls")
				renderMMMonth(monthCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)				
			elif len(dispm) == 1:
				month = list(calendar.month_name).index(dispm[0])
				year = datetime.now().year
				monthCalendar = calendar.Calendar(0).monthdayscalendar(year, month)
				headerText = "Displaying " + dispm[0] + " " + str(year)

				system("cls")
				renderMMMonth(monthCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)
			elif len(dispm) == 2:
				month = list(calendar.month_name).index(dispm[0])
				monthCalendar = calendar.Calendar(0).monthdayscalendar(int(dispm[1]), month)
				headerText = "Displaying " + dispm[0] + " " + dispm[1]

				system("cls")
				renderMMMonth(monthCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

		elif dispy is not None:			
			if len(dispy) == 0:				
				year = datetime.now().year
				yearCalendar = calendar.Calendar(0).yeardayscalendar(year)
				yearCalendar = reshape(yearCalendar, (3, 4))
				headerText = "Displaying " + str(year)

				system("cls")
				renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)
			elif len(dispy) == 1:
				yearCalendar = calendar.Calendar(0).yeardayscalendar(int(dispy[0]))
				yearCalendar = reshape(yearCalendar, (3, 4))
				headerText = "Displaying " + str(dispy[0])

				system("cls")
				renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText)

	return True

def main():
	colorama.init()

	CMD_WIDTH = get_terminal_size()[0]
	CMD_HEIGHT = get_terminal_size()[1]

	EVENTS = getEvents("events.txt")
	# print(events)

	# system("cls")
	# renderMainPage(CMD_WIDTH, CMD_HEIGHT)
	# sleep(1)

	COMMAND = "cur -m"
	execCommand(parseCommand(COMMAND), CMD_WIDTH, CMD_HEIGHT, EVENTS)
	# while True:
	# 	COMMAND = input("calendar>")
	# 	execCommand(parseCommand(COMMAND), CMD_WIDTH, CMD_HEIGHT)

if __name__ == "__main__":
	main()