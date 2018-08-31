import calendar
from pyfiglet import Figlet

# --- FUNCTION ----
# DESC: Prints a string at a given coordinate.
# INPUT: Prints text at coordinates x, y 
# RETURN: None
# -----------------
def printAt(x, y, text):
	# Uses ANSI cursor positioning to move the cursor.
	print("\033[" + str(x) + ";" + str(y) + "H" + text, end="")

# --- FUNCTION ----
# DESC: Displays the header row.
# INPUT: Centers text in CMD_WIDTH space.
# RETURN: None
# -----------------
def renderHeader(CMD_WIDTH, text):
	topLine = "|" + u'\u0305' * (CMD_WIDTH - 2) + "|"
	heading = "|" + text.center(CMD_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"

	print(topLine)
	print(heading)
	print(bottomLine)

# --- FUNCTION ----
# DESC: Renders the main page.
# INPUT: The main page is CMD_WIDTH x CMD_HEIGHT big.
# RETURN: None
# -----------------
def renderMainPage(CMD_WIDTH, CMD_HEIGHT):
	# u0305 is the overbar symbol in Unicode.
	topLine = "|" + u"\u0305" * (CMD_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"
	padding = "|" + " " * (CMD_WIDTH - 2) + "|"

	# pyfiglet is used to generate a nice ASCII font.
	# The string returned is not centered, so it is split at the newline and individually centered before being stiched back up again.
	f = Figlet(font="slant")
	string = str(f.renderText("CMD Calendar"))
	splits = ["|" + a.center(CMD_WIDTH - 2) + "|" for a in string.split("\n")]
	# CMD_HEIGHT is used inside to count how many lines are left that need printing. It must be decremented by the height of the Figlet font.
	CMD_HEIGHT -= len(splits)

	print(topLine)
	for _ in range(1, CMD_HEIGHT // 2):
		print(padding)
	# Each a in splits already has a newline at the end, hence print(, end="")
	for a in splits:
		print(a, end="")
	for _ in range(CMD_HEIGHT // 2, CMD_HEIGHT - 1):
		print(padding)
	print(bottomLine, end="")

# --- FUNCTION ----
# DESC: Renders the error page.
# INPUT: Dimensions CMD_WIDTH and CMD_HEIGHT, the errorMessage to display.
# RETURN: None
# -----------------
def renderError(CMD_WIDTH, CMD_HEIGHT, errorMessage):
	topLine = "|" + u"\u0305" * (CMD_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"
	padding = "|" + " " * (CMD_WIDTH - 2) + "|"

	# These three lines create a centered box in the middle of the screen, with the message in between the overbar and underscore lines.
	msgTopLine = "|" + ("|" + u"\u0305" * (CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"
	msgBottomLine = "|" + ("|" + "_" * (CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"
	msg = "|" + ("|" + errorMessage.center(CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"

	f = Figlet(font="poison")
	string = str(f.renderText("Error"))
	splits = ["|" + a.center(CMD_WIDTH - 2) + "|" for a in string.split("\n")]

	# 6 lines removed, one each for topLine, bottomLine, the next input prompt and the error box's three lines.
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

# --- FUNCTION ----
# DESC: Renders a single day when display -m MONTH-DATE is used.
# INPUT: x, y are the coordinates of the top left corner of the day's box, MM_WIDTH and MM_HEIGHT its dimensions and dayinfo, the date and events of the day.
# RETURN: None.
# -----------------
def renderMMDay(x, y, MM_WIDTH, MM_HEIGHT, dayInfo):
	topLine = "|" + u'\u0305' * (MM_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (MM_WIDTH - 2) + "|"

	printAt(x, y, topLine)
	# If the day is not in the month, then it is replaced with a None by addEventToMonthCalendar().
	if dayInfo:
		padding = "|" + " " * (MM_WIDTH - 2) + "|"
		date = ""
		events = ""
		# If the day has an event, the number of events and the date object are bound in a tuple by addEventToMonthCalendar().
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

# --- FUNCTION ----
# DESC: Renders the screen seen when display -m MONTH-DATE is used.
# INPUT: A list monthCalendar of all dates for a month, the dimensions of the screen CMD_WIDTH and CMD_HEIGHT and the headerText to be shown on the top.
# RETURN: None
# -----------------
def renderMMMonth(monthCalendar, CMD_WIDTH, CMD_HEIGHT, headerText):
	CMD_WIDTH -= CMD_WIDTH % 7
	CMD_HEIGHT -= 5
	CMD_HEIGHT -= CMD_HEIGHT % len(monthCalendar)

	MM_WIDTH = CMD_WIDTH // 7
	MM_HEIGHT = CMD_HEIGHT // len(monthCalendar)

	renderHeader(CMD_WIDTH, headerText)
	# This prints the names of the days just under the header.
	for day in calendar.day_name:
		print("|" + day.center(MM_WIDTH - 2, u"\u00b7") + "|", end="")
	# The coordinates at which to print each day are calculated in increments of MM_HEIGHT and MM_WIDTH for each day in each week of monthCalendar.
	for x, week in zip(range(5, CMD_HEIGHT+1, MM_HEIGHT), monthCalendar):
		for y, day in zip(range(1, CMD_WIDTH, MM_WIDTH), week):
			renderMMDay(x, y, MM_WIDTH, MM_HEIGHT, day)
	# renderMMDay does not print a newline after rendering a day, so this pushes the cursor to the next line for the command prompt.
	print()

# --- FUNCTION ----
# DESC: Renders a single month's calendar when display -y YEAR is used.
# INPUT: The cooridinates x, y of the top left corner of the month of dimensions YM_WIDTH and YM_HEIGHT with monthInd to get its name and list monthCalendar to get its dates.
# RETURN: None
# -----------------
def renderYMMonth(x, y, YM_WIDTH, YM_HEIGHT, monthCalendar, monthInd):
	topLine = "|" + u"\u0305" * (YM_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (YM_WIDTH - 2) + "|"
	padding = "|" + " " * (YM_WIDTH - 2) + "|"
	# Centers the month name in YM_WIDTH space.
	monthName = "|" + calendar.month_name[monthInd + 1].center(YM_WIDTH - 2) + "|"

	# 9, one each for upto 6 weeks in a month, topLine, bottomLine and monthName.
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
	# Some months do not have 6 weeks in them, hence the extra padding so all months are the same height.
	for _ in range(0, 6-len(monthCalendar)):
		printAt(x, y, padding)
		x += 1
	for _ in range(x, YM_HEIGHT):
		printAt(x, y, padding)
		x += 1
	printAt(x, y, bottomLine)

# --- FUNCTION ----
# DESC: Renders the screen seen when display -y YEAR is used.
# INPUT: The calendar for the year yearCalendar, the dimensions CMD_WIDTH and CMD_HEIGHT and the headerText to be displayed on top.
# RETURN: None.
# -----------------
def renderYMYear(yearCalendar, CMD_WIDTH, CMD_HEIGHT, headerText):
	CMD_WIDTH -= CMD_WIDTH % 4
	CMD_HEIGHT -= 5
	CMD_HEIGHT -= CMD_HEIGHT % 3

	YM_WIDTH = CMD_WIDTH // 4
	YM_HEIGHT = CMD_HEIGHT // 3

	renderHeader(CMD_WIDTH, headerText)

	# This section prints four copies of | Mon Tue .. Sun | side by side for the month's columns to line up.
	dayString = ""
	for day in calendar.day_abbr:
		dayString += day.center((YM_WIDTH - 2 - (YM_WIDTH % 7)) // 7)
	dayString = "|" + dayString.center(YM_WIDTH - 2) + "|"
	print(dayString * 4)
	
	# yearCalendar as returned by Python contains four lists of three months each, as the in-built function prints a vertical calendar.
	# It is reshaped in execCommand to three list of four months each so that it can be printed here as a horizontal calendar.
	for i, y in zip(range(0, 4), range(1, CMD_WIDTH, YM_WIDTH)):
		for j, x in zip(range(0, 3), range(5, CMD_HEIGHT, YM_HEIGHT)):
			renderYMMonth(x, y, YM_WIDTH, YM_HEIGHT, yearCalendar[j][i], i+4*j)
	print()

# --- FUNCTION ----
# DESC: Renders the extended box shown for a day when an event is search for.
# INPUT: the date searchedDay searched for, the list monthCalendar to gets its position, the list of events eventList on the day and dimensions CMD_WIDTH and CMD_HEIGHT.
# RETURN: None.
# -----------------
def renderEventSearchBox(searchedDay, monthCalendar, eventList, CMD_WIDTH, CMD_HEIGHT):
	CMD_WIDTH -= CMD_WIDTH % 7
	CMD_HEIGHT -= 5
	CMD_HEIGHT -= CMD_HEIGHT % len(monthCalendar)

	MM_WIDTH = CMD_WIDTH // 7
	MM_HEIGHT = CMD_HEIGHT // len(monthCalendar)

	# This section gets the top left corner coordinates for the searched day by recreating the method renderMMMonth() uses. I should probably find a better way.
	sx, sy = 0, 0
	for x, week in zip(range(5, CMD_HEIGHT + 1, MM_HEIGHT), monthCalendar):
		for y, day in zip(range(1, CMD_WIDTH, MM_WIDTH), week):			
			if type(day) is tuple and day[0] == searchedDay:
				sx = x
				sy = y
				break
	# Move the x coordinate up and increase MM_WIDTH by 5 so that the search box is bigger that the day's box.
	sx -= 3
	MM_WIDTH += 5
	MM_HEIGHT += 3

	topLine = "|" + u"\u0305" * (MM_WIDTH - 2) + "|"
	bottomLine = "|" + "_" * (MM_WIDTH - 2) + "|"
	padding = "|" + " " * (MM_WIDTH - 2) + "|"
	date = "|" + str(searchedDay.day).center(MM_WIDTH - 2) + "|"
	# If there are less events than MM_HEIGHT-4 lines available to print, then the eventList is temporarily extended.
	if len(eventList) <= MM_HEIGHT - 4:
		eventList.extend([" "] * (MM_HEIGHT - 4 - len(eventList)))
	# If there happened to be more than MM_HEIGHT-4 events, then the number of events not shown is put in leftOver.
	leftOver = len(eventList) - (MM_HEIGHT - 4)

	printAt(sx, sy, topLine)
	printAt(sx+1, sy, date)
	sx += 1
	for i in range(MM_HEIGHT - 4):	
		sx += 1
		# If there are more than MM_HEIGHT-4 events, only the first MM_HEIGHT-4 of them are shown.
		event = "|" + eventList[i][:MM_WIDTH - 4].center(MM_WIDTH - 2) + "|"
		printAt(sx, sy, event)
	sx += 1
	# leftOver is only printed if it is greater than 0.
	if leftOver > 0:
		temp = "+" + str(leftOver) + " more"
		printAt(sx, sy, "|" + temp.center(MM_WIDTH - 2) + "|")
	else:
		printAt(sx, sy, padding)
	printAt(sx+1, sy, bottomLine)
	# This moves the next prompt to the bottom of the month screen. Otherwise, it comes right after where the cursor finished after rendering the search box.
	print("\n" * (CMD_HEIGHT+3 - sx))