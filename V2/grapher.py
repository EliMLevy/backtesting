# importing the required module
import matplotlib.pyplot as plt
import math
import numpy as np
import datetime
import pandas as pd

def graph_this_please(start_time, end_time, y_vals, output_name):
    x = np.array(pd.date_range(start=start_time,end=end_time))
    length = min(len(y_vals), len(x))
    plt.plot(x[:length], y_vals[:length])
    
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')

    plt.title(output_name)

    plt.savefig(output_name + '.png')
    plt.clf()
