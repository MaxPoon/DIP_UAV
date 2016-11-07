
# import the necessary packages
import numpy as np
import argparse
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())


#raspistill -o image.jpg

# load the image
image = cv2.imread(args["image"])

# define the list of boundaries
boundaries = [
	([20, 20, 100], [110, 110, 255]),
	
]

# loop over the boundaries
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")

	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)

	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)
	# getting pixels from output
	px = output[10,10]
	RED_MIN = np.array([20, 20, 100], np.uint8)
        RED_MAX = np.array([110, 110, 255], np.uint8)

        dst = cv2.inRange(output, RED_MIN, RED_MAX)
        no_red = cv2.countNonZero(dst)
        print('The number of red pixels is: ' + str(no_red))
       
        if(no_red> 200):
                
                print('true')
        else:
                print ('false')


 

	
