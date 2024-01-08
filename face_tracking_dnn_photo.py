import cv2
import numpy as np
import csv

# DNN-based Face Detector (SSD)
dnn_net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

image = cv2.imread('sample.jpg')

largest_box = None  # Initialize variable to store the largest bounding box
max_area = 0  # Initialize maximum area as 0

height, width, _ = image.shape

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# DNN-based Face Detection
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
dnn_net.setInput(blob)
detections_dnn = dnn_net.forward()

# Process DNN-based detections
for i in range(detections_dnn.shape[2]):
    confidence = detections_dnn[0, 0, i, 2]
    if confidence > 0.3:
        box = detections_dnn[0, 0, i, 3:7] * np.array([width, height, width, height])
        (startX, startY, endX, endY) = box.astype("int")
        area = (endX - startX) * (endY - startY)
        
        if area > max_area:
            max_area = area
            largest_box = (startX, startY, endX, endY)

if largest_box is not None:
    (startX, startY, endX, endY) = largest_box
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

data = [[startX, startY, (endX-startX), (endY-startY)]] #MATLAB

# Open the file for writing
with open('sample_face_coord.txt', 'w') as file:
    # Create a CSV writer object
    writer = csv.writer(file, delimiter=',')

    # Write the single row of data to the file
    writer.writerow(data)
    #writer.writerow(data[0])

cv2.imshow('Face Tracking', cv2.resize(image, (0, 0), fx=0.5, fy=0.5))
cv2.waitKey(0)
cv2.destroyAllWindows()
