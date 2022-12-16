import cv2
import mediapipe as mp
import pyautogui
blnk=False
hold=False # toggles the click or hold mode
# adjust the blink threshold for both eyes for me 0.006 is good
# the program checks for values below the threshold because as you close your eyes the distance between the top and bottom of the eye decreases
right_eye_thresh=0.006
left_eye_thresh=0.006
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
mp_face_mesh.refine_landmarks=True
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture('/dev/video1') # select your video device (here it is the second video device on linux)
# for windows it would probably be like: cap = cv2.VideoCapture(0) for your first video device
def chck_click(faces,rt_thresh,lt_thresh):
  global hold
  global blnk
  for i in range(len(faces)):
    face=faces[i].landmark
    #print(face[145].y-face[159].y) print distance beetwen the top and the bottom of the right eye
    #print(face[374].y-face[386].y) print distance beetwen the top and the bottom of the left eye
    if face[145].y-face[159].y<rt_thresh and face[374].y-face[386].y<lt_thresh:
        if blnk==False:
          if hold==False:
            pyautogui.click()
          else:
            pyautogui.mouseDown()
          blnk=True
    else:
      if hold==True and blnk==True:
        pyautogui.mouseUp()
      blnk=False
with mp_face_mesh.FaceMesh(
    max_num_faces=1,# adjust it to your liking
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    try:
      faces=results.multi_face_landmarks
      chck_click(faces,right_eye_thresh,left_eye_thresh)
    except:
      pass
cap.release()
