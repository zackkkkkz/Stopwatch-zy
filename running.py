import webbrowser
import sys
import random
  
# then make a url variable
url = "https://www.google.com"
  
# then call the default open method described above
# webbrowser.open(url, new = 2, autoraise= True)

# with open("stopwatch.py") as f:
#     exec(f.read())

script_descriptor = open("stopwatch_mod2em.py")
a_script = script_descriptor.read()




def random_num(a, b):
    ans = random.randint(a, b)

    return str(ans)


## changing these two number to set range for random seconds of change. 

smt = random_num(0, 9)
# print(smt)


##DO NOT modify the first variable.
##First variable (i) decides the initial time pace (1 = normal, <1 = slower, >1 = faster)

## Second variable (n) decides after every REAL n seconds the pace will change by m

## Third variable (m) decides after every REAL n seconds the pace will change by m
## e.g. if second variable = 4, third variable = 20, it means every 4 real seconds, the clock is slowed by 20 miliseconds
## however, when inputing negative numbers for third variable, make sure it is less than |40|

## putting a positive number = slow down, putting a negative number = speed up

## Fourth variable decides after how many real second, the clock will stop/reset

# sys.argv = ["stopwatch_mod2em.py", "1", '1', "40", "10"] 

exec(a_script)


script_descriptor.close()