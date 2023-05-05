import tkinter as tk
import sys

class Application(tk.Frame):

    def __init__(self, window=None):
        super().__init__(window)
        self.window = window
        self.update_time = ''
        self.running = False
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.pack()
        self.create_widgets()
        
        self.delay = 1000  # the time interval (in ms) to update the watch lable, we can manipulate this number to change the pace. 
        if len(sys.argv) > 1:  # take input from the terminal. Give a number < 1000 will make the clock faster, > 1000 will make the clock slower
            self.delay = float(sys.argv[1])  
        

    def create_widgets(self):
        self.stopwatch_label = tk.Label(self, text='00:00:00', font=('ds-digital', 80), background= "black", bd= 60, foreground= "cyan")
        self.stopwatch_label.pack()
        self.start_button = tk.Button(self, text='start', height=5, width=7, font=('Arial', 20), command=self.start)
        self.start_button.pack(side=tk.LEFT)
        self.pause_button = tk.Button(self, text='pause', height=5, width=7, font=('Arial', 20), command=self.pause)
        self.pause_button.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self, text='reset', height=5, width=7, font=('Arial', 20), command=self.reset)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self, text='quit', height=5, width=7, font=('Arial', 20), command=self.window.quit)
        self.quit_button.pack(side=tk.LEFT)
        self.window.title('Stopwatch')

    def start(self):
        if not self.running:
            self.stopwatch_label.after(self.delay)
            self.update2()
            self.running = True

    def pause(self):
        if self.running:
            self.stopwatch_label.after_cancel(self.update_time)
            self.running = False

    def reset(self):
        if self.running:
            self.stopwatch_label.after_cancel(self.update_time)
            self.running = False
        self.hours, self.minutes, self.seconds = 0, 0, 0
        self.stopwatch_label.config(text='00:00:00')

    def update(self):
        self.seconds += 60
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
        hours_string = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        self.stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string )
        self.update_time = self.stopwatch_label.after(self.delay, self.update)

    def update2(self):
        x = int(sys.argv[1])
        self.seconds += x
        if self.seconds >= 60: # we need to update the code in this if block to make it work correctly, which is more complex 
            self.minutes += 1
            print("imsecond: ",self.seconds)
            self.seconds = 0
            print(self.seconds)
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
        hours_string = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        self.stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string )
        self.update_time = self.stopwatch_label.after(1000, self.update2)

root = tk.Tk()
app = Application(window=root)
app.mainloop()