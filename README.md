# docker_cmd
A console application for convenient viewing and interaction with Docker objects (images, containers, and volumes).
# How to Run
Download the repository:
```commandline
https://github.com/AlbertSabirzianov/docker_cmd.git
```
If you are using Windows, you need to install windows-curses. There are no dependencies for Linux:
```commandline
pip install windows-curses
```
Go to the src folder:
```commandline
cd docker_cmd/src
```
Run the application:
```commandline
python3 main.py
```
# Instructions
The utility allows you to view, highlight, and delete one or several Docker objects (images, containers, or volumes) at once. There is also functionality for saving Docker objects to an archive. The keys used are:
```text
LEFT, RIGHT  -- switch tab (there are 3 tabs in total - images, containers, and volumes)
UP, DOWN     -- move the cursor
SPACE, ENTER -- select the chosen object
d            -- delete: if no objects are selected - the object on which the cursor is located is deleted, otherwise all selected objects are deleted
r            -- refresh
q, ESC       -- exit
h            -- message with all available commands
s            -- save the selected object to a tar archive: if no objects are selected - the object on which the cursor is located is saved, otherwise all selected objects are saved
i            -- inspect the selected images or containers in json file: if no objects are selected - the object on which the cursor is located is saved, otherwise all selected objects are inspected
```


