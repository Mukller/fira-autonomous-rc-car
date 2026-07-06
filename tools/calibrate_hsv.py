"""Interactive HSV threshold tuner for the yellow/white lane-line color mask.

Opens a camera feed (or a still image) with OpenCV trackbars for
H/S/V min/max, shows the resulting mask live, and prints the final range on
exit — mirrors a standard OpenCV HSV-tuning pattern (independent of the
fixed HSV constants baked into external/pandas-team-avis-engine, which were
tuned for the simulator's rendering, not for real-world lighting).

Usage:
    python tools/calibrate_hsv.py --camera 0
    python tools/calibrate_hsv.py --image path/to/track_photo.jpg

Controls: adjust the six trackbars until only the lane line is white in the
"mask" window, then press 'q' to print the resulting HSV range (paste it
into lane_detection_node.py's color-mask logic once that's implemented for
the color-based approach, alongside the edge-based approach already there).

Not runnable end-to-end yet in this repo: no physical camera or track photo
exists (roadmap issues #1/#3/#8) — this is the tool that will be used once
they do.
"""

import argparse

import cv2
import numpy as np


def nothing(_):
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--camera', type=int, default=None,
                         help='camera device index, e.g. 0')
    parser.add_argument('--image', type=str, default=None,
                         help='path to a still image instead of a camera')
    args = parser.parse_args()

    if args.image is None and args.camera is None:
        raise SystemExit('Pass either --camera or --image')

    cap = None
    still_frame = None
    if args.image is not None:
        still_frame = cv2.imread(args.image)
        if still_frame is None:
            raise SystemExit(f'Could not read image: {args.image}')
    else:
        cap = cv2.VideoCapture(args.camera)
        if not cap.isOpened():
            raise SystemExit(f'Could not open camera index {args.camera}')

    cv2.namedWindow('trackbars')
    for name, default, maxval in [
        ('H min', 0, 179), ('H max', 179, 179),
        ('S min', 0, 255), ('S max', 255, 255),
        ('V min', 0, 255), ('V max', 255, 255),
    ]:
        cv2.createTrackbar(name, 'trackbars', default, maxval, nothing)

    last_range = None
    while True:
        if still_frame is not None:
            frame = still_frame.copy()
        else:
            ok, frame = cap.read()
            if not ok:
                print('Camera read failed, stopping.')
                break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([
            cv2.getTrackbarPos('H min', 'trackbars'),
            cv2.getTrackbarPos('S min', 'trackbars'),
            cv2.getTrackbarPos('V min', 'trackbars'),
        ])
        upper = np.array([
            cv2.getTrackbarPos('H max', 'trackbars'),
            cv2.getTrackbarPos('S max', 'trackbars'),
            cv2.getTrackbarPos('V max', 'trackbars'),
        ])
        last_range = (lower, upper)

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('result', result)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

    if last_range is not None:
        lower, upper = last_range
        print(f'lower = np.array({lower.tolist()})')
        print(f'upper = np.array({upper.tolist()})')


if __name__ == '__main__':
    main()
