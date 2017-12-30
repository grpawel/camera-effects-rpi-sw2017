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

class FaceDetector():
    def __init__(self,faces=True, eyes=False, smiles=False, mouths=False, noses=False):
        self.find_face = faces
        self.find_eye = eyes
        self.find_smiles = smiles
        self.find_mouths = mouths
        self.find_noses = noses
        self.face_live = 5
        self.eye_live = 5
        self.smile_live = 5
        self.nose_live = 5
        self.mouth_live = 5
        self.faces = []
        self.eyes = []
        self.noses = []
        self.smiles = []
        self.mouths = []
        self.cnt = 0
    def procces_img(self, img):
        self.cnt += 1
        if min(self.eye_live, self.face_live, self.mouth_live, self.nose_live, self.smile_live) < 0:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, None, fx=resize_scale, fy=resize_scale, interpolation=cv2.INTER_AREA)
        if self.find_face:
            if self.face_live < 0:
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    self.face_live = 4
                    self.faces = faces
            for face in self.faces:
                img = draw_rectange_on_face(img, face)
            self.face_live-=1

        if self.find_eye:
            if self.eye_live < 0:
                eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)
                if len(eyes)>0:
                    self.eyes = eyes
                    self.eye_live = 5
            for eye in self.eyes:
                img = draw_rectange_on_eye(img,eye)
            self.eye_live -= 1

        if self.find_smiles:
            if self.smile_live < 0:
                smiles = smile_cascade.detectMultiScale(gray, 1.3, 5)
                if len(smiles) > 0:
                    self.smiles = smiles
                    self.smile_live = 4
            for smile in self.smiles:
                img = draw_rectange_on_smile(img, smile)
            self.smile_live-=1

        if self.find_mouths:
            if self.mouth_live <0:
                mouths = mouth_cascade.detectMultiScale(gray, 2, 20)
                if len(mouths) >0:
                    self.mouths = mouths
                    self.mouth_live = 6
            for mouth in self.mouths:
                img = draw_rectange_on_mouth(img, mouth)
            self.mouth_live -= 1

        if self.find_noses:
            if self.nose_live < 0:
                noses = nose_cascade.detectMultiScale(gray, 1.3, 5)
                if len(noses) > 0:
                    self.noses = noses
                    self.nose_live=5
            for nose in self.noses:
                img = draw_rectange_on_nose(img, nose)
            self.nose_live-=1

        return img

def low_to_high_resize(x, y):
    return (int(x // resize_scale), int(y // resize_scale))

def draw_rectange_on_face(img, face):
    ((x, y), (width, height)) = low_to_high_resize(face[0], face[1]), low_to_high_resize(face[2], face[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), blue, 5)
    return img


def draw_rectange_on_eye(img, eye):
    ((x, y), (width, height)) = low_to_high_resize(eye[0], eye[1]), low_to_high_resize(eye[2], eye[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), green, 5)
    cv2.putText(img, 'oko', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1,green, thickness=2)
    return img


def draw_rectange_on_smile(img, smile):
    ((x, y), (width, height)) = low_to_high_resize(smile[0], smile[1]), low_to_high_resize(smile[2], smile[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), red, 5)
    cv2.putText(img, 'uśmiech', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 4, red)
    return img


def draw_rectange_on_mouth(img, mouth):
    ((x, y), (width, height)) = low_to_high_resize(mouth[0], mouth[1]), low_to_high_resize(mouth[2], mouth[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), yellow, 2)
    cv2.putText(img, 'usta', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, yellow, thickness=2)
    return img


def draw_rectange_on_nose(img, nose):
    ((x, y), (width, height)) = low_to_high_resize(nose[0], nose[1]), low_to_high_resize(nose[2], nose[3])
    img = cv2.rectangle(img, (x, y), (x + width, y + height), orange, 3)
    cv2.putText(img, 'nos', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, orange, thickness=2)
    return img


