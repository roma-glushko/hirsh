# Hirsh

📟 Resilient monitoring system that detects home utility outages in unreliable environments (e.g. IoT, RaspberryPi, etc).

Hirsh is designed and optimized for:

- 💪 resiliency, robustness and self-healing 
- 📟 running in resource-constrained IoT-like unstable environments
- ✨ easy installation, configuration and self-service

## Maturity

The project is in early MVP state. 

It's being actively tested using my [RaspberryPi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) under [the current unstable 🇺🇦 Ukrainian infrastructure conditions](https://www.ft.com/content/2be7ac39-530f-4c80-8363-f05ec37234eb).

## Setups

Hirsh can be executed in any IoT device or board computer that supports Linux-like OS and Python 3.9+.

- [Only Supported] Basic: The basic setup includes just the device.
    The device is plugged into the main electricity circuit/outlet along with a router that provides network connection for the device.
- UPS: TBU

## Monitors

In theory, you can track any utilities your home has (e.g. electricity, network, gas, water, etc.). 
However, in practice it's the easiest to track:

- network connection [Only Supported]
- electricity supply

## Notifications

Hirsh is notification agnostic application. It's designed to support rich variety of mediums.

### Telegram

The primary way to notify you about outages is via [Telegram bot](https://core.telegram.org/bots).
You need to create [a new bot](https://t.me/BotFather) and add it to a group or a channel.

### Will Add Soon

This is the list of notification sources that will be [added next](https://github.com/roma-glushko/hirsh/issues?q=is%3Aissue+is%3Aopen+label%3Anotifiers).

## How does it work?

Technically, Hirhs is an [asyncio](https://docs.python.org/3/library/asyncio.html) Python3 daemon. 
It uses SQLite to persist gathered information, process and keep you notified.


## References

### Similar Projects

- https://github.com/fabytm/Outage-Detector
- https://github.com/nestukh/rpi-powerfail
- https://www.kc4rcr.com/power-outage-notification/
- https://homediyelectronics.com/projects/raspberrypi/poweroffdelay/powerfail
- https://projects-raspberry.com/power-outage-sensor/
- https://raspberrypi.stackexchange.com/questions/13538/raspberry-pi-to-email-when-power-outage-occurs

### Python + RPi

- https://medium.com/geekculture/gpio-programming-on-the-raspberry-pi-python-libraries-e12af7e0a812

### AsyncIO and RPi

- https://github.com/PierreRust/apigpio
- https://beenje.github.io/blog/posts/experimenting-with-asyncio-on-a-raspberry-pi/
- https://www.digikey.bg/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c
- https://docs.micropython.org/en/latest/library/uasyncio.html

### Deployment

- https://github.com/beenje/legomac