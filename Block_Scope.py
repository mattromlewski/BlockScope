import cv2
import numpy as np
import time

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture(0)
frameCounter = 0

#capture one frame
ret, frame = cap.read()

#image scale
scale =1

#blank function for slider bars
def nothing(x):
    pass

#Initialize Window object
cv2.namedWindow('StatsProject')

#Initialize slider bars
cv2.createTrackbar('Pixels per mm [1]','StatsProject',0,10,nothing)
cv2.createTrackbar('Pixels per mm [2]','StatsProject',0,10,nothing)
cv2.createTrackbar('Pixels per mm [3]','StatsProject',0,10,nothing)
cv2.createTrackbar('Pixels per mm [4]','StatsProject',0,10,nothing)

then = 0

while(1):

    now = time.time()
    elapsed_time = now - then
    fps = elapsed_time ** (-1)
    then = now

    #declare HSV range for filtering
    lower_blue = np.array([30, 150, 50])
    upper_blue = np.array([255, 255, 180])

    #capture one frame
    ret, frame = cap.read()

    # reszize video
    height, width, layers = frame.shape
    new_h = height * scale
    new_w = width * scale
    frame = cv2.resize(frame, (int(new_w), int(new_h)))

    #convert to HSV Spectrum
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # color threshold using HSV window
    blue = cv2.inRange(hsv, lower_blue, upper_blue)

    #Superimpose color from frame onto the binary image
    result = cv2.bitwise_and(frame,frame, mask= blue)

    #declare kernel shape for erosion
    e_kernel = np.ones((2,2), np.uint8)

    #blur/smooth image
    median = cv2.medianBlur(blue,5)

    #despeckle image
    eroded = cv2.erode(median, e_kernel, iterations = 1)

    #max and min values for use in extent analysis
    max_i = 0
    min_i = new_h

    max_j = 0
    min_j = new_w

    #loop to determine maximums and minimums
    for i in range(0,new_h):
        for j in range(0, new_w):
            if eroded[i][j]:
                if i > max_i:
                    max_i = i

                if j > max_j:
                    max_j = j


                if i < min_i:
                    min_i = i

                if j < min_j:
                    min_j = j

    #corners for box drawing
    topCorner =  (max_j,max_i)
    bottomCorner = (min_j, min_i)

    #offset corners for second box drawing (cosmetic)
    topCornerOff = (max_j+5, max_i+5)
    bottomCornerOff = (min_j-5, min_i-5)

    #draw rectangles on raw frame
    cv2.rectangle(frame,bottomCorner,topCorner,(0,255,0),2)
    cv2.rectangle(frame, bottomCornerOff, topCornerOff, (0, 255, 0), 2)

    #determine length in pixel units
    lenghtPX = max_j-min_j

    px_to_mm = 0 #scale factor

    #if slider is not set to zero, take the reciprocol and add that to the scale factor
    #each slider contributes one tenth the amount to the scale factor as the slider before it

    if cv2.getTrackbarPos('Pixels per mm [1]','StatsProject') > 0:
        #px_to_mm1 = 1 / (cv2.getTrackbarPos('Pixels per mm [1]','StatsProject'))
        px_to_mm1 = (cv2.getTrackbarPos('Pixels per mm [1]', 'StatsProject'))
        px_to_mm += px_to_mm1/10

    if cv2.getTrackbarPos('Pixels per mm [2]','StatsProject') > 0:
        #px_to_mm2 = 1 / (cv2.getTrackbarPos('Pixels per mm [2]','StatsProject'))
        px_to_mm2 = (cv2.getTrackbarPos('Pixels per mm [2]', 'StatsProject'))
        px_to_mm += px_to_mm2/100

    if cv2.getTrackbarPos('Pixels per mm [3]','StatsProject') > 0:
        #px_to_mm3 = 1 / (cv2.getTrackbarPos('Pixels per mm [3]','StatsProject'))
        px_to_mm3 = (cv2.getTrackbarPos('Pixels per mm [3]', 'StatsProject'))
        px_to_mm += px_to_mm3/1000

    if cv2.getTrackbarPos('Pixels per mm [4]','StatsProject') > 0:
        #px_to_mm4 = 1 / (cv2.getTrackbarPos('Pixels per mm [4]', 'StatsProject'))
        px_to_mm4 = (cv2.getTrackbarPos('Pixels per mm [4]','StatsProject'))
        px_to_mm += px_to_mm4/10000

    #Calculate length in mm
    lengthMM = px_to_mm*lenghtPX

    #format numbers
    lengthMM = float("{0:.4f}".format(lengthMM))
    px_to_mm = float("{0:.4f}".format(px_to_mm))

    font = cv2.FONT_HERSHEY_DUPLEX
    font_thick = 1
    #write numbers
    cv2.putText(frame,'mm length: ' + str(lengthMM), (20, 80), font, 1, (0, 0, 0), font_thick, cv2.LINE_AA)
    cv2.putText(frame, 'Pixel length: ' + str(lenghtPX), (20, 40), font, 1, (0, 0, 0), font_thick,
                cv2.LINE_AA)
    round(px_to_mm, 3)
    cv2.putText(frame, 'Pixels to mm: ' + str(px_to_mm), (20, 460), font, 1, (0, 0, 0), font_thick,
                cv2.LINE_AA)

    cv2.putText(result, 'FILTERING...', (20, 40), font, 1, (0, 0, 255), font_thick,
                cv2.LINE_AA)


    cv2.putText(result, 'FPS '+str(int(fps)), (450, 40), font, 1, (0, 0, 255), font_thick,
                cv2.LINE_AA)

    #cosmetic lines
    cv2.line(result, (0, 240), (640, 240), (0, 0, 255), 1)
    cv2.line(result, (320, 0), (320, 480), (0, 0, 255), 1)

    cv2.line(result, (0, 260), (640, 260), (0, 0, 255), 1)
    cv2.line(result, (0, 220), (640, 220), (0, 0, 255), 1)

    cv2.line(result,(max_j, min_i), (min_j,max_i), (150, 150, 150), 2)
    cv2.line(result, (min_j, min_i), (max_j, max_i), (150, 150, 150), 2)

    #print(min_i)
    #print(min_j)
    #print(max_i)
    #print('maxj:',max_j)

    #compund two images together before showing
    display = np.hstack((frame, result))

    cv2.imshow('StatsProject', display)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    
cap.release()
cv2.destroyAllWindows()

    
