import matplotlib.pyplot as plt


def show_protocol_chart(packet_data):
    protocol_count = {}

    for pkt in packet_data:
        proto = pkt["Protocol"]
        protocol_count[proto] = protocol_count.get(proto, 0) + 1

    labels = list(protocol_count.keys())
    sizes = list(protocol_count.values())

    plt.figure()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Protocol Distribution")
    plt.show()