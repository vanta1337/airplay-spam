import socket
from time import sleep
import random
from zeroconf import *
from datetime import datetime
from randmac import RandMac

def getRandomString(str_size):
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(str_size))
try:
    prefix = input("Prefix: ")
    while True:
        name = getRandomString(21)
        rnd = random.randint(1, 255)
        example_mac = "00:00:00:00:00:00"
        generated_mac = RandMac(example_mac)

        desc = {
            "ft": "0xA7FFFF7,0xE",
            "pt": "0",
            "am": "VirtualMachine (1337 GmbH )",
            "vs": "5.3.2",
            "pf": "Windope 10",
            "deviceid": "08:00:27:7B:DE:F3",
            "pk": "96c57560c07e592c3276edd81aac695be11d148d45349e09b4660ec5ac11e4f3",
            "pi": "FC1990B7-A5E1-4A2F-9B39-9628E0662306",
            "os": "6.1.7601",
            "sf": "0x4"
        }
        
        info = ServiceInfo(
            type_ = "_airserver._tcp.local.",
            name = f"{prefix} $ {name}._airserver._tcp.local.",
            addresses = [socket.inet_aton("192.168.2.115")], port = 7000, host_ttl = 2, other_ttl = 2, properties=desc,
            server=f"{prefix} $ {name}.local."
        )
        
        airplay_desc = {
            "features": "0x5A7FFFF7,0x1E,0x4A7FFFF7",
            "srcvers": "220.68",
            "flags": "0x4",
            "deviceid": f"{generated_mac}",
            "vv": "2",
            "pk": "96c57560c07e592c3276edd81aac695be11d148d45349e09b4660ec5ac11e4f3",
            "model": "AppleTV5,3",
            "pi": "FC1990B7-A5E1-4A2F-9B39-9628E0662306"
        }
        
        airplay = ServiceInfo(
            type_ ="_airplay._tcp.local.",
            name =f"{prefix} $ {name}._airplay._tcp.local.",
            addresses =[socket.inet_aton("192.168.2.115")], port=7000, host_ttl = 2, other_ttl = 2, properties=airplay_desc,
            server=f"{prefix} $ {name}.local."
        )
        
        raop_desc = {
            "md": "0,1,2",
            "ft": "0xA7FFFF7,0xE",
            "cn": "0,1,2,3",
            "am": "AppleTV5,3",
            "tp": "UDP",
            "da": "true",
            "vs": "220.68",
            "vn": "65537",
            "vv": "2",
            "et": "0,3,5",
            "pk": "96c57560c07e592c3276edd81aac695be11d148d45349e09b4660ec5ac11e4f3",
            "sf": "0x4"
        }
        
        raop = ServiceInfo(
            type_ ="_raop._tcp.local.",
            name =f"0800277BDEF3@{name}._raop._tcp.local.",
            addresses =[socket.inet_aton("192.168.2.115")], port=5000, host_ttl = 2, other_ttl = 2, properties=raop_desc,
            server=f"{name}.local."
        )

        zeroconf = Zeroconf()
        print("Registering AirPlay Service...")
        zeroconf.register_service(info)
        zeroconf.register_service(airplay)
        zeroconf.register_service(raop)
        print(f"Service registered (Name: {prefix} $ {name})!")

except KeyboardInterrupt:
    pass
finally:
    print("Unregistering...")
    zeroconf.unregister_all_services()
    zeroconf.close()
