import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def add_image(filename, index=None):
    if index is None:
        images.append(filename)
    else:
        images.insert(index, filename)

def delete_images(filename):
    if filename in images:
        images.remove(filename)

def load_images_from_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Add more extensions if needed
            add_image(os.path.join(folder, filename))

def on_open():
    filepath = filedialog.askopenfilename(filetypes=[("IMP Files", "*.imp")])
    if filepath:
        # Clear current images list before loading the new one
        images.clear()
        with open(filepath, "r") as file:
            paths = file.readlines()
            for path in paths:
                add_image(path.strip())
        show_image(current_index)  # Show the first image from the loaded list

def on_save():
    filepath = filedialog.asksaveasfilename(defaultextension=".imp", filetypes=[("IMP Files", "*.imp")])
    if filepath:
        with open(filepath, "w") as file:
            for image in images:
                file.write(image + "\n")

def on_exit():
    root.quit()

def show_image(index):
    if 0 <= index < len(images):
        # Open and resize the image to fit within 600x600
        image = Image.open(images[index])
        image = image.resize((600, 600), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)
        
        label.config(image=image)
        label.image = image  # Keep a reference to prevent garbage collection
        index_label.config(text=f"Image {index + 1} of {len(images)}")

def next_image():
    global current_index
    if current_index < len(images) - 1:
        current_index += 1
        show_image(current_index)

def prev_image():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_image(current_index)

if __name__ == '__main__':
    images = []  # Initially empty list
    folder = 'images/'  # Folder where images are stored
    # Initially do not load any images, leave empty
    print(images)
    
    root = tk.Tk()
    root.geometry("800x800")
    root.title("Image Viewer")

    current_index = 0  # Start at the first image (but no images are loaded initially)

    # Create a frame to hold the image and buttons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Label to display the image
    label = tk.Label(frame)
    label.pack()

    # Label to show current image index
    index_label = tk.Label(root, text="No image loaded")
    index_label.pack()

    # Create the buttons frame at the bottom
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(side="bottom", pady=20)

    # Back button
    back_button = tk.Button(buttons_frame, text="Back", command=prev_image)
    back_button.pack(side="left", padx=10)

    # Next button
    next_button = tk.Button(buttons_frame, text="Next", command=next_image)
    next_button.pack(side="right", padx=10)

    # Main menu
    main_menu = tk.Menu(root)
    file_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Open", command=on_open)
    file_menu.add_command(label="Save", command=on_save)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_exit)
    main_menu.add_cascade(label="File", menu=file_menu)
    root.config(menu=main_menu)

    # Don't show any images until a file is opened
    root.mainloop()
