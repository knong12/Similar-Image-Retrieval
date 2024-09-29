# Created by Kyler & Kevin
# CSS 484
from contextlib import nullcontext
from tkinter import *
from PIL import Image, ImageTk
import os
import re
import random

# Store the image paths globally alongside thumbnails and labels
image_paths = []

# Function to deselect any selected images
def reset_selection():
    global selected_label
    if selected_label:
        # Remove the inner border by setting highlightthickness to 0
        selected_label.config(bd=0, relief="flat")
        selected_label = None  # Reset the selected label to None

    # Clear the larger image on the right
    selected_image_label.config(image=None)
    selected_image_label.image = None  # Clear the reference to the image


# Function to sort filenames numerically
def sort_numerically(filenames):
    # Extract numbers from filenames and sort based on the numeric part
    return sorted(filenames, key=lambda x: int(re.search(r'\d+', x).group()))

# Function to load images side by side, center them, and display filenames
def load_images():
    image_dir = "images"  # Folder where images are located
    thumbnails = []
    labels = []  # Store references to the image labels for modifying borders
    global image_paths  # Store the image paths here
    row = 0
    col = 0

    # List all image files in the directory
    filenames = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

    # Sort filenames numerically
    filenames = sort_numerically(filenames)

    # Loop through sorted files
    for filename in filenames:
        img_path = os.path.join(image_dir, filename)
        image_paths.append(img_path)  # Store the image path

        # Open and resize the image
        img = Image.open(img_path)
        img.thumbnail((150, 150))  # Resize to thumbnail size (150x150)

        # Convert to ImageTk format for Tkinter display
        img_tk = ImageTk.PhotoImage(img)

        # Store reference to avoid garbage collection
        thumbnails.append(img_tk)

        # Create a label to display the image inside the scrollable frame
        img_label = Label(inner_frame, image=img_tk, bd=0, relief="flat", padx=10, pady=10)
        img_label.grid(row=row, column=col, padx=15, pady=3)  # Adding extra padding to prevent shifting

        # Add a click event to the image label
        img_label.bind("<Button-1>", lambda e, path=img_path, label=img_label: on_image_click(path, label))

        # Store the label reference
        labels.append(img_label)

        # Create a label to display the filename
        filename_label = Label(inner_frame, text=filename, wraplength=150)
        filename_label.grid(row=row + 1, column=col, padx=10, pady=5)

        # Move to the next column (two images per row)
        col += 1
        if col > 1:
            col = 0
            row += 2  # Skip a row to make space for the filenames

    # Make columns and rows expand to center the images and filenames
    for i in range(2):
        inner_frame.grid_columnconfigure(i, weight=1)  # Centering the columns
    for i in range(row + 1):
        inner_frame.grid_rowconfigure(i, weight=1)  # Centering the rows

    return thumbnails, labels

# Function to select a random image
def select_random():
    global selected_label

    # Get a random image label from the labels list
    random_index = random.randint(0, len(labels) - 1)  # Select random index
    random_label = labels[random_index]  # Get the random label
    img_path = image_paths[random_index]  # Get the corresponding image path

    # If there is a currently selected image, remove its border
    if selected_label:
        selected_label.config(bd=0, relief="flat")

    # Set the border for the newly selected image
    random_label.config(bd=4, relief="solid")
    selected_label = random_label  # Update the selected label

    # Display the randomly selected image on the right frame
    img = Image.open(img_path)
    img.thumbnail((400, 400))  # Resize the image to fit
    img_tk = ImageTk.PhotoImage(img)

    # Update the image on the right side
    selected_image_label.config(image=img_tk)
    selected_image_label.image = img_tk  # Keep reference to avoid garbage collection

# Enable scrolling with the mouse wheel
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Handle image click events to populate a larger version of the image on the right
selected_label = None  # To keep track of the currently selected label
def on_image_click(img_path, label):
    global selected_label

    # Remove border from previously selected image
    if selected_label:
        selected_label.config(bd=0, relief="flat")

    # Add border to the newly selected image
    label.config(bd=4, relief="solid")
    selected_label = label  # Set this label as the currently selected one

    # Open the image, resize it to a larger size, and display it on the right frame
    img = Image.open(img_path)
    img.thumbnail((400, 400))  # Resize to a larger size
    img_tk = ImageTk.PhotoImage(img)

    # Update the image on the right side
    selected_image_label.config(image=img_tk)
    selected_image_label.image = img_tk  # Store reference to avoid garbage collection

# Create the window object
window = Tk()
window.geometry("1000x600")
window.title("Image Sort")
window.configure(background="grey")

# Create a frame for the scrollable content (left 20%)
left_frame = Frame(window)
left_frame.pack(side="left", fill="both")

# Create a canvas for the scrollbar
canvas = Canvas(left_frame)
canvas.pack(side="left", fill="both", expand=True)

# Create a scrollbar for the canvas
scrollbar = Scrollbar(left_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Bind the mouse scroll wheel event to the canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Create a frame inside the canvas to hold the content
inner_frame = Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Load images into the scrollable frame
thumbnails, labels = load_images()  # Store references to avoid garbage collection

# Create a frame for the right side content (80%)
right_frame = Frame(window)
right_frame.pack(side="right", fill="both", expand=True)

# Create a label to display the selected image
selected_image_label = Label(right_frame)
selected_image_label.pack(pady=10)

# Create a frame for the buttons and position them at the bottom of the screen
button_frame = Frame(right_frame)
button_frame.pack(side="bottom", pady=10)

# Add the sort and reset buttons to the button frame
sortBtn = Button(button_frame, text="Sort by color-code method", width=25, height=2, bg="light grey")
sortBtn.pack(side="left", padx=5)

resetBtn = Button(button_frame, text="Reset", width=10, height=2, bg="light grey", command=reset_selection)
resetBtn.pack(side="left", padx=5)

randBtn = Button(button_frame, text="Select random image", width=20, height=2, bg="light grey", command=select_random)
randBtn.pack(side="left", padx=5)

# Execute tkinter
window.mainloop()