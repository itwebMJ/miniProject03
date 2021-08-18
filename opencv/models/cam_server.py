import cv2
import pkg_resources

#cascade_file = pkg_resources.resource_filename('board.models','haar_xml/haarcascade_frontalface_alt2.xml')
f = 'static/haar_xml/haarcascade_frontalface_alt2.xml'
def detect(image):
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(f)
    face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150))
    h1, w1, _ = image.shape

    if len(face_list) > 0:

        print(face_list)
        color = (0, 0, 255)  # red
        for face in face_list:
            x, y, w, h = face
            image2 = image.copy()
            roi = image[y:y + h, x:x + w]
            cv2.rectangle(image2, (x, y), (x + w, y + h), color, thickness=8)
            roi = cv2.resize(roi, (w1, h1))
            res = cv2.hconcat([image2, roi])
        return res




