"""
Module: constants

This module provides constants related to Docker commands and key codes.
"""
import curses

from ..utils.enams import Steps

KEY_EXIT = ord('q')
KEY_ESC = 27
KEY_REFRESH = ord('r')
KEY_ENTER = ord("\n")
KEY_SPASE = ord(" ")
KEY_DELETE = ord("d")
KEY_HELP = ord("h")
KEY_SAVE = ord("s")
KEY_INSPECT = ord("i")
KEY_RENAME = ord("n")
KEY_PULL = ord('p')
KEY_LATEST = ord('l')

INVISIBLE = 0
START_PAGE_NUMBER = 1
PAGE_SIZE = 100
NO_PAGES = "0/0"
DOCKER_NOT_INSTALL_TEXT = (
    "Sorry - Docker is not installed or not running...\n"
    "press any key to exit"
)
INTERNET_TROUBLE_TEXT = "Sorry internet connection closed..."
DOCKER_API_TROUBLE_TEXT = "Sorry somthing wrong with Docker Api..."
MAKE_FULL_SCREEN_TEXT = "make the terminal full screen, please"
ICON = """
                    ##        .
              ## ## ##       ==
           ## ## ## ##      ===
       /\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\___/ ===
  ~~~ ~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
       \______ o          __/
         \    \        __/
          \____\______/
"""
HELP_TEXT = """


LEFT, RIGHT  -- switch tab (there are 3 tabs in total - images, containers, and volumes)
UP, DOWN     -- move the cursor
SPACE, ENTER -- select the chosen object
d            -- delete 
r            -- refresh
q, ESC       -- exit
h            -- message with all available commands
s            -- save 
i            -- inspect information of the selected image or container
n            -- rename the selected object
p            -- go to pull mode
l            -- pull the latest selected image
SPACE        -- in pull mode get information about image or tag
"""
START_TYPE_NAME = "Start Type New Name..."

PLUS = "+"
DASH = "-"
END_OF_LINE = "\n"
SPACE: str = " "
EMPTY_STRING = ""
UNDERSCORE = "_"
CURS = ">"
SLASH = '/'
COLON = ':'
LIBRARY = "library"
LATEST = "latest"


KEY_STEPS_DICT: dict[int, Steps] = {
    curses.KEY_DOWN: Steps.STEP_DOWN,
    curses.KEY_UP: Steps.STEP_UP
}
