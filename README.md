# Face-Recognition

I was tasked to build a desktop app using Python that would recognize faces through a webcam and tell that person's name and home district from the database. Also, an admin panel will manually train a person's photo and name, which will be saved in the database.

So here it goes. The task has two Python files. 
1.	Dataload.py (for training the data)
2.	Main.py (for facial recognition)
One additional Python file is there to check the database tables.
myData is the folder to save the trained photos.
## dataload.py
Interface: 
 ![image](https://github.com/akashasmaul/Face-Recognition/assets/98410077/80d6c506-ca26-4ee1-be42-5741dbbe320b)

### Description:
The script uses the Tkinter library to create a GUI application for face recognition. The application will continuously show video frames from the webcam. It has two input fields: one is name, and the other one is district.  When the 'Snapshot' button is clicked, it will take a snapshot, save the cropped face image, and store the name, photo ID, and district in the database. The application will be closed when the 'Quit' button is clicked. 

## main.py 
interface:

 ![image](https://github.com/akashasmaul/Face-Recognition/assets/98410077/b74fd039-ed25-4de9-ab16-5876e6d309ea)

### Description:
The application will continuously show video frames from the webcam. When a face is recognized in the video frames, it will display the name and district of the person. If it does not recognize, then it will show Unknown. The 'Quit' button can be used to close the application.

