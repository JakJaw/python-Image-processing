from tkinter import *
from tkinter import messagebox
from collections import Counter
from sklearn.cluster import KMeans
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import cv2


def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))#WTF
    return hex_color


def prep_image(raw_img):
    modified_img = cv2.resize(raw_img, (900, 600), interpolation = cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0]*modified_img.shape[1], 3)
    return modified_img

def color_analysis(img):
    clf = KMeans(n_clusters = 5)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_

    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    plt.figure(figsize = (12, 8))
    plt.pie(counts.values(), color_labels = hex_colors, colors = hex_colors)
    plt.savefig("color_analysis_report.png")
    print(hex_colors)


def extract():
    picture_location = picture_location_entry.get()

    if picture_location == "":
        messagebox.showinfo(title="Error", message="Insert file location")
    else:
        try:
            image = cv2.imread(f"{picture_location}")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(image)
            modified_image = prep_image(image)
            color_analysis(modified_image)

            pass
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No File Found!")
        else:
            pass


window = Tk()
window.title("Image Color Extract Tool")
window.config(padx=50, pady=50)
window.geometry("600x700")

canvas = Canvas(height=350, width=350)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(150, 150, image=logo_img)
canvas.grid(row=0, column=1)

picture_location_label = Label(text="Picture location:").grid(row=1, column=0)
number_of_colors = Label(text="How many colors?").grid(row=2, column=0)

colors_entry = Entry(width=54)
colors_entry.grid(row=2, column=1)

picture_location_entry = Entry(width=54)
picture_location_entry.grid(row=1, column=1)
picture_location_entry.focus()

add_button = Button(text="Extract", width=46, command=extract).grid(row=3, column=1, columnspan=2)
quit_button = Button(text="Quit", command=window.destroy).grid(column=4, row=3)

window.mainloop()
