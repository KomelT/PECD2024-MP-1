# PECD2024-MP-1

Project for class PECD (Programming energy constrained devices), at FRI, University of Ljubljana.

## Wiring

![Wiring diagram](https://raw.githubusercontent.com/KomelT/PECD2024-MP-1/refs/heads/main/wiring/wiring.png)

## Raspberry PI energy saving

- **Using simple OS**
  - Alpine Linux
- **Disabe 3 cores**
  - Adding `maxcpus=1` into `/boot/firmware/cmdline.txt`
- **Disable USB controller**
  - `echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind`

## Disclaimer

### This app was created for educational purposes only, don't use the app or any code from the app in real life!! Creators aren't liable for any damages done by using code from this repository.

## Authors

- Tilen Komel
- Telmo Sendino Sainz
