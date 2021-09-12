from imutils.video import WebcamVideoStream
import face_recognition
import cv2
import numpy as np
from threading import Thread

class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
	def read(self):
		# return the frame most recently read
		return self.frame
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-n", "--num-frames", type=int, default=100,
# 	help="# of frames to loop over for FPS test")
# ap.add_argument("-d", "--display", type=int, default=-1,
# 	help="Whether or not frames should be displayed")
# args = vars(ap.parse_args())

# Get a reference to webcam #0 (the default one) 
# OLD METHOD LOW FPS No threading
# video_capture = cv2.VideoCapture(0)

#

filePathObj = open("PathToImages.txt", "r") #opens the file in read mode.
filepaths = filePathObj.read().splitlines() #puts the file into a list.
filePathObj.close()
known_face_encodings = []
for i in filepaths:
    load_image = face_recognition.load_image_file(i)
    image_face_encoding = face_recognition.face_encodings(load_image)[0]
    known_face_encodings.append(image_face_encoding)

# Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

namesObj = open("KnownNames.txt", "r") #opens the file in read mode.
known_face_names = namesObj.read().splitlines() #puts the file into a list.
namesObj.close()

dataObj = open("KnownData.txt", "r") #opens the file in read mode.
known_data = dataObj.read().splitlines() #puts the file into a list.
dataObj.close()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

vs = WebcamVideoStream(src=0).start()


while True:
    #OLD METHOD LOW FPS No Threading
    #ret, frame = video_capture.read()
    # Grab a single frame of video
    frame = vs.read()
    frame = cv2.flip(frame, 1)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, ((left + 5, top + 5)), (right + 5, bottom + 5), (189, 195, 199), 2)
        (width_of_name_container, height_of_name_container), size_of_name_container = cv2.getTextSize(name, cv2.FONT_HERSHEY_DUPLEX, 0.75, 1)
        
        #centre the name in box
        adjuster = 0
        if(width_of_name_container + 30 < 165):
            adjuster = 82 - width_of_name_container//2
            width_of_name_container = 165
            
        # Draw a label with a name below the face
        # cv2.rectangle(frame, (left + 5, bottom - 30), (right + 5, bottom + 5), (89, 216, 250), cv2.FILLED)
        cv2.rectangle(frame, (right + 5, top + 4), (right + width_of_name_container + 35, top + 40), (89, 216, 250), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        person_data = []
        #display image in db
        if(name != "Unknown"):
            name_index = 0
            for i in range(0, len(known_face_names)):
                if(name == known_face_names[i]):
                    name_index = i
            person_data = known_data[name_index]
            person_data = person_data.split(", ")


            path_to_img = filepaths[name_index]
            db_img = cv2.imread(path_to_img)
            db_img = cv2.resize(db_img,(150,150))
            x_offset_db_img = right + width_of_name_container//2 + 20 - 75 #centre the db image
            y_offset_db_img = top - 146
            x_end = x_offset_db_img + db_img.shape[1]
            y_end = y_offset_db_img + db_img.shape[0]
            if((y_offset_db_img < frame.shape[1]) and (y_offset_db_img > 0) and (x_offset_db_img < frame.shape[0]) and (x_offset_db_img > 0)):
                frame[y_offset_db_img:y_end, x_offset_db_img:x_end] = db_img
            
                    
        # cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.75, (0, 84, 211), 1)
        cv2.putText(frame, name, (right + adjuster + 20, top + 35), font, 0.75, (0, 84, 211), 1)
        it = 0
        for i in person_data:
            it += (height_of_name_container + 5)
            cv2.putText(frame, i, (right + 20, top + 45 + it), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('LiveFeed', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
# video_capture.release()
vs.stop()
cv2.destroyAllWindows()