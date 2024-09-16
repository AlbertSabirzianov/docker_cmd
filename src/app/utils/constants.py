"""
Module: constants

This module provides constants related to Docker commands and key codes.
"""
KEY_EXIT = ord('q')
KEY_ESC = 27
KEY_REFRESH = ord('r')
KEY_ENTER = ord("\n")
KEY_SPASE = ord(" ")
KEY_DELETE = ord("d")
KEY_HELP = ord("h")
KEY_SAVE = ord("s")
KEY_EXPORT = ord("e")

INVISIBLE = 0
DOCKER_NOT_INSTALL_TEXT = (
    "Sorry - Docker is not installed or not running...\n"
    "press any key to exit"
)
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


LEFT, RIGHT  -- change tab
UP, DOWN     -- move cursor
SPACE, ENTER -- highlight
d            -- delete
r            -- refresh
q, ESC       -- exit
h            -- help
s            -- save docker image to tar file
e            -- export docker container to tar file
"""

TAR_ARCHIVE_EXTENSION = ".tar"

PLUS = "+"
DASH = "-"
END_OF_LINE = "\n"
SPACE = " "