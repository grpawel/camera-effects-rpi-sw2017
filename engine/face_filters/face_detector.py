import cv2

# parts of face definistions
face_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_smile.xml')
mouth_cascade = cv2.CascadeClassifier('./res/haarcascades/Mouth.xml')
nose_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_mcs_nose.xml')
resize_scale = 0.5

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
yellow = (0, 255, 255)
orange = (0,140,255)


def low_to_high_resize(x, y):
    return (int(x // resize_scale), int(y // resize_scale))


def draw_rectange_on_face(img, face):
    ((x, y), (width, height)) = low_to_high_resize(face[0], face[1]), low_to_high_resize(face[2], face[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), blue, 5)
    return img


def draw_rectange_on_eye(img, eye):
    ((x, y), (width, height)) = low_to_high_resize(eye[0], eye[1]), low_to_high_resize(eye[2], eye[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), green, 5)
    return img


def draw_rectange_on_smile(img, smile):
    ((x, y), (width, height)) = low_to_high_resize(smile[0], smile[1]), low_to_high_resize(smile[2], smile[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), red, 5)
    return img


def draw_rectange_on_mouth(img, mouth):
    ((x, y), (width, height)) = low_to_high_resize(mouth[0], mouth[1]), low_to_high_resize(mouth[2], mouth[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), yellow, 2)
    return img


def draw_rectange_on_nose(img, nose):
    ((x, y), (width, height)) = low_to_high_resize(nose[0], nose[1]), low_to_high_resize(nose[2], nose[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), orange, 3)
    return img


def face_detector(img, faces=True, eyes=False, smiles=False, mouths=False, noses=False):
    scale = 1.3
    min_neighbours = 5

    # convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=resize_scale, fy=resize_scale, interpolation=cv2.INTER_AREA)

    if faces:
        for face in face_cascade.detectMultiScale(gray, scale, min_neighbours):
            img = draw_rectange_on_face(img, face)
    if eyes:
        for eye in eyes_cascade.detectMultiScale(gray, scale, min_neighbours):
            img = draw_rectange_on_eye(img, eye)
    if smiles:
        for smile in smile_cascade.detectMultiScale(gray, scale, min_neighbours):
            img = draw_rectange_on_smile(img, smile)
    if mouths:
        for mouth in mouth_cascade.detectMultiScale(gray, 1.7, 11):
            img = draw_rectange_on_mouth(img, mouth)
    if noses:
        for nose in nose_cascade.detectMultiScale(gray, scale, min_neighbours):
            img = draw_rectange_on_nose(img, nose)
    return img
