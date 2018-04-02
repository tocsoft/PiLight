import sys
import re
import socket
import time
import struct
import threading
import fcntl

def get_ip_address( NICname ):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', NICname[:15].encode("UTF-8"))
    )[20:24])

def nic_info():
    """
    Return a list with tuples containing NIC and IPv4
    """
    nic = []

    for ix in socket.if_nameindex():
        name = ix[1]
        if(name != 'lo') :
            ip = get_ip_address( name )
            nic.append(ip)

    return nic

def create_sockets(multicast_ip, port):
    """
    Creates a socket, sets the necessary options on it, then binds it. The socket is then returned for use.
    """
    ip_addresses = nic_info()
    socketCollection = []
    for local_ip in ip_addresses :
        # create a UDP socket
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # allow reuse of addresses
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # set multicast interface to local_ip
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))

        # Set multicast time-to-live to 2...should keep our multicast packets from escaping the local network
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # Construct a membership request...tells router what multicast group we want to subscribe to
        membership_request = socket.inet_aton(multicast_ip) + socket.inet_aton(local_ip)

        # Send add membership request to socket
        # See http://www.tldp.org/HOWTO/Multicast-HOWTO-6.html for explanation of sockopts
        my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership_request)

        # Bind the socket to an interface.
        # If you bind to a specific interface on the Mac, no multicast data will arrive.
        # If you try to bind to all interfaces on Windows, no multicast data will arrive.
        # Hence the following.
        port += 1
        my_socket.bind((local_ip, port))
        socketCollection.append(my_socket)

    return socketCollection

_announce = False
def _loop():
    global _announce
    # Choose an arbitrary multicast IP and port.
    # 239.255.0.0 - 239.255.255.255 are for local network multicast use.
    # Remember, you subscribe to a multicast IP, not a port. All data from all ports
    # sent to that multicast IP will be echoed to any subscribed machine.
    multicast_address = "239.255.4.3"
    multicast_port = 1234
    # Offset the port by one so that we can send and receive on the same machine
    my_sockets = create_sockets(multicast_address, multicast_port)

    while True:
        if (_announce):
            # Send data. Destination must be a tuple containing the ip and port.
            for my_socket in my_sockets:
                my_socket.sendto("data".encode('utf8'), (multicast_address, multicast_port))

            time.sleep(15)
        else:
            time.sleep(1)

def start():
    global _announce
    _announce = True
    
def stop():
    global _announce
    _announce = False

_thread = threading.Thread(target=_loop, args=())
_thread.start()
    