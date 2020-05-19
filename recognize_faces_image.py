import face_recognition
import pickle
import cv2

print("[INFO] loading encodings...")
data = pickle.loads(open("./encodings.pickle", "rb").read())
print(data)
image = cv2.imread("./examples/example5.jpeg")
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb, model="cnn")
encodings = face_recognition.face_encodings(rgb, boxes)

names = []

for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"], encoding)
    name = "Unknown"

    if True in matches:
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}

        for i in matchedIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1


        name = max(counts, key=counts.get)

    names.append(name)

for ((top, right, bottom, left), name) in zip(boxes, names):
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = bottom + 15
    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

while True: 
    cv2.imshow("Image", image)
    try:
        cv2.waitKey(1)
    except KeyboardInterrupt:
        break
cv2.destroyWindow("Image")
