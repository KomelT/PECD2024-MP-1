# PECD2024-MP-1

Project for class PECD (Programming energy constrained devices), at FRI, University of Ljubljana.

## Running

### Server

```bash
cd server

docker compose build

docker compose up -d
```

### App

```bash
cd app

nano main.py # edit server address

cp planter.service /etc/systemd/system/planter.service

apt install python3-pip python3-picamera2 -y

pip3 install -r requirements.txt

systemctl enable planter.service

systemctl start planter.service
```

## Wiring

![Wiring diagram](https://raw.githubusercontent.com/KomelT/PECD2024-MP-1/refs/heads/main/wiring/wiring.png)

## [Raspberry PI energy saving](https://github.com/KomelT/PECD2024-MP-1/tree/main/energy_saving)

## Disclaimer

### This app was created for educational purposes only, don't use the app or any code from the app in real life!! Creators aren't liable for any damages done by using code from this repository.

## Authors

- Tilen Komel
- Telmo Sendino Sainz
