from tkinter import *
from time import strftime
from datetime import datetime, time

root = Tk()
root.geometry("500x500")
root.resizable(0,0)
root.title('Python Clock')



mark = Label(root,
            font = ('calibri', 40, 'bold'),
            pady=150,
            foreground = 'black')
# dt = datetime.today()  
dt = datetime.strptime("09/19/22 00:00:00:00", '%m/%d/%y %H:%M:%S:%f')

print(dt)
seconds = int(dt.timestamp())
# start = int(dt.timestamp()) 
print(seconds)
test = datetime.fromtimestamp(seconds)
print(test)
timer = 0


def time():
    # realTime = strftime('%H:%M:%S')
    
    # fakeTime = realTime
    # string = fakeTime.split(":")
    # print(string)
    # hour = string[0]
    # minute = string[1]
    # second = string[2]

	# Get timezone naive now
	global seconds
	# global start
	seconds += 1
	# watch = seconds - start
	display_time = datetime.fromtimestamp(seconds).strftime("%H:%M:%S:%f")
	# delta = seconds - start
	# display_timer = datetime.fromtimestamp(delta).strftime("%H:%M:%S")
    
	mark.config(text = display_time)
	mark.after(500, time)




mark.pack(anchor = 'center')
time()

mainloop()