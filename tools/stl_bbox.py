"""Print the bounding-box dimensions of every part under models/.

No external dependencies (numpy-stl not assumed to be installed) — parses
binary STL directly. Used to produce the dimension table in
docs/electronics-bom.md; rerun after any model changes to keep that table
accurate.

Usage: python tools/stl_bbox.py
"""

import glob
import os
import struct


def read_binary_stl_bbox(path):
    with open(path, 'rb') as f:
        f.read(80)  # header
        n_tri_bytes = f.read(4)
        if len(n_tri_bytes) < 4:
            return None
        n_tri = struct.unpack('<I', n_tri_bytes)[0]
        minx = miny = minz = float('inf')
        maxx = maxy = maxz = float('-inf')
        for _ in range(n_tri):
            data = f.read(50)
            if len(data) < 50:
                break
            vals = struct.unpack('<12fH', data)
            verts = vals[3:12]
            for j in range(0, 9, 3):
                x, y, z = verts[j], verts[j + 1], verts[j + 2]
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)
                minz, maxz = min(minz, z), max(maxz, z)
        return minx, miny, minz, maxx, maxy, maxz, n_tri


def is_ascii_stl(path):
    with open(path, 'rb') as f:
        return f.read(5) == b'solid'


def main():
    base = os.path.join(os.path.dirname(__file__), '..', 'models')
    files = sorted(glob.glob(os.path.join(base, 'Print-*', '*.stl')))
    for f in files:
        if is_ascii_stl(f):
            print(f'{os.path.basename(f)} -> ASCII STL, skip binary parse')
            continue
        bbox = read_binary_stl_bbox(f)
        if not bbox:
            continue
        minx, miny, minz, maxx, maxy, maxz, n = bbox
        dx, dy, dz = maxx - minx, maxy - miny, maxz - minz
        print(
            f'{os.path.basename(f):55s} '
            f'X={dx:8.2f} Y={dy:8.2f} Z={dz:8.2f} tris={n}'
        )


if __name__ == '__main__':
    main()
