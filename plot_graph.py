import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#plt.style.use('fivethirtyeigth')

def animate(i):
    data = pd.read_csv('graph.csv')
    x = data['time_list']
    y = data['trend']
    plt.cla()
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.plot(x, y)

ani = FuncAnimation(plt.gcf(), animate, interval= 60000)

plt.tight_layout()
plt.show()