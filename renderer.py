import calendar
from pyfiglet import Figlet

def printAt(x, y, text):
	print("\033[" + str(x) + ";" + str(y) + "H" + text, end="")

def renderHeader(CMD_WIDTH, text):
	topLine = "|" + u'\u0305' * (CMD_WIDTH - 2) + "|"
	heading = "|" + text.center(CMD_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"

	print(topLine)
	print(heading)
	print(bottomLine)

def renderMainPage(CMD_WIDTH, CMD_HEIGHT):
	topLine = "|" + u"\u0305" * (CMD_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"
	padding = "|" + " " * (CMD_WIDTH - 2) + "|"

	f = Figlet(font="slant")
	string = str(f.renderText("CMD Calendar"))
	splits = ["|" + a.center(CMD_WIDTH - 2) + "|" for a in string.split("\n")]
	CMD_HEIGHT -= len(splits)

	print(topLine)
	for _ in range(1, CMD_HEIGHT // 2):
		print(padding)
	for a in splits:
		print(a, end="")
	for _ in range(CMD_HEIGHT // 2, CMD_HEIGHT - 1):
		print(padding)
	print(bottomLine, end="")

def renderError(CMD_WIDTH, CMD_HEIGHT, errorMessage):
	topLine = "|" + u"\u0305" * (CMD_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"
	padding = "|" + " " * (CMD_WIDTH - 2) + "|"

	msgTopLine = "|" + ("|" + u"\u0305" * (CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"
	msgBottomLine = "|" + ("|" + "_" * (CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"
	msg = "|" + ("|" + errorMessage.center(CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"

	f = Figlet(font="poison")
	string = str(f.renderText("Error"))
	splits = ["|" + a.center(CMD_WIDTH - 2) + "|" for a in string.split("\n")]

	CMD_HEIGHT -= len(splits) + 6
	
	print(topLine)
	for _ in range(CMD_HEIGHT // 2):
		print(padding)
	for a in splits:
		print(a, end="")
	print(msgTopLine)
	print(msg)
	print(msgBottomLine)
	for _ in range(CMD_HEIGHT // 2):
		print(padding)
	print(bottomLine)

def renderMMDay(x, y, MM_WIDTH, MM_HEIGHT, dayInfo):
	topLine = "|" + u'\u0305' * (MM_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (MM_WIDTH - 2) + "|"

	printAt(x, y, topLine)
	if dayInfo:
		padding = "|" + " " * (MM_WIDTH - 2) + "|"
		date = ""
		events = ""
		if type(dayInfo) is tuple:
			date = "|" + str(dayInfo[0].day).center(MM_WIDTH - 2) + "|"
			events = str(dayInfo[1]) + " event(s)"
			events = "|" + events.center(MM_WIDTH - 2) + "|"
		else:
			date = "|" + str(dayInfo.day).center(MM_WIDTH - 2) + "|"
			events = "|" + " " * (MM_WIDTH - 2) + "|"
		
		printAt(x + 1, y, date)
		printAt(x + 2, y, padding)
		printAt(x + 3, y, events)
		for i in range(4, MM_HEIGHT - 1):
			printAt(x + i, y, padding)
	else:
		crosses = "| " + "x" * (MM_WIDTH - 4) + " |"
		for i in range(1, MM_HEIGHT - 1):
			printAt(x + i, y, crosses)
	printAt(x + MM_HEIGHT - 1, y, bottomLine)

def renderMMMonth(monthCalendar, CMD_WIDTH, CMD_HEIGHT, headerText):
	CMD_WIDTH -= CMD_WIDTH % 7
	CMD_HEIGHT -= 5
	CMD_HEIGHT -= CMD_HEIGHT % len(monthCalendar)

	MM_WIDTH = CMD_WIDTH // 7
	MM_HEIGHT = CMD_HEIGHT // len(monthCalendar)

	renderHeader(CMD_WIDTH, headerText)
	for day in calendar.day_name:
		print("|" + day.center(MM_WIDTH - 2, u"\u00b7") + "|", end="")
	for x, week in zip(range(5, CMD_HEIGHT+1, MM_HEIGHT), monthCalendar):
		for y, day in zip(range(1, CMD_WIDTH, MM_WIDTH), week):
			renderMMDay(x, y, MM_WIDTH, MM_HEIGHT, day)
	print()

def renderYMMonth(x, y, YM_WIDTH, YM_HEIGHT, monthCalendar, monthInd):
	topLine = "|" + u"\u0305" * (YM_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (YM_WIDTH - 2) + "|"
	padding = "|" + " " * (YM_WIDTH - 2) + "|"
	monthName = "|" + calendar.month_name[monthInd + 1].center(YM_WIDTH - 2) + "|"

	numPaddingLines = YM_HEIGHT - 9
	YM_HEIGHT += x - 1

	printAt(x, y, topLine)
	printAt(x + 1, y, monthName)
	printAt(x + 2, y, padding)
	x += 3
	for _ in range(x, x + (numPaddingLines // 2)):
		printAt(x, y, padding)
		x += 1
	for week, _ in zip(monthCalendar, range(x, x + len(monthCalendar))):
		dayString = ""
		for day in week:
			if day == 0:
				dayString += " ".center((YM_WIDTH - 2 - (YM_WIDTH % 7)) // 7)
			else:
				dayString += str(day).center((YM_WIDTH - 2 - (YM_WIDTH % 7)) // 7)
		dayString = "|" + dayString.center(YM_WIDTH - 2) + "|"
		printAt(x, y, dayString)
		x += 1
	for _ in range(0, 6-len(monthCalendar)):
		printAt(x, y, padding)
		x += 1
	for _ in range(x, YM_HEIGHT):
		printAt(x, y, padding)
		x += 1
	printAt(x, y, bottomLine)

def renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText):
	CMD_WIDTH -= CMD_WIDTH % 4
	CMD_HEIGHT -= 5
	CMD_HEIGHT -= CMD_HEIGHT % 3

	YM_WIDTH = CMD_WIDTH // 4
	YM_HEIGHT = CMD_HEIGHT // 3

	renderHeader(CMD_WIDTH, headerText)

	dayString = ""
	for day in calendar.day_abbr:
		dayString += day.center((YM_WIDTH - 2 - (YM_WIDTH % 7)) // 7)
	dayString = "|" + dayString.center(YM_WIDTH - 2) + "|"
	print(dayString * 4)
	
	for i, y in zip(range(0, 4), range(1, CMD_WIDTH, YM_WIDTH)):
		for j, x in zip(range(0, 3), range(5, CMD_HEIGHT, YM_HEIGHT)):
			renderYMMonth(x, y, YM_WIDTH, YM_HEIGHT, yearCalendar[j][i], i+4*j)
	print()

def renderEventSearchBox(searchedDay, monthCalendar, eventList, CMD_WIDTH, CMD_HEIGHT):
	CMD_WIDTH -= CMD_WIDTH % 7
	CMD_HEIGHT -= 5
	CMD_HEIGHT -= CMD_HEIGHT % len(monthCalendar)

	MM_WIDTH = CMD_WIDTH // 7
	MM_HEIGHT = CMD_HEIGHT // len(monthCalendar)

	sx, sy = 0, 0
	for x, week in zip(range(5, CMD_HEIGHT + 1, MM_HEIGHT), monthCalendar):
		for y, day in zip(range(1, CMD_WIDTH, MM_WIDTH), week):			
			if type(day) is tuple and day[0] == searchedDay:
				sx = x
				sy = y
				break
	sx -= 3
	MM_WIDTH += 5
	MM_HEIGHT += 3

	topLine = "|" + u"\u0305" * (MM_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (MM_WIDTH - 2) + "|"
	padding = "|" + " " * (MM_WIDTH - 2) + "|"
	date = "|" + str(searchedDay.day).center(MM_WIDTH - 2) + "|"
	if len(eventList) <= MM_HEIGHT - 4:
		eventList.extend([" "] * (MM_HEIGHT - 4 - len(eventList)))
	leftOver = len(eventList) - (MM_HEIGHT - 4)

	printAt(sx, sy, topLine)
	printAt(sx+1, sy, date)
	sx += 1
	for i in range(MM_HEIGHT - 4):	
		sx += 1
		event = "|" + eventList[i][:MM_WIDTH - 4].center(MM_WIDTH - 2) + "|"
		printAt(sx, sy, event)
	sx += 1
	if leftOver > 0:
		temp = "+" + str(leftOver) + " more"
		printAt(sx, sy, "|" + temp.center(MM_WIDTH - 2) + "|")
	else:
		printAt(sx, sy, padding)
	printAt(sx+1, sy, bottomLine)
	print("\n" * (CMD_HEIGHT+3 - sx))