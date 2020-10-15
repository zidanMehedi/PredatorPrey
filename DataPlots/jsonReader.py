#importing all necessary libraries and modules

import json
import os

pdr_points = []     #empty list for predator co-ordinations

pr_points = []      #empty list for prey co-ordinations

sample = 'Sample5'

myJSONS = [file for file in os.listdir('E:\\PredatorPrey\\'+sample+'\\JSON_Files')]     #taking JSON files in a list of a particular sample




##fetching co-ordintations of predator and prey to their corresponding lists

for file in myJSONS:
    myJSON = json.loads(open(os.path.join('E:\\PredatorPrey\\'+sample+'\\JSON_Files', file),'r').read())     #reading JSON files of a particular sample
    
    predator=[(myJSON['shapes'][0]['points'][0][0]+myJSON['shapes'][0]['points'][1][0])/2,
                (myJSON['shapes'][0]['points'][0][1]+myJSON['shapes'][0]['points'][1][1])/2]        #fetching predator co-ordinations and finding the center point
    
    prey=[(myJSON['shapes'][1]['points'][0][0]+myJSON['shapes'][1]['points'][1][0])/2,
                (myJSON['shapes'][1]['points'][0][1]+myJSON['shapes'][1]['points'][1][1])/2]        #fetching prey co-ordinations and finding the center point


    #getting the lists filled with available co-ordinates
    
    pdr_points.append(predator)
    pr_points.append(prey)
