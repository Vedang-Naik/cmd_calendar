import os
from pyfiglet import Figlet

CMD_WIDTH = os.get_terminal_size()[0]
CMD_HEIGHT = os.get_terminal_size()[1]

topLine = "|" + u"\u0305" * (CMD_WIDTH - 2) + "|"
bottomLine = "|" + "_" * (CMD_WIDTH - 2) + "|"
padding = "|" + " " * (CMD_WIDTH - 2) + "|"

msg = "The date you entered does not exist."

msgTopLine = "|" + ("|" + u"\u0305" * (CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"
msgBottomLine = "|" + ("|" + "_" * (CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"
msg = "|" + ("|" + msg.center(CMD_WIDTH // 2) + "|").center(CMD_WIDTH - 2) + "|"

f = Figlet(font="poison")
string = str(f.renderText("Error"))
splits = ["|" + a.center(CMD_WIDTH - 2) + "|" for a in string.split("\n")]

CMD_HEIGHT -= len(splits) + 6

os.system("cls")
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