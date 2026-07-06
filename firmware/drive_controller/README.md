# drive_controller firmware

Arduino sketch that turns `S<angle>` / `T<throttle>` serial commands from
`serial_bridge_node.py` into actual servo/motor PWM. See the header comment
in [`drive_controller.ino`](drive_controller.ino) for the protocol and
safety-timeout behaviour.

## Status

Written against the BOM in [`../../docs/electronics-bom.md`](../../docs/electronics-bom.md)
(MG90s servo, DC-motor 280 through a generic 2-direction H-bridge). **Not yet
tested on real hardware** — see roadmap issue #5. Pin numbers are
placeholders; update `STEERING_SERVO_PIN`, `MOTOR_IN1_PIN`, `MOTOR_IN2_PIN`,
`MOTOR_PWM_PIN` to match the actual wiring once the electronics from issue
#1 are on hand.

## Bring-up checklist (do this before trusting it on the physical car)

1. Bench-test the servo alone (wheels off the ground): send `S60`, `S90`,
   `S120` over the Serial Monitor and confirm it hits mechanical limits of
   `Print-09_Stearing` without binding.
2. Bench-test the motor alone (car up on blocks): send small `T` values
   first (`T0.2`) and confirm direction matches expectation before trying
   higher throttle.
3. Confirm the safety timeout actually cuts the motor: stop sending `T`
   commands and check power drops within `COMMAND_TIMEOUT_MS`.
4. Only after 1-3 pass, connect `serial_bridge_node.py` and test the full
   ROS pipeline with the car on blocks before a real track run.
