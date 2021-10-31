import bluetooth

if __name__ == '__main__':
    nearby_devices = bluetooth.discover_devices(lookup_names=False)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))