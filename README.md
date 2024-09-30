# docker_cmd
A console application for convenient viewing and interaction with Docker objects (images, containers, and volumes).
# How to Run
Download the repository:
```commandline
git clone https://github.com/AlbertSabirzianov/docker_cmd.git
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
# How to use
Immediately after launching the application, you will see a menu where all the docker images installed on your device are displayed
<br/>![docker images menu](images/main_menu.png)<br/>
By pressing the right and left keys, you can easily switch between tabs with docker containers and volumes (there are three tabs in total images, volumes and containers).
Use the forward and backward keys to move the cursor. To select one or more objects, use the space bar or enter keys, after which the selected objects will look like in the picture below.
<br/>![selected objects](images/underlined.png)<br/>
You can use the following keys to interact with selected objects:
- __d__ (*delete*)
delete all selected objects, if no objects are selected - the object on which the cursor is located is deleted.
- __r__  (*refresh*) all information about docker objects will be updated and all selected objects will become unselected.
- __s__ (*save*) save all selected objects in tar archive, if no objects are selected - the object on which the cursor is located is saved.
- **h** (*help*) show help message with all available commands
- **q, ESC** (*quit*) exit from help message (or from application)
- **n** (*rename*) rename the object on which the cursor is located. Then you press this key you will see window like on the image bellow
 <br/> ![rename](images/type_new_name.png)<br/>
  you see a prompt to enter a new name for the selected object, after you enter the desired name and press Enter, the object will be renamed. To exit the new name input mode, press  **ESC** or **cntl + C**.</b>
- **i** (*inspect*) see the inspect information about image or container on which the cursor is located. To exit press **ESC** or **q**.
  <br/>![inspect](images/inspect.png)<br/>
  
- **p** (*pull*) switch to image search mode on dockerhub. after switching to this mode, you will see a prompt to enter the image name.
  <br/>![search](images/start_type.png)<br/>
   
  when you start entering the name of the desired image, the available images on dockerhub for download will begin to appear below. By pressing the right and left keys, you can go to the next/previous page. The current page and their number can be seen at the bottom of the screen.To exit press **ESC** or **cntl + C**.
  <br/>![result search](images/find_image.png)<br/>
  
  If you press the **space** bar you will be able to see detailed information about the image on which the cursor is located.To exit press **ESC** or **q**
  <br/>![image info](images/image_information.png)<br/>
  To select the found image, press **Enter**, after which you will switch to the search mode for the desired tag.To exit press **ESC** or **cntl + C**
  <br/>![find tag](images/find_tag.png)<br/>

If you press the **space** bar you will be able to see detailed information about the tag on which the cursor is located.To exit press **ESC** or **q**.
<br/>![tag info](images/tag_information.png)<br/>
If you just want pull the latest image you can press **l** and latest image will be pulled on your device.To select the found tag, press **Enter**, after which image with selected tag will be pulled on your device.To exit press **ESC** or **q**.




