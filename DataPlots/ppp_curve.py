#importing all necessary libraries and modules

from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import jsonReader as jr
import functions as fn
import movingAvgFilter as maf

time = 0.5
timeSpliter = 2

pdr_points = jr.pdr_points
pr_points = jr.pr_points

pdr_x = [fn.pixelToCm(pdr_points[x][0],96) for x in range(len(pdr_points))]      #getting a seperate list for predator X co-ordination for center point
pdr_y = [fn.pixelToCm(pdr_points[y][1],96) for y in range(len(pdr_points))]      #getting a seperate list for predator Y co-ordination for center point

pr_x = [fn.pixelToCm(pr_points[x][0],96) for x in range(len(pr_points))]         #getting a seperate list for prey X co-ordination for center point
pr_y = [fn.pixelToCm(pr_points[y][1],96) for y in range(len(pr_points))]         #getting a seperate list for prey Y co-ordination for center point

distances_pdr = fn.distance(pdr_x,pdr_y)
distances_pr = fn.distance(pr_x,pr_y)

velocities_pdr = fn.velocity(distances_pdr, time)
velocities_pr = fn.velocity(distances_pr, time)
distance_between_object = fn.distance_between_objects(pdr_x,pdr_y,pr_x,pr_y)

##poly = np.polyfit(T,velocities_pdr,43)
##poly_eqn = np.poly1d(poly)
##print(np.polyval(poly,[0.3333333333333333,0.6666666666666666, 1.0]))

T = [(i+1)/timeSpliter for i in range(len(velocities_pdr))]

f_pdr = interp1d(T,velocities_pdr,kind='linear',fill_value="extrapolate")
f_pr = interp1d(T,velocities_pr,kind='linear',fill_value="extrapolate")
f_distance = interp1d(T,distance_between_object,kind='linear',fill_value="extrapolate")
newT_pdr =  np.linspace(T[0],T[-1],num=60,endpoint=True)
newT_pr =  np.linspace(T[0],T[-1],num=60,endpoint=True)

without_nans_pdr = maf.filter(f_pdr(newT_pdr),10)
without_nans_pr = maf.filter(f_pr(newT_pr),10)
without_nans_distance = maf.filter(f_distance(newT_pdr),10)
##
newT_pdrT = newT_pdr[:len(without_nans_pdr)]
newT_prT = newT_pr[:len(without_nans_pr)]

##plt.figure(1)
#plt.plot(newT_pdrT,without_nans_pdr, marker='o', label = 'Predator Speed')
#plt.plot(newT_prT,without_nans_pr,marker='o', label = 'Prey Speed')
#plt.plot(T,velocities_pdr, marker='o', label = 'Predator Speed')
##plt.plot(T,velocities_pr,marker='o', label = 'Prey Speed')
#plt.xlabel('time(t)')
#plt.ylabel('velocity(v)')
#plt.legend()
##
##plt.figure(2)
###plt.plot(newT_pdrT,without_nans_distance,marker='o', label = 'Distances Between Predator & Prey')
##plt.bar(newT_pdrT,without_nans_distance, label = 'Distances Between Predator & Prey', width = 0.07)
###plt.bar(T,distance_between_object, label = 'Distances Between Predator & Prey', width = 0.2)
###plt.bar(newT_pdr,f_distance(newT_pdr), label = 'Distances Between Predator & Prey', width = 0.08)
##plt.xlabel('time(t)')
##plt.ylabel('Distance(d)')
##plt.legend()
##

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(newT_pdrT,without_nans_distance, label = 'Distances Between Predator & Prey', width = 0.07)
ax2.plot(newT_pdrT,without_nans_pdr, marker='o', color = 'red', label = 'Predator Speed')
ax2.plot(newT_prT,without_nans_pr,marker='o', color = 'orange', label = 'Prey Speed')
ax1.set_xlabel('Time(s)', fontsize = 14)
ax1.set_ylabel('Distance(cm)', fontsize = 14)
ax2.set_ylabel('Velocity(cm)', fontsize = 14)
plt.title('Predator & Prey Time-Velocity and Time-Distance Graph Comparison', fontsize = 20, pad = 20)
ax = plt.gca()
ax.set_xlim(newT_pdrT[0]-0.1,newT_pdrT[-1]+0.1)
ax1.legend(fancybox=True)
ax2.legend(fancybox=True)
plt.show()

