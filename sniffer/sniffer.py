import struct
import sys
import socket
# NEW
# import mail
from sniffer_tcp_2 import get_http

def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    # NEW
    id_dict = {"ID": 1}
    # /NEW
    while True:
        raw_data, addr = s.recvfrom(65535)
        eth_frame = ethernet(raw_data)
        # These if-statements print all the package information, from ethernet frame
        # , to ipv4 packet, to tcp packet, to http packet.
        if eth_frame[2] == 8:
            packet = ipv4(eth_frame[3])
            if packet[3] == 6:
                tcp_packet = tcp(packet[6])
                if len(tcp_packet[10]) > 0:
                    # if src or dest = 80, it's an http packet.
                    if tcp_packet[0] == 80 or tcp_packet[1] == 80:
                        http_packet = tcp_packet[10]
                        subnet = "192.168.137.0/24"
                        MAC_admin = "08:00:27:A8:D7:2F"
                        subnet_err = 0
                        mac_err = 0
                        http_err = 0
                        # NEW
                        # This enables a series in which the urls from the database
                        # are searched for inside the http packet.
                        result = http(http_packet, id_dict)
                        if result != 0:
                            http_err = 1
                        if inSubnet(subnet, packet[4]) != 1:
                            subnet_err = 1
                        if eth_frame[1] != MAC_admin:
                            mac_err = 1
                        # If a http_err is activated and either a subnet_err or mac_err
                        # a dict is created which will then be mailed.
                        if http_err and (subnet_err or mac_err):
                            toMail = {"subnet_err": subnet_err,
                                      "mac_err": mac_err, "http_err": http_err, "url": result["url"], "payload": http_packet}
                            print(toMail)
                        # /NEW
                        # if http_err and (subnet_err or mac_err):
                        #     if subnet_err:
                        #         mail.sendMail(
                        #             mail.getAlertType(2),
                        #             mail.getAlertSubject(
                        #                 1) + ", " + mail.getAlertSubject(2),
                        #             url,
                        #             eth_frame[1],
                        #             packet[4],
                        #             http_packet,
                        #             mail.tcpPacket(
                        #                 raw_data, eth_frame, packet, tcp_packet)
                        #         )
                        #
                        #     elif mac_err:
                        #         mail.sendMail(
                        #             mail.getAlertType(2),
                        #             mail.getAlertSubject(
                        #                 1) + ", " + mail.getAlertSubject(2),
                        #             url,
                        #             eth_frame[1],
                        #             packet[4],
                        #             http_packet,
                        #             mail.tcpPacket(
                        #                 raw_data, eth_frame, packet, tcp_packet)
                        #         )

# Uses the ethernet's frame header to grab the src and dest MAC
# and the ethernet prototype and returns this in the right format.


def ethernet(raw_data):
    dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
    new_src = get_mac(src)
    new_dest = get_mac(dest)
    src_format = new_src[0:2] + ":" + new_src[2:4] + ":" + new_src[4:6] + \
        ":" + new_src[6:8] + ":" + new_src[8:10] + ":" + new_src[10:12]
    dest_format = new_dest[0:2] + ":" + new_dest[2:4] + ":" + new_dest[4:6] + \
        ":" + new_dest[6:8] + ":" + new_dest[8:10] + ":" + new_dest[10:12]
    proto = socket.htons(prototype)
    data = raw_data[14:]
    return dest_format, src_format, proto, data

# Gets the ethernet's frame payload if it's an IPv4 package.
# Returs the version, header length, time to live, prototype
# source IP, destination IP and the packet's data.


def ipv4(raw_payload):
    version_header_length = raw_payload[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, dest = struct.unpack(
        '! 8x B B 2x 4s 4s', raw_payload[:20])
    new_src = get_ip(src)
    new_dest = get_ip(dest)
    data = raw_payload[header_length:]
    return version, header_length, ttl, proto, new_src, new_dest, data

# unpacks the TCP header, returns portnumbers, seq and ack number, flags and de packet's
# data.


def tcp(ipv4_payload):
    (src_port, dest_port, sequence, acknowledgment,
     length_reserved_flags) = struct.unpack('! H H L L H', ipv4_payload[:14])
    length = (length_reserved_flags >> 12) * 4
    flag_urg = (length_reserved_flags & 32) >> 5
    flag_ack = (length_reserved_flags & 16) >> 4
    flag_psh = (length_reserved_flags & 8) >> 3
    flag_rst = (length_reserved_flags & 4) >> 2
    flag_syn = (length_reserved_flags & 2) >> 1
    flag_fin = length_reserved_flags & 1
    data = ipv4_payload[length:]
    return src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data


def http(http_payload):
    return http_payload


def get_ip(addr):
    return '.'.join(map(str, addr))


def get_mac(addr):
    return addr.hex().upper()

# Next three functions are used to check if an ip is inside a subnet.
# Ip to binary


def ipToBit(ip):
    list_str = ip.split(".")
    list_int = list(map(int, list_str))
    list_int_r = list_int[::-1]
    list_int_p = []
    i = 0
    sum = 0
    for num in list_int_r:
        sum += (num * 256**i)
        i += 1
    return sum

# Mask to binary


def maskToBit(mask):
    mask_bin = ((~0) << (32 - int(mask)))
    return mask_bin


def inSubnet(subnet_and_mask, ip):
    ip_bin = ipToBit(ip)
    subnet_split = subnet_and_mask.split("/")
    subnet = subnet_split[0]
    subnet_bin = ipToBit(subnet)
    mask = subnet_split[1]
    mask_bin = maskToBit(mask)
    return (ip_bin & mask_bin) == (subnet_bin & mask_bin)

# NEW
# This function call the get_http function inside sniffer_tcp_2.


def http(payload, id_dict):
    id = id_dict.get("ID")
    result = get_http(payload, id)
    id += 1
    id_dict["ID"] = id
    return result

main()
