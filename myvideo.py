from PIL import Image
import os
import cv2

for file in os.listdir('E:\\PredatorPray\\Sample5\\Frames'):
    im = Image.open(os.path.join('E:\\PredatorPray\\Sample5\\Frames',file))
    print(im)

##def video_gen():
##    folder = 'E:\\PredatorPray\\Sample1\\Frames'
##    name = 'newvideo.avi'
##    images = [img for img in os.listdir(folder)]
##    video = cv2.VideoWriter(name,0,6,(512,386))
##    for image in images:
##        video.write(cv2.imread(os.path.join(folder,image)))
##    cv2.destroyAllWindows()
##    video.release()
##
##video_gen()







