import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


plt.style.use('fivethirtyeight')

x_vals = np.zeros(30)
y_vals = np.zeros(30)

def update_plot(xval, yval):
    global x_vals
    x_vals = np.delete(x_vals, 0, 0)
    global y_vals
    y_vals = np.delete(y_vals, 0, 0)
    x_vals = np.append(x_vals,xval)
    y_vals = np.append(y_vals,yval)
    plt.cla()
    plt.plot(x_vals, y_vals)
    print(x_vals)
    print(y_vals)

#ani = FuncAnimation(plt.gcf(), update_plot(1,2), interval=1000)
#This goes in the button signal function ^^^^^^
plt.tight_layout()
plt.show()
