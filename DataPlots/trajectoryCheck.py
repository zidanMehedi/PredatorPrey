import jsonReader as jr
import functions as fn
import matplotlib.pyplot as plt


pdr_points = jr.pdr_points
pr_points = jr.pr_points

pdr_x = [fn.pixelToCm(pdr_points[x][0],96) for x in range(len(pdr_points))]      #getting a seperate list for predator X co-ordination for center point
pdr_y = [fn.pixelToCm(pdr_points[y][1],96) for y in range(len(pdr_points))]      #getting a seperate list for predator Y co-ordination for center point

pr_x = [fn.pixelToCm(pr_points[x][0],96) for x in range(len(pr_points))]         #getting a seperate list for prey X co-ordination for center point
pr_y = [fn.pixelToCm(pr_points[y][1],96) for y in range(len(pr_points))]

fig1, ax1 = plt.subplots()
ax2 = ax1.twiny()
##ax1.plot(pdr_x,pdr_y, 'ro-')
##ax2.plot(pr_x,pr_y, 'go-')
##plt.show()

pdr_X = pdr_x
pdr_Y = pdr_y
pr_X = pr_x
pr_Y = pr_y

from pykalman import KalmanFilter
import numpy as np
import copy


def kalman_filter(X, Y):
    outlier_thresh = 0

    # Treat y as position, and that y-dot is
    # an unobserved state - the velocity,
    # which is modelled as changing slowly (inertia)

    # state vector [y,
    #               y_dot]

    # transition_matrix =  [[1, dt],
    #                       [0, 1]]

    observation_matrix = np.asarray([[1, 0]])

    # observations:
    #t = [1,10,22,35,40,51,59,72,85,90,100]
    t = X

    # dt betweeen observations:
    dt = [np.mean(np.diff(t))] + list(np.diff(t))
    transition_matrices = np.asarray([[[1, each_dt],[0, 1]]
                                        for each_dt in dt])

    # observations
    ##y = np.transpose(np.asarray([[0.2,0.23,0.3,0.4,0.5,0.2,
    ##                              0.65,0.67,0.62,0.5,0.4]]))

    y = np.transpose(np.asarray([Y]))


    y = np.ma.array(y)


    leave_1_out_cov = []

    for i in range(len(y)):
        y_masked = np.ma.array(copy.deepcopy(y))
        y_masked[i] = np.ma.masked

        kf1 = KalmanFilter(transition_matrices = transition_matrices,
                       observation_matrices = observation_matrix)

        kf1 = kf1.em(y_masked)

        leave_1_out_cov.append(kf1.observation_covariance[0,0])

    # Find indexes that contributed excessively to observation covariance
    outliers = (leave_1_out_cov / np.mean(leave_1_out_cov)) < outlier_thresh

    for i in range(len(outliers)):
        if outliers[i]:
            y[i] = np.ma.masked


    kf1 = KalmanFilter(transition_matrices = transition_matrices,
                       observation_matrices = observation_matrix)

    kf1 = kf1.em(y)

    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(y)

    return smoothed_state_means


smoothed_pdr_state_means = kalman_filter(pdr_X, pdr_Y)
smoothed_pr_state_means = kalman_filter(pr_X, pr_Y)


import math
from sklearn.metrics import mean_squared_error
print(math.sqrt(mean_squared_error(pr_Y, smoothed_pr_state_means[:,0])*100))

#plt.figure()
ax1.plot(pdr_X, smoothed_pdr_state_means[:,0], 'b--', linewidth=5,label="Predator Value Estimate" )
ax1.plot(pdr_X, pdr_Y, 'r--', linewidth=2,label="Predator Observations")
ax1.legend(loc = 'lower right')

ax2.plot(pr_X, smoothed_pr_state_means[:,0], 'y--', linewidth=5 ,label="Prey Value Estimate" )
ax2.plot(pr_X, pr_Y, 'g--',linewidth=2,label="Prey Observations")
ax2.legend(loc = 'lower right')

ax1.set_xlim([0,20])
ax1.set_ylim([0,20])

ax2.set_ylim([0,20])
ax2.set_xlim([0,20])
ax2.legend(fancybox=True, bbox_to_anchor=(1, 0.1, 0, 0), loc = 'lower right')
#plt.xlabel("Time (s)")
#plt.ylabel("Value (unit)")
ax1.invert_yaxis()
#ax2.invert_yaxis()
#plt.legend(loc = 'bottom right')
plt.title('Kalman Filter Result', fontsize = 20, pad = 20)
plt.annotate('End Point', xytext=(18.06,4.41),xy=(17.27,7.37),arrowprops={'facecolor':'black'}, fontsize = 13)
plt.annotate('End Point', xytext=(18.31,9.98),xy=(17.18,8.32),arrowprops={'facecolor':'black'}, fontsize = 13)
#ax2.set_ylabel('y co-ordinate', fontsize = 14)
plt.show()
