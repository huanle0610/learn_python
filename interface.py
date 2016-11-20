"""get all inv4 address"""

from netifaces import interfaces, ifaddresses, AF_INET


def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        # print(ifaddresses(interface))
        if AF_INET not in ifaddresses(interface):
            continue

        for link in ifaddresses(interface)[AF_INET]:
            ip_list.append(link['addr'])

    return ip_list


if __name__ == '__main__':
    print("amtf")
    my_ip_list = ip4_addresses()
    print(my_ip_list)
