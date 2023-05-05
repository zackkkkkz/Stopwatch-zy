import tkinter as tk
import sys
import csv
import pandas as pd
from datetime import datetime
import time

class Application(tk.Frame):

    def __init__(self, window=None):
        super().__init__(window)
        self.window = window
        self.pack()
        # self.base_pace = 0 #this is the variable we can use to modify the pace of time. 
        # 1 = real time, less than 1 = slow down, more than 1 = speed up
        # if self.base_pace == 0:
        
        self.config_df = self.read_config("config.csv")
        # print(self.config_df)

        self.output_df = self.config_df.copy()


        self.output_df.insert(4, "keypress_timestamp", "NAN")
        self.output_df.insert(5, "pace_at_keypress", "NAN")

        # self.test = 'something'
        # self.output_df = self.config_df.copy()
        # self.output_df.insert(4, "keypress_timestamp", self.elapsed)
        # self.output_df.insert(5, "pace_at_keypress", "NAN")
        # print(self.output_df.head())

        self.trial_num = 0
        self.base_pace = 0
        self.pace_at_keypress = 0
        self.frequency_of_change = 0
        self.add_increment = 0

        self.start_time = 0

        self.elapsed = 0

        self.stop_time = 0
           
        self.pace_update = False

        self.running = False
       
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0

        self.prev_sec = 0
        
        self.passed = 0 
        self.until = 0
        
        self.stop = ''
        self.cancel = ''
        self.stop_timer = ''
        self.first_time_flag = True
        
        self.create_widgets()
        
        self.update_trial(0)
        # print(self.trial_num)

    def read_config(self, file_name):
        df = pd.read_csv (file_name)
        df.reset_index()
        df = df.set_index("trial_num")
        return df

    def write_output(self): 
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        file_name = 'OUTPUT_' + current_time + '.csv'


        self.output_df.to_csv(file_name)

    def create_widgets(self):
        self.stopwatch_label = tk.Label(self, text='00:00:00:00', font=("Arial", 85), background= "black", bd = 10, width= 11, foreground= "cyan", anchor=tk.CENTER)
        self.stopwatch_label.grid(row = 0, column = 0, columnspan = 9)
        self.start_button = tk.Button(self, text='Start', height=4, width=15, font=('Arial', 20), command=self.start)
        self.start_button.grid(row = 1, column = 0, columnspan = 3)
        self.pause_button = tk.Button(self, text='CHANGE', height=4, width=30, font=('Arial', 20), background="red", foreground="red", command=self.pause)
        self.pause_button.grid(row = 1, column = 3, columnspan = 6)
        
        self.trial_num_label = tk.Label(self, text='Trial' + str(self.trial_num), font=("Arial", 10), bd = 10, width= 11, anchor=tk.CENTER)
        self.trial_num_label.grid(row = 2, column = 0)
        self.done_button = tk.Button(self, text='DONE', height=2, width=7, font=('Arial', 10), fg="red", command=self.write_output)
        self.done_button.grid(row = 2, column = 5)
        self.prev_trial_button = tk.Button(self, text='< Prev', height=2, width=7, font=('Arial', 10), fg="gray", command=self.prev)
        self.prev_trial_button.grid(row = 2, column = 7)
        self.next_trial_button = tk.Button(self, text='Next >', height=2, width=7, font=('Arial', 10), fg="gray", command=self.next)
        self.next_trial_button.grid(row = 2, column = 8)
        #self.reset_button = tk.Button(self, text='Reset', height=5, width=7, font=('Arial', 20), command=self.reset)
        #self.reset_button.pack(side=tk.LEFT)
        #self.quit_button = tk.Button(self, text='Quit', height=5, width=7, font=('Arial', 20), command=self.window.quit)
        #self.quit_button.pack(side=tk.LEFT)
        self.window.title('Stopwatch')

    def start(self):
        if not self.running:
            self.stopwatch_label.after(self.update_time)
            self.update()
            self.stop_after()
            self.running = True
            self.start_time = time.time()

    def pause(self):
        if self.running:
            self.stopwatch_label.after_cancel(self.cancel)
            self.running = False
        stop = time.time()
        self.elapsed = stop - self.start_time
        self.elapsed = round(self.elapsed, 3)
        pace = 1/(self.update_time/40) 
        self.pace_at_keypress = pace
        
        # print("trial num after pause: ",self.trial_num)
        # print(self.output_df)
        # # print(self.output_df.index[1])
        # print(self.elapsed)
        self.output_df.at[self.trial_num+1, "keypress_timestamp"] = self.elapsed
        self.output_df.at[self.trial_num+1, "pace_at_keypress"] = self.pace_at_keypress
        # # # print('current pace',pace)
        # print(self.output_df)

        # print("-------")

    def reset(self):
        if self.running:
            self.stopwatch_label.after_cancel(self.cancel)
            self.running = False
        
        hours_string = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        millisecond_string ="{:03d}".format(self.milliseconds)[:3]
        # print("\n","final time: ", hours_string + ":", minutes_string + ":" + seconds_string + ":" + millisecond_string, "\n")
        self.hours, self.minutes, self.seconds, self.milliseconds = 0, 0, 0, 0
        self.stopwatch_label.config(text='00:00:00:00')
        pace = 1/(self.update_time/40) 
        self.pace_at_keypress = pace
        # print("initial base pace: ", self.base_pace, "\n")
        # print("after", self.frequency_of_change, "seconds, time pace will change", "\n")
        # print("at ", f"{pace:.3f}", "times of the initial pace, the participants realized time change")
        self.update_time = int(40/self.base_pace)
        self.stopwatch_label.after_cancel(self.stop_timer)
        self.prev_sec = 0
        # print("current update time: ", self.update_time)

    def next(self): 
        self.reset()
        self.update_trial(self.trial_num + 1)

    def prev(self): 
        self.reset()
        self.update_trial(self.trial_num - 1) 

    def update_trial(self, trial_num): 
        # print('updating to trial', trial_num)
        # need to add checks for number of trials so this doesn't break when you get to the end
        # self.trial_num = trial_num
        # print("current trial: ", self.trial_num)
        # print("indexing: ",self.config_df.index)
        if trial_num < 0:
            # print("prev test")
            trial_num = self.config_df.index[-1] - 1
            
        
        if trial_num > self.config_df.index[-1] - 1:
            # print("next test", trial_num)
            trial_num = self.config_df.index[0] - 1
            # print(trial_num)
        #     print("i am config\n",self.config_df[trial_num])
        #     print("I am trialnum, ",self.trial_num)
        # print("im self: ", self.trial_num)
        # print('trial info\n',self.config_df.loc[trial_num])
        self.trial_num = trial_num

        self.base_pace = self.config_df.iloc[trial_num]['base_pace']
        # print("working")
        self.update_time = int(40/self.base_pace)
        # print("working2222")
        self.frequency_of_change = self.config_df.iloc[trial_num]['frequency_of_change']
        self.add_increment = self.config_df.iloc[trial_num]['add_increment']
        self.stop_time = self.config_df.iloc[trial_num]['stop_time']
        # self.elapsed = self.config_df.iloc[trial_num]['keypress_timestamp']

        # print(str(self.trial_num))

        self.trial_num_label.config(text='Trial' + str(self.trial_num + 1))
        # print(self.trial_num_label.cget('text'))

    def update(self):
        self.milliseconds += 40
        if self.milliseconds >= 1000:
            self.seconds += 1
            self.milliseconds = 0
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
        hours_string = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
        minutes_string = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        seconds_string = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        # print(self.milliseconds)

        # self.milliseconds = round(self.milliseconds, 2)
        # print(str(self.milliseconds).zfill(2))
 
        millisecond_string ="{:02d}".format(self.milliseconds)[:2]
  
        if self.seconds % int(self.frequency_of_change) == 0 and self.seconds != self.prev_sec:
            self.update_time = int(self.update_time + float(self.add_increment))
            # print("update time after change: ", self.update_time)
            self.prev_sec = self.seconds
            # print('update time:')
            # print(self.update_time)
            if self.update_time <= 0:
                self.update_time = 1
            
      
        # millisecond_string = f'{self.milliseconds}' #if self.seconds > 9 else f'0{self.milliseconds}'
        self.stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string + ':' + millisecond_string )
        self.cancel = self.stopwatch_label.after(self.update_time, self.update)
        # self.stop = self.stopwatch_label.after((int(self.stop_time) * 1000), self.pause)
        # print(int(self.stop_time))
        # test = self.stopwatch_label.after(5000, self.pase_update)
        # if self.seconds // 10 == 0:
        #    self.update_time = int(self.update_time/1.5 )
    
    def stop_after(self):
        # print("i am running")
        # print(int(self.stop_time))
        self.stop_timer = self.stopwatch_label.after((int(self.stop_time) * 1000), self.reset)



        
        

root = tk.Tk()
# root.geometry("400x400")
root.resizable(0,0)
app = Application(window=root)
app.mainloop()
