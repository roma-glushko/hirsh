from outage_detector.daemon import Daemon

MONITORS = []

if __name__ == "__main__":
    outage_detector = Daemon(monitors=MONITORS)
    outage_detector.start()
