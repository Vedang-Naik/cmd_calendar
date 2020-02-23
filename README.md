# cmd_calendar
cmd_calendar is an attempt to make a calendar system with events and reminders on the command line. It is akin to a very-simplified Google Calendar, Windows Calendar, etc.

## Features: 
1. The calendar of any month or year can be displayed here (Gregorian only, infinitely extended in both directions).
2. Events can be added to any particular day. One can search for events and delete them.

## Usage: 
Start main.py using python. At the calendar> prompt, enter the specific command to do whatever you wish to do. calendar> -h will provide help.

## Plans: 
1. Reminders for events through either email or desktop notifications are planned.
2. A more colourful UI might be implemented.

## Working: 
1. Once main.py starts up, it shows the calendar for the current month and an input prompt.
2. The user enters a argument at the prompt. This is error-checked and parsed by parseCommand()
3. The parsed command is sent to execCommand(), which carries out the user's operation.
    * If command parsing fails, the error will be displayed, followed by the next prompt.
    * If the input is invalid, the error page is shown, followed by the next prompt.
4. Once the operation is done, the prompt is displayed again for the next command.
5. Steps 2-4 continue for ever until the user inputs "exit" or closes the program in some other fashion.
