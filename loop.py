import cv2
import mediapipe as mp
import pydirectinput
from scipy.spatial import distance as dist

CAMERA = 0 # Usually 0, depends on input device(s)

MOUSE_DELTA = 20

EYE_BLINK_HEIGHT = .15
EYE_BULGE_HEIGHT = .6
EYE_SQUINT_HEIGHT = .2

WAIT_FRAMES = 10

NONE, LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3, 4
active_gesture = NONE
frames_waiting = 0

def get_aspect_ratio(top, bottom, right, left):
  height = dist.euclidean([top.x, top.y], [bottom.x, bottom.y])
  width = dist.euclidean([right.x, right.y], [left.x, left.y])
  return height / width

cap = cv2.VideoCapture(CAMERA)

def update_gesture(direction):
  global active_gesture, frames_waiting

  if active_gesture == direction:
    frames_waiting += 1
  else:
    active_gesture = direction
    frames_waiting = 0
  if frames_waiting > WAIT_FRAMES:
    return True

with mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success: break

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    if results.multi_face_landmarks and len(results.multi_face_landmarks) > 0:
      face_landmarks = results.multi_face_landmarks[0]
      face = face_landmarks.landmark

      eyeR_ar = get_aspect_ratio(face[159], face[145], face[133], face[33])
      eyeL_ar = get_aspect_ratio(face[386], face[374], face[362], face[263])
      eyeA_ar = (eyeR_ar + eyeL_ar) / 2

      if (eyeL_ar < EYE_BLINK_HEIGHT) and (eyeR_ar > EYE_SQUINT_HEIGHT):
        print("L squint: LEFT")
        if update_gesture(LEFT):
          pydirectinput.move(-MOUSE_DELTA, 0, relative=True)
      elif (eyeR_ar < EYE_BLINK_HEIGHT) and (eyeL_ar > EYE_SQUINT_HEIGHT):
        print("R squint: RIGHT")
        if update_gesture(RIGHT):
          pydirectinput.move(MOUSE_DELTA, 0, relative=True)
      elif eyeA_ar > EYE_BULGE_HEIGHT:
        if update_gesture(UP):
          print("big eyes: UP")
          pydirectinput.move(0, -MOUSE_DELTA, relative=True)
      elif (eyeL_ar < EYE_SQUINT_HEIGHT) and (eyeR_ar < EYE_SQUINT_HEIGHT):
        if update_gesture(DOWN):
          print("both squint: DOWN")
          pydirectinput.move(0, MOUSE_DELTA, relative=True)
      else:
        active_gesture = NONE

cap.release()
