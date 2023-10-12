## iMouse

### Pan and tilt with your mouse using eye winks.

Run with: `python loop.py`

Exit with `CTRL + C`


Use your eyes as follows to move the mouse:
- Left: squint left eye
- Right: squint right eye
- Up: open both eyes wide
- Down: squint both eyes

Change `CAMERA` to a higher integer if using multiple cameras; an external webcam 
might show up as device `1` or `2`.

Increase `MOUSE_DELTA` to make the mouse move faster.

Increase `EYE_BLINK_HEIGHT` for more sensitivity to pick up squints.

Increase `EYE_SQUINT_HEIGHT` for less sensitivity to pick up wide open eyes.

Increase `WAIT_FRAMES` to recognize slower winking sequences with longer pauses.
