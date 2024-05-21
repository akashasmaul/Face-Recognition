from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import face_recognition
import sqlite3

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Connect to SQLite database
conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS faces
             (name TEXT, photo_id TEXT, district TEXT)''')

# Function to take a snapshot and save it
def snapshot():
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    face_locations = face_recognition.face_locations(cv2image)
    for face_location in face_locations:
        top, right, bottom, left = face_location
        # Crop the face from the image
        im1 = img.crop((left, top, right, bottom))
        name = name_var.get()
        district = district_var.get()  # Get home district
        photo_id = 'myData/' + name + '.jpg'
        # Save the cropped face with the given name
        im1.save(photo_id)
        # Insert data into database
        c.execute("INSERT INTO faces VALUES (?, ?, ?)", (name, photo_id, district))
        conn.commit()

# Function to continuously show frames from the camera
def show_frames():
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(10, show_frames)  # Repeat after an interval

# Function to quit the application
def quitapp():
    cap.release()  # Release the camera
    win.destroy()  # Destroy the window
    conn.close()  # Close the database connection

# Create the main Tkinter window
win = Tk()
name_var = StringVar()
district_var = StringVar()  # Variable for home district

# Create a Label to display the video frames
label = Label(win)
label.grid(row=0, column=0, columnspan=2)  # Span across two columns

# Label for entering the name
name_label = Label(win, text="Name", font=('calibre', 10, 'normal'))
name_label.grid(row=1, column=0)

# Label for entering the home district
district_label = Label(win, text="Home District", font=('calibre', 10, 'normal'))
district_label.grid(row=2, column=0)

# Entry for entering the name
name_entry = Entry(win, textvariable=name_var, font=('calibre', 10, 'normal'))
name_entry.grid(row=1, column=1)

# Entry for entering the home district
district_entry = Entry(win, textvariable=district_var, font=('calibre', 10, 'normal'))
district_entry.grid(row=2, column=1)

# Button to take a snapshot
snap_btn = Button(win, text='Snapshot', command=snapshot)
snap_btn.grid(row=3, column=0, columnspan=2)  # Span across two columns

# Button to quit the application
quit_btn = Button(win, text='Quit', command=quitapp)
quit_btn.grid(row=4, column=0, columnspan=2)  # Span across two columns

# Show the video frames
show_frames()

# Start the Tkinter event loop
win.mainloop()
