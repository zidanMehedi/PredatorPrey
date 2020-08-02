import cv2
import json
import math
import os
from PIL import Image


sample = 'Sample1'

myJSONS = [file for file in os.listdir('E:\\PredatorPray\\'+sample+'\\JSON_Files')]
myImages = [img for img in os.listdir('E:\\PredatorPray\\'+sample+'\\Frames')]

for img,file in zip(myImages,myJSONS):
    imageFrame = cv2.imread(os.path.join('E:\\PredatorPray\\'+sample+'\\Frames',img),1)
    DataJSON = json.loads(open(os.path.join('E:\\PredatorPray\\'+sample+'\\JSON_Files',file),'r').read())
    image = cv2.rectangle(imageFrame,(math.ceil(DataJSON['shapes'][0]['points'][0][0]),math.ceil(DataJSON['shapes'][0]['points'][0][1])),
                    (math.ceil(DataJSON['shapes'][0]['points'][1][0]),math.ceil(DataJSON['shapes'][0]['points'][1][1])),
                    (0,0,255),1)

    image = cv2.rectangle(imageFrame,(math.ceil(DataJSON['shapes'][1]['points'][0][0]),math.ceil(DataJSON['shapes'][1]['points'][0][1])),
                        (math.ceil(DataJSON['shapes'][1]['points'][1][0]),math.ceil(DataJSON['shapes'][1]['points'][1][1])),
                        (0,255,0),1)
    tempJSON = myJSONS[:myJSONS.index(file)]

    myJSON = json.loads(open(os.path.join('E:\\PredatorPray\\'+sample+'\\JSON_Files',myJSONS[0]),'r').read())
    pdx2 = math.ceil((myJSON['shapes'][0]['points'][0][0]+myJSON['shapes'][0]['points'][1][0])/2)
    pdy2 = math.ceil((myJSON['shapes'][0]['points'][0][1]+myJSON['shapes'][0]['points'][1][1])/2)
    pdx = pdx2
    pdy = math.ceil(pdy2-10)
    image = cv2.line(imageFrame,(pdx,pdy),(pdx2,pdy2),(0,0,255),1)

    prx2 = math.ceil((myJSON['shapes'][1]['points'][0][0]+myJSON['shapes'][1]['points'][1][0])/2)
    pry2 = math.ceil((myJSON['shapes'][1]['points'][0][1]+myJSON['shapes'][1]['points'][1][1])/2)
    prx = prx2
    pry = math.ceil(pry2-10)
    image = cv2.line(imageFrame,(prx,pry),(prx2,pry2),(0,255,0),1)

    for data in tempJSON[1:]:
            myJSON = json.loads(open(os.path.join('E:\\PredatorPray\\'+sample+'\\JSON_Files',data),'r').read())
            pdx2 = math.ceil((myJSON['shapes'][0]['points'][0][0]+myJSON['shapes'][0]['points'][1][0])/2)
            pdy2 = math.ceil((myJSON['shapes'][0]['points'][0][1]+myJSON['shapes'][0]['points'][1][1])/2)
            pdx1 = pdx
            pdy1 = pdy
            image = cv2.line(imageFrame,(pdx,pdy),(pdx2,pdy2),(0,0,255),1)
            pdx = pdx2
            pdy = pdy2

            prx2 = math.ceil((myJSON['shapes'][1]['points'][0][0]+myJSON['shapes'][1]['points'][1][0])/2)
            pry2 = math.ceil((myJSON['shapes'][1]['points'][0][1]+myJSON['shapes'][1]['points'][1][1])/2)
            prx1 = prx
            pry1 = pry
            image = cv2.line(imageFrame,(prx,pry),(prx2,pry2),(0,255,0),1)
            prx = prx2
            pry = pry2
                        
    cv2.imwrite(img,image)


folder = 'E:\PredatorPray\S1Plot'
name = 'newvideo.mp4'

def video_gen():
    images = [img for img in os.listdir(folder)]
    frame = cv2.imread(os.path.join(folder,images[0]))
    height,width,layers = frame.shape
    video = cv2.VideoWriter(name,0,6,(width,height))
    os.chdir('E:\PredatorPray\S5Plot')
    for image in images:
        video.write(cv2.imread(os.path.join(folder,image)))
    cv2.destroyAllWindows()
    video.release()

video_gen()



def playVideo():
    cap = cv2.VideoCapture(os.path.join(folder,name))
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('Frame',frame)
        if (cv2.waitKey(150) & 0xFF==ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

playVideo()
