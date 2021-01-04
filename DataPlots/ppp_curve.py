#importing all necessary libraries and modules

from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14,})
import numpy as np
import jsonReader as jr
import functions as fn
import movingAvgFilter as maf
import math

videoLength = 7
timeSpliter = len(jr.myJSONS)/videoLength
time = 1/timeSpliter

pdr_points = jr.pdr_points
pr_points = jr.pr_points

pdr_x = [fn.pixelToCm(pdr_points[x][0],96) for x in range(len(pdr_points))]      #getting a seperate list for predator X co-ordination for center point
pdr_y = [fn.pixelToCm(pdr_points[y][1],96) for y in range(len(pdr_points))]      #getting a seperate list for predator Y co-ordination for center point

pr_x = [fn.pixelToCm(pr_points[x][0],96) for x in range(len(pr_points))]         #getting a seperate list for prey X co-ordination for center point
pr_y = [fn.pixelToCm(pr_points[y][1],96) for y in range(len(pr_points))]         #getting a seperate list for prey Y co-ordination for center point

distances_pdr = fn.distance(pdr_x,pdr_y)
distances_pr = fn.distance(pr_x,pr_y)

velocities_pdr = fn.velocity(distances_pdr, time)
#print(velocities_pdr)
velocities_pr = fn.velocity(distances_pr, time)
distance_between_object = fn.distance_between_objects(pdr_x,pdr_y,pr_x,pr_y)

##poly = np.polyfit(T,velocities_pdr,43)
##poly_eqn = np.poly1d(poly)
##print(np.polyval(poly,[0.3333333333333333,0.6666666666666666, 1.0]))

T = [(i+1)/timeSpliter for i in range(len(velocities_pdr))]
#print(T)

f_pdr = interp1d(T,velocities_pdr,kind='linear',fill_value="extrapolate")
f_pr = interp1d(T,velocities_pr,kind='linear',fill_value="extrapolate")
f_distance = interp1d(T,distance_between_object,kind='linear',fill_value="extrapolate")
newT_pdr =  np.linspace(T[0],T[-1],num=99,endpoint=True)
newT_pr =  np.linspace(T[0],T[-1],num=99,endpoint=True)
#print(list(f_pdr(newT_pdr)))
#print(list(newT_pdr))

without_nans_pdr = maf.filter(f_pdr(newT_pdr),10)
without_nans_pr = maf.filter(f_pr(newT_pr),10)
without_nans_distance = maf.filter(f_distance(newT_pdr),10)
##
newT_pdrT = newT_pdr[:len(without_nans_pdr)]
newT_prT = newT_pr[:len(without_nans_pr)]

#print(without_nans_distance)


Mean = math.fsum(without_nans_distance)/len(without_nans_distance)
print('Mean : ',format(Mean))


new_list = []
for i in range(len(without_nans_distance)):
    new_list.append(abs(Mean-without_nans_distance[i])**2)



sum = 0
for i in range(len(new_list)):
    sum = sum + new_list[i]
print('SD :', format(math.sqrt(math.fsum(new_list)/len(without_nans_distance))))

print(math.fsum(without_nans_distance))

Mean_Predator = fn.mean(without_nans_pdr)
Predator_SD = fn.standard_daviation(without_nans_pdr, Mean_Predator)

Mean_Prey = fn.mean(without_nans_pr)
Prey_SD = fn.standard_daviation(without_nans_pr, Mean_Prey)

Mean_Distance = fn.mean(without_nans_distance)
Distance_SD = fn.standard_daviation(without_nans_distance, Mean_Distance)

print('Predator Speed Mean : {predmean}\nPredator Speed SD : {predsd}' .format(predmean = Mean_Predator, predsd = Predator_SD))
print('Prey Speed Mean : {premean}\nPrey Speed SD : {presd}' .format(premean = Mean_Prey, presd = Prey_SD))
print('Distance Mean : {distmean}\nDistance SD : {distsd}' .format( distmean = Mean_Distance, distsd = Distance_SD))
print()
print('Initial Predator Speed : {0}'.format(without_nans_pdr[0]))
print('Final Predator Speed : {0}'.format(without_nans_pdr[-1]))
print('Maximum Predator Speed : {0}'.format(max(without_nans_pdr)))
print()
print('Predator Speed List : {0}' .format(without_nans_pdr))
print()
print('Initial Prey Speed : {0}'.format(without_nans_pr[0]))
print('Final Prey Speed : {0}'.format(without_nans_pr[-1]))
print('Maximum Prey Speed : {0}'.format(max(without_nans_pr)))
print()
print('Prey Speed List : {0}' .format(without_nans_pr))
print()
print('Initial Distance : {0}'.format(without_nans_distance[0]))
print('Final Distance : {0}'.format(without_nans_distance[-1]))
print('Maximum Distance : {0}'.format(max(without_nans_distance)))
print()
print('Prey Speed List : {0}' .format(without_nans_distance))
print()
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



##print(list(without_nans_pdr))
##print(list(without_nans_pr))
##print(list(newT_pdrT))


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(newT_pdrT,without_nans_distance, label = 'Distances Between \nPredator & Prey', width = 0.025 if videoLength < 10 else 0.05)
ax2.plot(newT_pdrT,without_nans_pdr, color = 'red', label = 'Predator Speed')
ax2.plot(newT_prT,without_nans_pr, color = 'orange', label = 'Prey Speed')
ax2.scatter(newT_pdrT,without_nans_pdr, s = 2 if videoLength < 10 else 10, marker='o', color = 'red')
ax2.scatter(newT_prT,without_nans_pr, s = 2 if videoLength < 10 else 10, marker='o', color = 'orange')
ax1.set_xlabel('Time(s)', fontsize = 20, labelpad = 7)
ax1.set_ylabel('Distance(cm)', fontsize = 20, labelpad = 10)
ax2.set_ylabel('Velocity(cm/s)', fontsize = 20, labelpad = 10)
plt.title('Predator & Prey Time-Velocity and Time-Distance Graph Comparison', fontsize = 25, pad = 20)
ax1.set_xlim([0,16])
ax1.set_ylim([0,11])
ax2.set_ylim([0,4.5])
ax1.legend(fancybox=True, fontsize = 'small', bbox_to_anchor=(0.5, 0.5, 0.5, 0.5), shadow = True, loc = 'upper right')
ax2.legend(fancybox=True, fontsize = 'small', shadow = True, bbox_to_anchor=(0.5, 0.5, 0.5, 0.35), loc = 'upper right')
plt.annotate('Catching Point', xytext=(6.08,0.97),xy=(5.96,0.69),arrowprops={'facecolor':'black'})
plt.annotate('Attack Point', xytext=(0.73,4.3),xy=(0.56,4.03),arrowprops={'facecolor':'black'})
plt.show()

