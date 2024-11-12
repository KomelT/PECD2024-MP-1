# Energy saving

## What we can do?

**Using simple OS**

- Alpine Linux

**Disabe 3 cores**

- Adding `maxcpus=1` into `/boot/firmware/cmdline.txt`

**Clock Down the CPU**

- Setting CPU to "preset": `"powersave"| sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`
  OR
- Manually specifaying frequency, appending code below into `/boot/config.txt`:

```
[all]
arm_freq=900
arm_freq_max=900
```

**Disable USB controller**

- `echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind`

**Disable Wi-Fi**
Add code bellow into `/boot/config.txt`:

```bash
[all]
dtoverlay=disable-wifi
```

**Disable Bluetooth**
Add code bellow into `/boot/config.txt`:

```bash
[all]
dtoverlay=disable-bt
```

**Disable HDMI**

- `sudo /opt/vc/bin/tvservice -o`

**Disable RJ45 port**

- Disable networking: `/etc/init.d/networking stop`
- Power down USB chip: `echo 0x0 > /sys/devices/platform/bcm2708_usb/buspower`

**Disable Onboard LEDs**
Add code bellow into `/boot/config.txt`:

```bash
[pi4]
# Disable the PWR LED
dtparam=pwr_led_trigger=none
dtparam=pwr_led_activelow=off
# Disable the Activity LED
dtparam=act_led_trigger=none
dtparam=act_led_activelow=off
# Disable ethernet port LEDs
dtparam=eth_led0=4
dtparam=eth_led1=4
```

## What does the numbers say?

## Resources

- https://ucilnica.fri.uni-lj.si/mod/page/view.php?id=53513
- https://blues.com/blog/tips-tricks-optimizing-raspberry-pi-power/
- https://stackoverflow.com/questions/23487728/ethernet-disabling-in-raspberry-pi#answer-23530711
