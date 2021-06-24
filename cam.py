import cv2
import time
import numpy

# Deciding the codex scheme for the output file & specifing properties for output file
cc = cv2.VideoWriter_fourcc(*'XVID')
outfile = cv2.VideoWriter('output.avi' , cc , 20.0 , (600,400))

# Starting the Web Cam 
cam = cv2.VideoCapture(0)

# Make the code wait for 2 sec
time.sleep(2)
bg = 0

#caputring the background from the frames for 80
for i in range(80):
    flag,bg = cam.read()

bg = numpy.flip(bg , axis = 1)

# Caputring a image when the cam is on
while cam.isOpened():
    ret,img = cam.read()

    if not ret:
        break

    #Flipping the image to be consistent
    img = numpy.flip(img,axis=1)

    #Converting image into HSV model
    hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)

    #Creating the masks
    lower = numpy.array([0,100,52])
    upper = numpy.array([20,255,255])
    mask1 = cv2.inRange(hsv,lower,upper)

    lower = numpy.array([180,100,52])
    upper = numpy.array([200,255,255])
    mask2 = cv2.inRange(hsv,lower,upper)

    mask1 = mask1 + mask2

    # Opening the image and morphing the same by exapanding the image
    mask1 = cv2.morphologyEx(mask1 , cv2.MORPH_OPEN , numpy.ones((3,3), numpy.uint8))
    mask1 = cv2.morphologyEx(mask1 , cv2.MORPH_DILATE , numpy.ones((3,3), numpy.uint8))

    # Selecting part without mask 1 and storing it in mask 2
    mask2 = cv2.bitwise_not(mask1)

    #Keeping only the part of the image whoch does not have red color
    result1 = cv2.bitwise_and(img,img,mask = mask2)
    result2 = cv2.bitwise_and(bg,bg,mask = mask1)

    final = cv2.addWeighted(result1,1,result2,1,0)
    outfile.write(final)
    cv2.imshow("MAGIC" , final)
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break

cam.release()
cv2.destroyAllWindows()
