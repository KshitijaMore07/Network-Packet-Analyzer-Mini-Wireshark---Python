import csv
from tkinter import messagebox


def export_to_csv(packet_data):
    """
    Export packet data to a CSV file.
    """

    if not packet_data:
        messagebox.showwarning(
            "No Data",
            "No packet data available to export."
        )
        return

    filename = "captured_packets.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Header Row
        writer.writerow([
            "Packet No",
            "Time",
            "IP Version",
            "Source IP",
            "Destination IP",
            "Protocol",
            "Packet Size (Bytes)"
        ])

        # Data Rows
        for packet in packet_data:
            writer.writerow([
                packet["No"],
                packet["Time"],
                packet["IP Version"],
                packet["Source IP"],
                packet["Destination IP"],
                packet["Protocol"],
                packet["Size"]
            ])

    messagebox.showinfo(
        "Export Successful",
        f"Packet data exported successfully to:\n{filename}"
    )