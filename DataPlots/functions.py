import math

def pixelToCm(x,dpi):
    x = (x/dpi)*2.54
    return x

def distance(lst_x,lst_y):
    distance_list = [math.sqrt((lst_x[i+1]-lst_x[i])**2+(lst_y[i+1]-lst_y[i])**2) for i in range(len(lst_x)-1)]
    return distance_list

def distance_between_objects(lst_x1, lst_y1, lst_x2, lst_y2):
    distance_list = [math.sqrt((lst_x2[i]-lst_x1[i])**2+(lst_y2[i]-lst_y1[i])**2) for i in range (len(lst_x1)-1)]
    return distance_list

def velocity(lst, timeDivision):
    prev_velocity = 0
    time = timeDivision
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
    time = .5
    post_velocity = lst
    acceleration = []
    for i in range(len(post_velocity)):
        A = (post_velocity[i]-prev_velocity)/time
        acceleration.append(A)
        prev_velocity = post_velocity[i]
    return acceleration