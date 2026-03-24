import numpy as np
from torch import angle

def calculate_angle(a,b,c):
    a=np.array(a)           # define point shoulder,elbow, wrist
    b=np.array(b)
    c=np.array(c)

    #calculating the angle of a point relative to its origin
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0],b[0])

    #radian to degree
    angle=np.abs(radians*180.0/np.pi)

    if angle>180.0 :         #the arm position always be in  0-180 degree 
        angle= 360-angle
    return angle

    








