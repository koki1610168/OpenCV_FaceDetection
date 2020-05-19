from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# construct the argument tparser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--dataset', required=True, help='path to input directory of face + images')
# ap.add_argument('-e', '--encodings', required=True, help='path to serialized db of facial encodings')
# ap.add_argument('-d', '--detection-method', type=str, default='cnn', help="face detection model to use: either 'hog' or 'cnn")

# args = vars(ap.parse_args())

print("[INFO] quantifying faces...")
imagePaths = []
for image_dir in os.listdir("./dataset"):
    path_with_label = {image_dir[:-7]: []}
    for image in os.listdir("./dataset/{}".format(image_dir)):
        path_with_label[image_dir[:-7]].append(image)
    imagePaths.append(path_with_label)

#print(imagePaths)
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
    for (image_key, image_list) in imagePath.items():
        for image in image_list:
            #name of the player(key)
            print(image)
            name = list(imagePath.keys())[0]
            #load the image
            image_read = cv2.imread("./dataset/" + image_key + "_images/"+ image)
            
            #dlib expects rgb so we convert it
            rgb = cv2.cvtColor(image_read, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model="cnn")

            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)

print("[INFO] serializin encodings...")
data = {"encodings": knownEncodings, "names": knownNames}

if os.path.exists("./encodings.pickle"):
    os.remove("./encodings.pickle")

with open("./encodings.pickle", "wb") as f:
    f.write(pickle.dumps(data))