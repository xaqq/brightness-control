#!/usr/bin/env python
import pyinotify


# This is the device that tools write to (ie the incorrect one)
WATCH_PATH = "/sys/devices/pci0000:00/0000:00:02.0/backlight/acpi_video0/"

# This is the device that really controls the brightness
VALID_DEVICE = "/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight/"

# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()

mask = pyinotify.IN_MODIFY | pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

def get_value(filepath):
    with open(filepath) as f:
        return int(f.read())

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):

        max_acpi = get_value(WATCH_PATH + "max_brightness")
        cur_acpi = get_value(WATCH_PATH + "brightness")
        avg = float(cur_acpi) / max_acpi

        max_intel = get_value(VALID_DEVICE + "max_brightness")
        val_intel = max_intel * avg
        
        with open(VALID_DEVICE + "brightness", "w") as f:
            f.write(str(int(val_intel)))

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(WATCH_PATH, mask, rec=True)
notifier.loop()
