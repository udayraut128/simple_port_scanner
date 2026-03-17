import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import nmap
from fpdf import FPDF
import threading

scanner = nmap.PortScanner()

# ---------- START SCAN ----------
def start_scan():
    target = entry.get().strip()

    if not target:
        messagebox.showerror("Error", "Enter target IP or domain")
        return

    output.delete(1.0, tk.END)

    thread = threading.Thread(target=scan, args=(target,))
    thread.start()


def scan(target):
    output.insert(tk.END, f"Scanning {target}...\n\n")

    try:
        scanner.scan(hosts=target, arguments="-T4 -F")

        for host in scanner.all_hosts():
            output.insert(tk.END, f"Host: {host}\n")
            output.insert(tk.END, f"State: {scanner[host].state()}\n\n")

            for proto in scanner[host].all_protocols():
                output.insert(tk.END, f"Protocol: {proto}\n")

                for port in scanner[host][proto]:
                    service = scanner[host][proto][port]
                    output.insert(
                        tk.END,
                        f"Port {port}: {service['state']} | {service['name']}\n"
                    )

            output.insert(tk.END, "\n--------------------------\n")

    except Exception as e:
        output.insert(tk.END, f"Error: {e}\n")


# ---------- SAVE TXT ----------
def save_txt():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w") as f:
            f.write(output.get(1.0, tk.END))


# ---------- SAVE PDF ----------
def save_pdf():
    file = filedialog.asksaveasfilename(defaultextension=".pdf")
    if file:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        for line in output.get(1.0, tk.END).split("\n"):
            pdf.multi_cell(0, 6, line)

        pdf.output(file)


# ---------- GUI ----------
root = tk.Tk()
root.title("Simple Nmap Scanner")
root.geometry("800x600")

tk.Label(
    root,
    text="Enter Target IP or Domain:",
    font=("Arial", 12)
).pack(pady=5)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(
    root,
    text="Start Scan",
    command=start_scan,
    bg="green",
    fg="white",
    font=("Arial", 12)
).pack(pady=10)

tk.Button(
    root,
    text="Save TXT",
    command=save_txt
).pack(pady=2)

tk.Button(
    root,
    text="Save PDF",
    command=save_pdf
).pack(pady=2)

output = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=90,
    height=25,
    font=("Consolas", 10)
)
output.pack(padx=10, pady=10)

root.mainloop()