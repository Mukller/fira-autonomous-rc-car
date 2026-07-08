/*
 * Camera mount for Raspberry Pi Camera Module 3, for the NITROUS chassis
 * (models/Print-01_DKS-Pro_DukeDoks_Main-body_One-piece-Body).
 *
 * The original NITROUS model has no camera bracket at all -- the author
 * built it as a manual RC car with a custom ESP32 board, no camera. This
 * is a fresh design, not adapted from any external source.
 *
 * Camera board dimensions and hole pattern are read directly from the
 * official Raspberry Pi mechanical drawing (see doc comment below), not
 * guessed. Because reading exact hole-to-hole pitch off a technical PDF
 * without the physical board in hand carries some risk of a small error,
 * this design uses SLOTS instead of tight-fit holes for the camera board
 * mounting screws -- a few mm of horizontal slack means a misread pitch of
 * 1-2mm won't make the part useless, whereas a precise round hole would.
 *
 * Source of dimensions: official Raspberry Pi Camera Module 3 Standard
 * mechanical drawing, https://datasheets.raspberrypi.com/camera/camera-module-3-standard-mechanical-drawing.pdf
 * Board envelope: 25 x 23.862mm. Mounting holes: 4x diameter 2.2mm on
 * ~21.6mm x ~20.8mm pitch (read off the drawing; verify against your
 * physical unit before drilling any TIGHT-fit hole pattern -- the slots
 * below are deliberately oversized for this reason).
 *
 * STATUS: NOT COMPILED. No OpenSCAD installation was available in this
 * environment (chocolatey install failed on a permissions/lock error, and
 * installing software system-wide without confirmation felt like the
 * wrong call for a throwaway CAD check). Written carefully with only
 * basic primitives (cube/cylinder/translate/rotate/difference/union) that
 * are unlikely to have syntax errors, but treat this as a first draft:
 * OPEN IT IN OPENSCAD AND VISUALLY CHECK BEFORE SLICING/PRINTING.
 * See roadmap issue #3.
 */

// ---- Parameters (all mm) ----

// Camera board (official RPi Camera Module 3 drawing)
cam_board_x = 25;
cam_board_y = 23.862;
cam_board_thickness = 1.5;     // PCB thickness, approximate
cam_hole_dia = 2.2;            // mounting hole diameter on the board
cam_slot_width = 4.5;          // oversized slot width for tolerance
cam_slot_length = 6;           // slot length (horizontal play)
cam_hole_pitch_x = 21.6;       // approx horizontal hole-to-hole spacing
cam_hole_pitch_y = 20.8;       // approx vertical hole-to-hole spacing
cam_lens_hole_dia = 8;         // clearance hole behind the lens (>5.75mm pad)

// Mounting post (attaches to the chassis top, e.g. near
// Print-10_Central-Axis or Print-11_Bridge -- the tallest existing part
// is 61mm, this post is deliberately independent of that so it can be
// glued/screwed wherever the assembled chassis has clearance)
post_height = 45;
post_width = 12;
post_depth = 8;

// Base plate that sits on the chassis and gets screwed/glued down
base_x = 30;
base_y = 20;
base_thickness = 4;
base_screw_hole_dia = 3.2;     // for M3 self-tapping screws into the chassis
base_screw_inset = 4;          // distance of screw holes from base edge

// Camera head plate, tilted down toward the track
head_tilt_deg = 15;            // downward tilt so the camera looks at the
                                // track ahead, not the horizon -- adjust
                                // once the camera is actually mounted and
                                // the perspective calibration (tools/
                                // calibrate_camera.py) shows what's needed
head_plate_thickness = 3;

module base_plate() {
    difference() {
        cube([base_x, base_y, base_thickness]);
        for (x = [base_screw_inset, base_x - base_screw_inset])
            for (y = [base_screw_inset, base_y - base_screw_inset])
                translate([x, y, -1])
                    cylinder(h = base_thickness + 2, d = base_screw_hole_dia, $fn = 24);
    }
}

module post() {
    translate([(base_x - post_width) / 2, (base_y - post_depth) / 2, base_thickness])
        cube([post_width, post_depth, post_height]);
}

module camera_head_plate() {
    difference() {
        cube([cam_board_x + 6, cam_board_y + 6, head_plate_thickness]);

        // Lens clearance hole, centered
        translate([(cam_board_x + 6) / 2, (cam_board_y + 6) / 2, -1])
            cylinder(h = head_plate_thickness + 2, d = cam_lens_hole_dia, $fn = 32);

        // Mounting slots (oversized on purpose, see header comment)
        for (dx = [-cam_hole_pitch_x / 2, cam_hole_pitch_x / 2])
            for (dy = [-cam_hole_pitch_y / 2, cam_hole_pitch_y / 2])
                translate([(cam_board_x + 6) / 2 + dx, (cam_board_y + 6) / 2 + dy, -1])
                    hull() {
                        translate([-cam_slot_length / 2, 0, 0])
                            cylinder(h = head_plate_thickness + 2, d = cam_slot_width, $fn = 24);
                        translate([cam_slot_length / 2, 0, 0])
                            cylinder(h = head_plate_thickness + 2, d = cam_slot_width, $fn = 24);
                    }
    }
}

module camera_mount_assembly() {
    base_plate();
    post();

    // Camera head plate sits on top of the post, tilted down toward the
    // track. Rotated around the X axis so the front edge (toward the
    // track) dips down by head_tilt_deg.
    translate([(base_x - (cam_board_x + 6)) / 2, (base_y - (cam_board_y + 6)) / 2,
               base_thickness + post_height])
        rotate([head_tilt_deg, 0, 0])
            camera_head_plate();
}

camera_mount_assembly();
