import cv2
import mediapipe as mp
import pyautogui
from scipy.spatial import distance as dist

CAMERA = 0 # Usually 0, depends on input device(s)

MOUSE_DELTA = 20

EYE_BLINK_HEIGHT = .15

WAIT_FRAMES = 10


winkedR = False
winkedR_frames = 0
winkedL = False
winkedL_frames = 0

mp_face_mesh = mp.solutions.face_mesh

def get_aspect_ratio(top, bottom, right, left):
  height = dist.euclidean([top.x, top.y], [bottom.x, bottom.y])
  width = dist.euclidean([right.x, right.y], [left.x, left.y])
  return height / width

def timeout_double(state, frames):
  if state:
    frames += 1
  if frames > WAIT_FRAMES:
    frames = 0
    state = False
  return state, frames

cap = cv2.VideoCapture(CAMERA)

with mp_face_mesh.FaceMesh(
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

      if (eyeL_ar < EYE_BLINK_HEIGHT) and (eyeR_ar > EYE_BLINK_HEIGHT):
        winkedL = True
        if winkedR:
          print("R then L winks: DOWN")
          pyautogui.move(0, -MOUSE_DELTA)
        else:
          print("L wink: LEFT")
          pyautogui.move(-MOUSE_DELTA, 0)
      elif (eyeR_ar < EYE_BLINK_HEIGHT) and (eyeL_ar > EYE_BLINK_HEIGHT):
        winkedR = True
        if winkedL:
          print("L then R wink: UP")
          pyautogui.move(0, MOUSE_DELTA)
        else:
          print("R wink: RIGHT")
          pyautogui.move(MOUSE_DELTA, 0)

      winkedL, winkedL_frames = timeout_double(winkedL, winkedL_frames)
      winkedR, winkedR_frames = timeout_double(winkedR, winkedR_frames)

cap.release()
