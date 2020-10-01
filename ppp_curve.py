#importing all necessary libraries and modules

import matplotlib.pyplot as plt
import json
import math
import os
import pandas as pd
import numpy as np

sample = 'Sample1'

pdr_points = []     #empty list for predator co-ordinations

pr_points = []      #empty list for prey co-ordinations

myJSONS = [file for file in os.listdir('E:\\PredatorPray\\'+sample+'\\JSON_Files')]     #taking JSON files in a list of a particular sample




##fetching co-ordintations of predator and prey to their corresponding lists

for file in myJSONS:
    myJSON = json.loads(open(os.path.join('E:\\PredatorPray\\'+sample+'\\JSON_Files',file),'r').read())     #reading JSON files of a particular sample
    
    predator=[(myJSON['shapes'][0]['points'][0][0]+myJSON['shapes'][0]['points'][1][0])/2,
                (myJSON['shapes'][0]['points'][0][1]+myJSON['shapes'][0]['points'][1][1])/2]        #fetching predator co-ordinations and finding the center point
    
    prey=[(myJSON['shapes'][1]['points'][0][0]+myJSON['shapes'][1]['points'][1][0])/2,
                (myJSON['shapes'][1]['points'][0][1]+myJSON['shapes'][1]['points'][1][1])/2]        #fetching prey co-ordinations and finding the center point


    #getting the lists filled with available co-ordinates
    
    pdr_points.append(predator)
    pr_points.append(prey)


pdr_x = [pdr_points[x][0] for x in range(len(pdr_points))]      #getting a seperate list for predator X co-ordination for center point
pdr_y = [pdr_points[y][1] for y in range(len(pdr_points))]      #getting a seperate list for predator Y co-ordination for center point

pr_x = [pr_points[x][0] for x in range(len(pr_points))]         #getting a seperate list for prey X co-ordination for center point
pr_y = [pr_points[y][1] for y in range(len(pr_points))]         #getting a seperate list for prey Y co-ordination for center point


def distance(lst_x,lst_y):
    distance_list = [math.sqrt((lst_x[i+1]-lst_x[i])**2+(lst_y[i+1]-lst_y[i])**2) for i in range(len(lst_x)-1)]
    return distance_list

def distance_between_objects(lst_x1, lst_y1, lst_x2, lst_y2):
    distance_list = [abs(abs(lst_x2[i]-lst_x1[i])-abs(lst_y2[i]-lst_y1[i])) for i in range (len(lst_x1)-1)]
    return distance_list


distances_pdr = distance(pdr_x,pdr_y)
distances_pr = distance(pr_x,pr_y)
print('Distances of Predator : ',distances_pdr)
print()
print('Distances of Prey : ',distances_pr)
print()

def velocity(lst):
    prev_velocity = 0
    time = .3
    post_velocity = []
    distance_list = lst
    for i in range(len(distance_list)):
##      V = prev_velocity+((2*distance_list[i])/time)
        V = distance_list[i]/time
        post_velocity.append(V)
        prev_velocity = V
    return post_velocity

def acceleartion(lst):
    prev_velocity = 0
    time = .3
    post_velocity = lst
    acceleration = []
    for i in range(len(post_velocity)):
        A = (post_velocity[i]-prev_velocity)/time
        acceleration.append(A)
        prev_velocity = post_velocity[i]
    return acceleration

velocities_pdr = velocity(distances_pdr)
print('Velocities of Predator : ',velocities_pdr)
print()
accelerations_pdr = acceleartion(velocities_pdr)
print('Accelerations of Predator : ',accelerations_pdr)
print()
velocities_pr = velocity(distances_pr)
print('Velocities of Prey : ',velocities_pr)
print()
accelerations_pr = acceleartion(velocities_pr)
print('Accelerations of Prey : ',accelerations_pr)
print()

T = [(i+1)/3 for i in range(len(accelerations_pdr))]
#T = [(i+1) for i in range(34)]
print(T)

##poly = np.polyfit(T,velocities_pdr,43)
##poly_eqn = np.poly1d(poly)
##print(np.polyval(poly,[0.3333333333333333,0.6666666666666666, 1.0]))

from scipy.interpolate import interp1d

f_pdr = interp1d(T,velocities_pdr,kind='linear',fill_value="extrapolate")
f_pr = interp1d(T,velocities_pr,kind='linear',fill_value="extrapolate")
newT_pdr =  np.linspace(0.3,14.5,num=60,endpoint=True)
newT_pr =  np.linspace(0.3,14.5,num=60,endpoint=True)

##plt.plot(newT_pdr,f_pdr(newT_pdr),marker='o')
##plt.plot(newT_pr,f_pr(newT_pr),marker='o')


##plt.show()

window_size = 10
##
numbers_series_pdr = pd.Series(f_pdr(newT_pdr))
numbers_series_pr = pd.Series(f_pr(newT_pr))
windows_pdr = numbers_series_pdr.rolling(window_size)
windows_pr = numbers_series_pr.rolling(window_size)
moving_averages_pdr = windows_pdr.mean()
moving_averages_pr = windows_pr.mean()
##
##
moving_averages_list_pdr = moving_averages_pdr.tolist()
moving_averages_list_pr = moving_averages_pr.tolist()
without_nans_pdr = moving_averages_list_pdr[window_size - 1:]
without_nans_pr = moving_averages_list_pr[window_size - 1:]
###print(without_nans)
##
distance_between_object = distance_between_objects(pdr_x,pdr_y,pr_x,pr_y)
##
##distance_between_object_series = pd.Series(distance_between_object)
##windows_distance = distance_between_object_series.rolling(window_size)
##moving_average_object_distance = windows_distance.mean()
##
##moving_distance_list = moving_average_object_distance.tolist()
##without_nans_distance = moving_distance_list[window_size -1:]

newT_pdr = newT_pdr[:len(without_nans_pdr)]
newT_pr = newT_pr[:len(without_nans_pr)]

##plt.figure(1)
plt.plot(newT_pdr,without_nans_pdr, marker='o', label = 'Predator Speed')
plt.plot(newT_pr,without_nans_pr,marker='o', label = 'Prey Speed')
#plt.plot(T,velocities_pdr, marker='o', label = 'Predator Speed')
##plt.plot(T,velocities_pr,marker='o', label = 'Prey Speed')
##plt.xlabel('time(t)')
##plt.ylabel('velocity(v)')
##plt.legend()
##
##plt.figure(2)
#plt.plot(T,without_nans_distance,marker='o', label = 'Distances Between Predator & Prey')
##plt.plot(T,distance_between_object,marker='o', label = 'Distances Between Predator & Prey')
##plt.xlabel('time(t)')
##plt.ylabel('Distance(d)')
##plt.legend()
##
plt.grid(b=True, which='major', color='#666666', linestyle='-')
##
plt.show()

