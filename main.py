import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import face_recognition
import sqlite3
import numpy as np

# Connect to SQLite database
conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()

# Fetch data from the database
c.execute("SELECT * FROM faces")
rows = c.fetchall()

names = []
images = []
districts = []  # Added for storing districts

for row in rows:
    name, photo_id, district = row
    names.append(name)
    images.append(cv2.imread(photo_id))
    districts.append(district)

def encoding1(images):
    encode = []

    for img in images:
        unk_encoding = face_recognition.face_encodings(img)[0]
        encode.append(unk_encoding)
    return encode

encodelist = encoding1(images)

# Initialize the video capture object
cap = cv2.VideoCapture(0)

def update_image():
    '''executed frequently, it updates frame/image on canvas'''

    # read one frame (and "return" status)
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)

    if ret is None:
        print("Can't read from camera")
    else:
        image = Image.fromarray(frame)

        face_locations = face_recognition.face_locations(frame)
        curframe_encoding = face_recognition.face_encodings(frame1, face_locations)

        for encodeface, facelocation in zip(curframe_encoding, face_locations):
            results = face_recognition.compare_faces(encodelist, encodeface)
            distance = face_recognition.face_distance(encodelist, encodeface)
            match_index = np.argmin(distance)

            # Set a threshold for the face distance
            threshold = 0.6
            if distance[match_index] < threshold:
                name = names[match_index]
                district = districts[match_index]  # Retrieve district based on index
            else:
                name = "Unknown"
                district = ""

            top, right, bottom, left = facelocation

            draw = ImageDraw.Draw(image)
            draw.rectangle([left, top, right, bottom], outline="green")
            draw.text((left, top), f"{name}, {district}", font=myFont, fill=(255, 0, 0))  # Display both name and district

        photo.paste(image)

    root.after(10, update_image)

def quitapp():
    cap.release()  # Release the camera
    root.destroy()  # Destroy the window
    conn.close()  # Close the database connection

# Create the main Tkinter window
root = Tk()

myFont = ImageFont.truetype('arial.ttf', 30)

image = Image.fromarray(np.zeros((500, 500, 3), dtype=np.uint8))
photo = ImageTk.PhotoImage(image)

canvas = tk.Canvas(root, width=photo.width(), height=photo.height())
canvas.pack(fill='both', expand=True)

canvas.create_image((0, 0), image=photo, anchor='nw')

button_quit = tk.Button(root, text="Quit", command=quitapp)
button_quit.pack(side='left')

update_image()

root.mainloop()

# ---

# close stream
cap.release()
