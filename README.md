brightness-control
==================

Python script to fix brightness control.

On some Optimus sytem, graphical tools to control brightness will write to `/sys/class/backlight/acpi_video0/brightness`. However, this isn't always the file that really controls the brightness.

This script is here to act as a bridge and to forward brightness update to the correct file.


How to use
==========

Just make `brigthnessd.py` autostart.

Systemd instruction:
Copy the `brightnessd.py` somewhere on your system. Edit the `brightnessd.service` file so that 
`ExecStart` points to the correct file. Then enable the service: `systemctl enable brightnessd`.
