import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_myhand = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.3, min_tracking_confidence=0.3)

# Load the PNG image
img = cv2.imread('sample.jpg')

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, _ = img.shape

# Define the ROI coordinates
roi_x = width // 4
#roi_y = height // 2
roi_y = 3*(height // 4)
roi_width = width // 4
#roi_height = height // 2
roi_height = height // 4

roi = img[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

# Apply light blurring
blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)

results = mp_myhand.process(blurred_roi)

# Convert back to BGR for rendering
roi = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
blurred_roi = cv2.cvtColor(blurred_roi, cv2.COLOR_RGB2BGR)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

data = []

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        x_min, x_max, y_min, y_max = float('inf'), 0, float('inf'), 0
        for i, landmark in enumerate(hand_landmarks.landmark):
            if i in [0, 1, 5, 9, 13, 17]:
                x = int(landmark.x * roi.shape[1]) + roi_x
                y = int(landmark.y * roi.shape[0]) + roi_y

                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y

            # mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        data.append([[x_min, y_min, (x_max-x_min), (y_max-y_min)]])   #MATLAB

# Open the file for writing
with open('sample_hand_coord.txt', 'w') as file:
    # Create a CSV writer object
    writer = csv.writer(file, delimiter=',')

    # Write the single row of data to the file
    writer.writerow(data)
    #writer.writerow(data[0])

# Display the blurred ROI and original image
cv2.imshow('captured_image.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
