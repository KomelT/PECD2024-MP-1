# Energy saving

## What we can do?

**Using simple OS**
- Raspberry PI OS Lite
- Alpine Linux

**Disabe 3 cores**
- Adding `maxcpus=1` into `/boot/firmware/cmdline.txt`

**Clock Down the CPU**
- Setting CPU to "preset": `"powersave"| sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`
  OR
- Manually specifaying frequency, appending code below into `/boot/firmware/config.txt`:

```
[all]
arm_freq=900
arm_freq_max=900
```

**Disable USB controller**
- `echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind`

**Disable Wi-Fi**\
Add code bellow into `/boot/firmware/config.txt`:

```bash
[all]
dtoverlay=disable-wifi
```

**Disable Bluetooth**\
Add code bellow into `/boot/firmware/config.txt`:

```bash
[all]
dtoverlay=disable-bt
```

**Disable HDMI**
- `vcgencmd display_power 0 3 %% vcgencmd display_power 0 7`

**Disable RJ45 port**
- `ip link set eth0 down`

**Disable Onboard LEDs**\
Add code bellow into `/boot/firmware/config.txt`:

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

**Disabling WAKE_ON_GPIO**\
Edit `WAKE_ON_GPIO` to `0`, with `rpi-eeprom-config --edit`.

## What does the numbers say?

**OS**\
We have performed the test with 3 different OSes. Power draw was mesaured 3 minutes after boot for 50s with enabled Wi-Fi.

- Alpine Linux 1827.28 mW
- Raspberry PI OS 1795.26 mW
- Raspberry PI Lite 1774.07 mW

Consclusion: We thought Alpine Linux will perform the best, but it actually didn't. We will use Raspberry PI Lite for other test and for final product.

**Cores**\
Again power was mesaured 3 minutes after boot for 50s with enabled Wi-Fi, but this time with only one core enabled.

Power usage was: 1705.58 mW, which isn't signiicant power optimization, but let them disabled for now.

**Underclocking**\
While idling the power usage was 1505.35 mW, which is an improvement.

**USB**\
We tried to disable USBs, but it didnt made difference, with power usage, so we left USBs enabled.

**Bluetooth**\
Same was with Bluetooth. We didn't saw a difference.

**HDMI**\
Same was with HDMI. We didn't saw a difference.

**Onboard LEDs**\
Same was with LEDs. They use so small amount of power that we didn't saw a difference.

**Peripherals**\
With sensor / buzzer / ADC just plugged it we didn't notice any biger power draw.

**ATtiny85**\
We mesaured it by itself and it used 43 mW.

**Optimizing power off**\
When RPI is powered down with default settings it uses: __ mW\
But if we edit `WAKE_ON_GPIO` it uses: __ mW

## Resources

- https://ucilnica.fri.uni-lj.si/mod/page/view.php?id=53513
- https://blues.com/blog/tips-tricks-optimizing-raspberry-pi-power/
- https://stackoverflow.com/questions/23487728/ethernet-disabling-in-raspberry-pi#answer-23530711
- https://raspberrypi.stackexchange.com/questions/104944/rpi-4-consumes-2-5w-when-shut-down#128100
