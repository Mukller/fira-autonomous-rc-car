"""Calibrate camera intrinsics from a set of chessboard photos.

Standard OpenCV camera calibration (cv2.calibrateCamera over detected
chessboard corners) — this is generic, well-documented OpenCV usage, not
adapted from any of the referenced repositories.

Usage:
    1. Print a chessboard pattern (default assumes a 9x6 internal-corner
       board — adjust --cols/--rows to match whatever you printed).
    2. Take 15-20 photos of it with the actual onboard camera, at varied
       angles/distances, and put them in one directory.
    3. Run:
         python tools/calibrate_camera.py --images-dir path/to/photos \
             --output config/camera_intrinsics.yaml

The output feeds lane_detection_node.py's camera_matrix/dist_coeffs
(currently None placeholders — see roadmap issue #2).

Not runnable end-to-end yet in this repo: no photos of the actual onboard
camera exist because no camera has been mounted (roadmap issue #1/#3).
This script itself is complete and has no missing pieces — it just has no
input data to run against yet.
"""

import argparse
import glob
import os

import cv2
import numpy as np
import yaml


def calibrate(images_dir: str, cols: int, rows: int, square_size_mm: float):
    objp = np.zeros((rows * cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2) * square_size_mm

    obj_points = []
    img_points = []
    image_size = None

    image_paths = sorted(
        glob.glob(os.path.join(images_dir, '*.jpg'))
        + glob.glob(os.path.join(images_dir, '*.png'))
    )
    if not image_paths:
        raise SystemExit(f'No images found in {images_dir}')

    used = 0
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image_size = gray.shape[::-1]

        found, corners = cv2.findChessboardCorners(gray, (cols, rows))
        if not found:
            print(f'  chessboard NOT found in {os.path.basename(path)}')
            continue

        criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)

        obj_points.append(objp)
        img_points.append(corners)
        used += 1
        print(f'  chessboard found in {os.path.basename(path)}')

    if used < 5:
        raise SystemExit(
            f'Only {used} usable images — need at least 5-10 for a '
            'reliable calibration, ideally 15-20 at varied angles.'
        )

    rms, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(
        obj_points, img_points, image_size, None, None)

    print(f'Calibration RMS reprojection error: {rms:.4f} '
          '(lower is better; > 1.0 usually means retake photos)')
    return camera_matrix, dist_coeffs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--images-dir', required=True)
    parser.add_argument('--cols', type=int, default=9,
                         help='internal chessboard corners, horizontal')
    parser.add_argument('--rows', type=int, default=6,
                         help='internal chessboard corners, vertical')
    parser.add_argument('--square-size-mm', type=float, default=25.0)
    parser.add_argument('--output', default='config/camera_intrinsics.yaml')
    args = parser.parse_args()

    camera_matrix, dist_coeffs = calibrate(
        args.images_dir, args.cols, args.rows, args.square_size_mm)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w') as f:
        yaml.safe_dump({
            'camera_matrix': camera_matrix.tolist(),
            'dist_coeffs': dist_coeffs.tolist(),
        }, f)

    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
