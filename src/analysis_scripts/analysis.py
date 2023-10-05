import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bag = bagreader('/home/ubuntuzzd/stationary_data.bag')
bag.topic_table

msg_data = bag.message_by_topic('/gps_out')

data = pd.read_csv(msg_data)

utm_east = np.array(data['utm_easting']-data['utm_easting'].min())
utm_north = np.array(data['utm_northing']-data['utm_northing'].min())
plt.scatter(utm_east,utm_north, marker='o',s=3,color='blue')
plt.xlabel('utm_easting')
plt.ylabel('utm_northing')
plt.show()