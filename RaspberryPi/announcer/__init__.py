# Written by Aaron Cohen -- 1/14/2013
# Brought to you by BitTorrent, Inc.
# "We're not just two guys in a basement in Sweden." TM
#
# This work is licensed under a Creative Commons Attribution 3.0 Unported License.
# See: http://creativecommons.org/licenses/by/3.0/

import sys
import re
import socket
import time
import struct
import threading


def ip_is_local(ip_string):
    """
    Uses a regex to determine if the input ip is on a local network. Returns a boolean. 
    It's safe here, but never use a regex for IP verification if from a potentially dangerous source.
    """
    combined_regex = "(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)|(^239\.255\.)"
    return re.match(combined_regex, ip_string) is not None # is not None is just a sneaky way of converting to a boolean


def get_local_ip():
    """
    Returns the first externally facing local IP address that it can find.

    Even though it's longer, this method is preferable to calling socket.gethostbyname(socket.gethostname()) as
    socket.gethostbyname() is deprecated. This also can discover multiple available IPs with minor modification.
    We excludes 127.0.0.1 if possible, because we're looking for real interfaces, not loopback.

    Some linuxes always returns 127.0.1.1, which we don't match as a local IP when checked with ip_is_local().
    We then fall back to the uglier method of connecting to another server.
    """

    # socket.getaddrinfo returns a bunch of info, so we just get the IPs it returns with this list comprehension.
    local_ips = [ x[4][0] for x in socket.getaddrinfo(socket.gethostname(), 80)
                  if ip_is_local(x[4][0]) ]

    # select the first IP, if there is one.
    local_ip = local_ips[0] if len(local_ips) > 0 else None

    # If the previous method didn't find anything, use this less desirable method that lets your OS figure out which
    # interface to use.
    if not local_ip:
        # create a standard UDP socket ( SOCK_DGRAM is UDP, SOCK_STREAM is TCP )
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Open a connection to one of Google's DNS servers. Preferably change this to a server in your control.
            temp_socket.connect(('8.8.8.8', 9))
            # Get the interface used by the socket.
            local_ip = temp_socket.getsockname()[0]
        except socket.error:
            # Only return 127.0.0.1 if nothing else has been found.
            local_ip = "127.0.0.1"
        finally:
            # Always dispose of sockets when you're done!
            temp_socket.close()
    return local_ip

def create_socket(multicast_ip, port):
    """
    Creates a socket, sets the necessary options on it, then binds it. The socket is then returned for use.
    """

    local_ip = get_local_ip()

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
    my_socket.bind(('0.0.0.0', port))

    return my_socket

def get_bound_multicast_interface(my_socket):
    """
    Returns the IP address (probably your local IP) that the socket is bound to for multicast.
    Note that this may not be the same address you bound to manually if you specified 0.0.0.0.
    This isn't used here, just a useful utility method.
    """
    response = my_socket.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF)
    socket.inet_ntoa(struct.pack('i', response))

def drop_multicast_membership(my_socket, multicast_ip):
    """
    Drops membership to the specified multicast group without closing the socket.
    Note that this happens automatically (done by the kernel) if the socket is closed.
    """


    local_ip = get_local_ip()

    # Must reconstruct the same request used when adding the membership initially
    membership_request = socket.inet_aton(multicast_ip) + socket.inet_aton(local_ip)

    # Leave group
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, membership_request)

# def listen_loop(multicast_ip, port):
#     my_socket = create_socket(multicast_ip, port+1)

#     while True:
#         # Data waits on socket buffer until we retrieve it.
#         # NOTE: Normally, you would want to compare the incoming data's source address to your own, and filter it out
#         #       if it came rom the current machine. Everything you send gets echoed back at you if your socket is
#         #       subscribed to the multicast group.
#         data, address = my_socket.recvfrom(4096)
#         print ("%s says the time is %s" % (address, data))

def allIps()
    ip_addresses = []
    for x in socket.getaddrinfo(socket.gethostname(), 80):
        for ip in x
            ip_addresses.append(ip)
    return ip_addresses

def create_sockets(multicast_ip, port):
    """
    Creates a socket, sets the necessary options on it, then binds it. The socket is then returned for use.
    """
    ip_addresses = allIps()
    print (ip_addresses)
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
    my_sockets = create_sockets(multicast_address, multicast_port+1)

    while True:
        if (_announce):
            # Send data. Destination must be a tuple containing the ip and port.
            for my_socket in my_sockets:
                my_socket.sendto(bytes([1,2,3,4]), (multicast_address, multicast_port))

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
    