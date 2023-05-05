import tkinter as tk
import time
import math
 
# Height and width of Analog clock window
WIDTH = 400
HEIGHT = 400
 
root = tk.Tk()
root.title("Analog Clock")
 
# Create clock canvas tkinter
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

def update_clock():
    canvas.delete("all")
    now = time.localtime()
    hour = now.tm_hour % 12
    minute = now.tm_min
    second = now.tm_sec
 
    # Draw clock face
    canvas.create_oval(WIDTH, HEIGHT, 4, 4, outline="black", width=2)
     
# Calling the function
update_clock()

root.mainloop()