## iMouse

### Pan and tilt with your mouse using eye winks.

Run with: `python loop.py`

Exit with `CTRL + C`


Close your eyes as follows to move the mouse:
- Left: keep left eye closed
- Right: keep right eye closed
- Up: wink left eye, then keep right eye closed
- Down: wink right eye, then keep left eye closed

Change `CAMERA` to a higher integer if using multiple cameras; an external webcam 
might show up as device `1` or `2`.

Increase `MOUSE_DELTA` to make the mouse move faster.

Increase `EYE_BLINK_HEIGHT` for more sensitivity to pick up blinks.

Increase `WAIT_FRAMES` to recognize slower winking sequences with longer pauses.
