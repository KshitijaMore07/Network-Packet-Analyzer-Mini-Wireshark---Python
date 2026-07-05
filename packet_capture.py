from scapy.all import AsyncSniffer
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6
from datetime import datetime

packet_number = 0
sniffer = None


def get_packet_details(packet):
    global packet_number
    packet_number += 1

    ip_version = "N/A"
    source_ip = "N/A"
    destination_ip = "N/A"
    protocol = "Other"

    if packet.haslayer(IP):
        ip_version = "IPv4"
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

    elif packet.haslayer(IPv6):
        ip_version = "IPv6"
        source_ip = packet[IPv6].src
        destination_ip = packet[IPv6].dst

    if packet.haslayer(TCP):
        protocol = "TCP"
    elif packet.haslayer(UDP):
        protocol = "UDP"
    elif packet.haslayer(ICMP):
        protocol = "ICMP"

    return {
        "No": packet_number,
        "Time": datetime.now().strftime("%H:%M:%S"),
        "IP Version": ip_version,
        "Source IP": source_ip,
        "Destination IP": destination_ip,
        "Protocol": protocol,
        "Size": len(packet)
    }


def start_sniffing(callback):
    global sniffer

    def process(packet):
        packet_dict = get_packet_details(packet)
        callback(packet_dict)

    sniffer = AsyncSniffer(prn=process, store=False)
    sniffer.start()


def stop_sniffing():
    global sniffer
    if sniffer:
        sniffer.stop()