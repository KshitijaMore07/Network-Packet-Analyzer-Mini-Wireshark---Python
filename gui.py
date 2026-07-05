import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from queue import Queue

from packet_capture import start_sniffing, stop_sniffing
from session_manager import save_session, load_session
from charts import show_protocol_chart


# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("Mini Wireshark - Advanced Packet Analyzer")
root.geometry("1200x700")
root.configure(bg="#1e1e1e")


# =========================
# GLOBALS
# =========================
packet_data = []
packet_queue = Queue()

capture_running = False
packet_count = 0
selected_protocol = "ALL"
last_count = 0


# =========================
# TABLE
# =========================
columns = ("No", "Time", "IP Version", "Source IP", "Destination IP", "Protocol", "Size")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True, padx=10, pady=10)


# =========================
# LABELS
# =========================
counter_label = tk.Label(root, text="Captured: 0 Packets", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold"))
counter_label.pack()

pps_label = tk.Label(root, text="Packets/sec: 0", fg="cyan", bg="#1e1e1e", font=("Arial", 11))
pps_label.pack()


# =========================
# THREAD SAFE
# =========================
def add_packet(packet):
    packet_queue.put(packet)


# =========================
# UPDATE TABLE
# =========================
def update_table():
    global packet_count

    while not packet_queue.empty():
        packet = packet_queue.get()

        packet_data.append(packet)
        packet_count += 1

        tree.insert("", tk.END, values=tuple(packet.values()))

    counter_label.config(text=f"Captured: {packet_count} Packets")

    root.after(100, update_table)


# =========================
# PACKETS PER SECOND
# =========================
def update_pps():
    global last_count, packet_count

    pps = packet_count - last_count
    last_count = packet_count

    pps_label.config(text=f"Packets/sec: {pps}")

    root.after(1000, update_pps)


# =========================
# START CAPTURE
# =========================
def start_capture():
    global capture_running

    if capture_running:
        return

    capture_running = True
    start_sniffing(add_packet)


# =========================
# STOP CAPTURE
# =========================
def stop_capture():
    global capture_running

    capture_running = False
    stop_sniffing()
    messagebox.showinfo("Stopped", "Packet Capture Stopped")


# =========================
# CLEAR TABLE
# =========================
def clear_table():
    global packet_data, packet_count

    packet_data = []
    packet_count = 0

    for i in tree.get_children():
        tree.delete(i)

    counter_label.config(text="Captured: 0 Packets")


# =========================
# SEARCH
# =========================
def search_ip():
    query = search_entry.get()

    for i in tree.get_children():
        tree.delete(i)

    for pkt in packet_data:
        if query in pkt["Source IP"] or query in pkt["Destination IP"]:
            tree.insert("", tk.END, values=tuple(pkt.values()))


# =========================
# SAVE / LOAD
# =========================
def save_data():
    save_session(packet_data)
    messagebox.showinfo("Saved", "Session saved successfully")


def load_data():
    global packet_data, packet_count

    packet_data = load_session()

    for i in tree.get_children():
        tree.delete(i)

    packet_count = 0

    for pkt in packet_data:
        tree.insert("", tk.END, values=tuple(pkt.values()))
        packet_count += 1

    counter_label.config(text=f"Captured: {packet_count} Packets")


# =========================
# CHART
# =========================
def show_chart():
    if not packet_data:
        messagebox.showwarning("Empty", "No data available")
        return

    show_protocol_chart(packet_data)


# =========================
# SEARCH BOX
# =========================
search_frame = tk.Frame(root, bg="#1e1e1e")
search_frame.pack(pady=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

tk.Button(search_frame, text="Search IP", command=search_ip).pack(side="left")


# =========================
# BUTTONS
# =========================
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start", bg="green", fg="white", command=start_capture).pack(side="left", padx=5)
tk.Button(btn_frame, text="Stop", bg="red", fg="white", command=stop_capture).pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear", bg="gray", fg="white", command=clear_table).pack(side="left", padx=5)

tk.Button(btn_frame, text="Save", bg="purple", fg="white", command=save_data).pack(side="left", padx=5)
tk.Button(btn_frame, text="Load", bg="orange", fg="white", command=load_data).pack(side="left", padx=5)
tk.Button(btn_frame, text="Chart", bg="blue", fg="white", command=show_chart).pack(side="left", padx=5)


# =========================
# START LOOPS
# =========================
update_table()
update_pps()

root.mainloop()