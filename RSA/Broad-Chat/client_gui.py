import socket
import threading
import tkinter as tk
from rsa import RSA

# ── Network setup ──────────────────────────────────────────────────────────────
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

rsa = RSA()
keys = client.recv(1024).decode().split(",")
rsa.e = int(keys[0])
rsa.N = int(keys[1])
rsa.d = int(keys[2])

# ── GUI ────────────────────────────────────────────────────────────────────────
BG = "#0f0f0f"
PANEL = "#1a1a1a"
ACCENT = "#2563eb"
TEXT = "#f0f0f0"
MUTED = "#666666"
ENTRY_BG = "#1f1f1f"
BORDER = "#2a2a2a"

root = tk.Tk()
root.title("Broad-Chat")
root.geometry("480x800")
root.configure(bg=BG)
root.resizable(False, False)

# ── Header ─────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=PANEL, height=64)
header.pack(fill=tk.X)
header.pack_propagate(False)

status_dot = tk.Canvas(header, width=10, height=10, bg=PANEL, highlightthickness=0)
status_dot.pack(side=tk.LEFT, padx=(20, 6), pady=20)
status_dot.create_oval(1, 1, 9, 9, fill="#22c55e", outline="")

tk.Label(
    header, text="Broad-Chat", font=("Georgia", 15, "bold"), bg=PANEL, fg=TEXT
).pack(side=tk.LEFT, pady=20)

tk.Label(header, text="RSA Encrypted", font=("Courier", 9), bg=PANEL, fg=MUTED).pack(
    side=tk.RIGHT, padx=20, pady=20
)

tk.Frame(root, bg=BORDER, height=1).pack(fill=tk.X)

# ── Name prompt overlay ────────────────────────────────────────────────────────
name_frame = tk.Frame(root, bg=BG)
name_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    name_frame, text="What is your name?", font=("Georgia", 14), bg=BG, fg=TEXT
).pack(pady=(0, 12))

name_entry = tk.Entry(
    name_frame,
    font=("Courier", 13),
    bg=ENTRY_BG,
    fg=TEXT,
    insertbackground=TEXT,
    relief=tk.FLAT,
    highlightthickness=1,
    highlightcolor=ACCENT,
    highlightbackground=BORDER,
    width=22,
)
name_entry.pack(ipady=8, pady=(0, 12))
name_entry.focus()

user_name = tk.StringVar()

# ── Chat area ──────────────────────────────────────────────────────────────────
chat_frame = tk.Frame(root, bg=BG)

# ✅ Plain Text widget — no scrollbar
chat_box = tk.Text(
    chat_frame,
    state=tk.DISABLED,
    font=("Courier", 11),
    bg=BG,
    fg=TEXT,
    relief=tk.FLAT,
    wrap=tk.WORD,
    padx=16,
    pady=12,
    spacing3=6,
    highlightthickness=0,
    bd=0,
)
chat_box.pack(fill=tk.BOTH, expand=True)

# colour tags
chat_box.tag_config("me", foreground="#93c5fd", font=("Courier", 11, "bold"))
chat_box.tag_config("friend", foreground="#86efac", font=("Courier", 11, "bold"))
chat_box.tag_config("msg", foreground=TEXT, font=("Courier", 11))
chat_box.tag_config("system", foreground=MUTED, font=("Courier", 10, "italic"))

# ── Bottom input bar ────────────────────────────────────────────────────────────
bottom = tk.Frame(root, bg=PANEL, height=64)

input_frame = tk.Frame(
    bottom,
    bg=ENTRY_BG,
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
)
input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 8), pady=12)

msg_entry = tk.Entry(
    input_frame,
    font=("Courier", 12),
    bg=ENTRY_BG,
    fg=TEXT,
    relief=tk.FLAT,
    insertbackground=TEXT,
    bd=4,
)
msg_entry.pack(fill=tk.BOTH, expand=True)


def send_message(event=None):
    msg = msg_entry.get().strip()
    if not msg:
        return
    name = user_name.get()
    full = f"[{name}]: {msg}"

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "You", "me")
    chat_box.insert(tk.END, f"  {msg}\n", "msg")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

    encrypted = rsa.encrypt(full)
    encrypted_str = ",".join(map(str, encrypted))
    client.send(encrypted_str.encode())
    msg_entry.delete(0, tk.END)


send_btn = tk.Button(
    bottom,
    text="Send",
    font=("Courier", 11, "bold"),
    bg=ACCENT,
    fg="white",
    relief=tk.FLAT,
    activebackground="#1d4ed8",
    activeforeground="white",
    cursor="hand2",
    padx=18,
    command=send_message,
)
send_btn.pack(side=tk.RIGHT, padx=(0, 16), pady=12, ipady=4)

msg_entry.bind("<Return>", send_message)


# ── Receive thread ──────────────────────────────────────────────────────────────
def append_message(msg):
    chat_box.config(state=tk.NORMAL)
    if "]: " in msg:
        parts = msg.split("]: ", 1)
        label = parts[0].lstrip("[")
        text = parts[1]
        chat_box.insert(tk.END, label, "friend")
        chat_box.insert(tk.END, f"  {text}\n", "msg")
    else:
        chat_box.insert(tk.END, msg + "\n", "msg")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)


def receive():
    while True:
        try:
            raw = client.recv(65536).decode()
            ciphertext = list(map(int, raw.split(",")))
            msg = rsa.decrypt(ciphertext)
            root.after(0, append_message, msg)
        except:
            root.after(0, append_message, "⚠ Disconnected from server.")
            break


# ── Name confirmation ───────────────────────────────────────────────────────────
def confirm_name(event=None):
    name = name_entry.get().strip()
    if not name:
        return
    user_name.set(name)

    name_frame.place_forget()
    chat_frame.pack(fill=tk.BOTH, expand=True)
    bottom.pack(fill=tk.X, side=tk.BOTTOM)

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(
        tk.END, f"  Joined as {name}. Messages are RSA encrypted.\n", "system"
    )
    chat_box.config(state=tk.DISABLED)

    msg_entry.focus()

    t = threading.Thread(target=receive, daemon=True)
    t.start()


name_entry.bind("<Return>", confirm_name)

join_btn = tk.Button(
    name_frame,
    text="Join Chat",
    font=("Courier", 12, "bold"),
    bg=ACCENT,
    fg="white",
    relief=tk.FLAT,
    activebackground="#1d4ed8",
    activeforeground="white",
    cursor="hand2",
    padx=20,
    command=confirm_name,
)
join_btn.pack(ipady=6)

root.mainloop()
