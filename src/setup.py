import pandas as pd
import numpy as np
import os

path = os.path.abspath("..") + "/data/"

#create two panels
upright = pd.Panel()
sitting = pd.Panel()

#initialise the panel with the first data frame as zeros
temp = np.zeros([9,2,1])
upright = pd.Panel(temp,items=xrange(0,9,1),major_axis=['x','y'],minor_axis=xrange(0,1,1))
sitting = pd.Panel(temp,items=xrange(0,9,1),major_axis=['x','y'],minor_axis=xrange(0,1,1))

#save them to files
upright.to_pickle(path+'upright.pkl')
sitting.to_pickle(path+'sitting.pkl')

print "done"