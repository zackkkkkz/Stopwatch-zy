import tkinter as tk
import sys
import pandas as pd

class Application(tk.Frame):

    def __init__(self, window=None):
        super().__init__(window)
        self.window = window
        self.pack()
        # self.alpha = 0 #this is the variable we can use to modify the pace of time. 
        # 1 = real time, less than 1 = slow down, more than 1 = speed up
        # if self.alpha == 0:
        self.alpha = float(sys.argv[1])
           

        self.update_time = int(40/self.alpha)
        self.pace_update = False

        self.running = False
       
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.miliseconds = 0

        self.prev_sec = 0
        
        #indexing for participants
        self.count = 0 
        #index for different trials 
        self.trial = 0
        
        
        self.stop = ''
        self.cancle = ''
        self.first_time_flag = True
        self.create_widgets()
  
        
    

    def create_widgets(self):
        self.stopwatch_label = tk.Label(self, text='00:00:00:00', font=("Arial", 55), background= "black", bd = 10, width= 11, foreground= "cyan", anchor=tk.CENTER)
        self.stopwatch_label.pack()
        self.start_button = tk.Button(self, text='Start', height=5, width=7, font=('Arial', 20), command=self.start)
        self.start_button.pack(side=tk.LEFT)
        self.pause_button = tk.Button(self, text='Pause', height=5, width=7, font=('Arial', 20), command=self.pause)
        self.pause_button.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self, text='Reset', height=5, width=7, font=('Arial', 20), command=self.reset)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self, text='Quit', height=5, width=7, font=('Arial', 20), command=self.window.quit)
        self.quit_button.pack(side=tk.LEFT)
        self.window.title('Stopwatch')

    def start(self):
        if not self.running:
            self.stopwatch_label.after(self.update_time)
            self.update()
            self.stop_after()
            self.count += 1
            self.running = True

    def pause(self):
        if self.running:
            self.stopwatch_label.after_cancel(self.cancle)
            self.running = False

    def reset(self):
        if self.running:
            self.stopwatch_label.after_cancel(self.cancle)
            self.running = False
        
        hours_string = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        milisecond_string ="{:03d}".format(self.miliseconds)[:3]
        print("\n","final time: ", hours_string + ":", minutes_string + ":" + seconds_string + ":" + milisecond_string, "\n")
        self.hours, self.minutes, self.seconds, self.miliseconds = 0, 0, 0, 0
        self.stopwatch_label.config(text='00:00:00:00')
        pace = 1/(self.update_time/40) 
        print("initial base pace: ", sys.argv[1], "\n")
        print("after", sys.argv[2], "seconds, time pace will change", "\n")
        print("at ", f"{pace:.3f}", "times of the initial pace, the participants realized time change")
        self.update_time = int(40/self.alpha)
        self.prev_sec = 0
        # print("current update time: ", self.update_time)




    def update(self):
        self.miliseconds += 40
        if self.miliseconds >= 1000:
            self.seconds += 1
            self.miliseconds = 0
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
        hours_string = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        # print(self.miliseconds)

        # self.miliseconds = round(self.miliseconds, 2)
        # print(str(self.miliseconds).zfill(2))
 
        milisecond_string ="{:02d}".format(self.miliseconds)[:2]
  
        if self.seconds % int(sys.argv[2]) == 0 and self.seconds != self.prev_sec:
            self.update_time = int(self.update_time + float(sys.argv[3]))
            # print("update time after change: ", self.update_time)
            self.prev_sec = self.seconds
            if self.update_time <= 0:
                self.update_time = 1
            
      
        # milisecond_string = f'{self.miliseconds}' #if self.seconds > 9 else f'0{self.miliseconds}'
        self.stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string + ':' + milisecond_string )
        self.cancle = self.stopwatch_label.after(self.update_time, self.update)
        # self.stop = self.stopwatch_label.after((int(sys.argv[4]) * 1000), self.pause)
        # print(int(sys.argv[4]))
        # test = self.stopwatch_label.after(5000, self.pase_update)
        # if self.seconds // 10 == 0:
        #    self.update_time = int(self.update_time/1.5 )
    
    def stop_after(self):
        print("i am running")
        print(int(sys.argv[4]))
        self.stopwatch_label.after((int(sys.argv[4]) * 1000), self.reset)

    def export_tocsv(self):
        print('testing')
        df = pd.DataFrame()

    
    # def pase_update(self):
    #     # if not self.pace_update:
    #     #     self.update_time = int(self.update_time//1.5)
    #     #     self.pace_update = True
    #     self.update_time = int(self.update_time//1.5)
        
        

root = tk.Tk()
# root.geometry("400x400")
root.resizable(0,0)
app = Application(window=root)
app.mainloop()