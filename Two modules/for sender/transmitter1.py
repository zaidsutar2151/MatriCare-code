import sys, subprocess, time, random, socket, json
from collections import deque

# --- Auto install missing libs ---
for lib in ["matplotlib"]:
    try:
        __import__(lib)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

try:
    import tkinter as tk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])
    import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# -------- Config --------
PARAMS = ["SysBP", "DiaBP", "HR", "Temp", "SpO2", "RR", "FHR", "Toco"]
RANGES = {
    "SysBP": (100, 140), "DiaBP": (60, 90),
    "HR": (60, 120), "Temp": (36.5, 37.8),
    "SpO2": (92, 100), "RR": (12, 25),
    "FHR": (110, 160), "Toco": (0, 5)
}
SERVER_IP = "192.168.12.195"   # ✅ Receiver IP
PORT = 5000
UPDATE_MS = 1000  # 1 second update interval


# -------- TCP socket --------
def connect_tcp():
    """Try to connect to receiver socket."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, PORT))
        print("✅ Connected to Receiver at", SERVER_IP)
        return s
    except Exception as e:
        print("⚠️ Could not connect:", e)
        return None


# -------- GUI + Data --------
class MonitorSender:
    def __init__(self, root, sock):
        self.root = root
        self.sock = sock
        self.data = {p: deque(maxlen=30) for p in PARAMS}
        self.time_axis = deque(maxlen=30)
        self.start_time = time.time()

        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.axes = {}
        for i, p in enumerate(PARAMS):
            ax = self.fig.add_subplot(4, 2, i + 1)
            ax.set_title(p)
            ax.set_ylim(RANGES[p][0] - 5, RANGES[p][1] + 5)
            self.axes[p] = ax

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update()

    def generate_vitals(self):
        vitals = {}
        for p in PARAMS:
            lo, hi = RANGES[p]
            vitals[p] = (
                round(random.uniform(lo, hi), 1)
                if isinstance(lo, float)
                else random.randint(lo, hi)
            )
        return vitals

    def send_vitals(self, vitals):
        """Send data safely via TCP as proper JSON."""
        if not self.sock:
            # Try reconnect
            print("🔄 Reconnecting...")
            self.sock = connect_tcp()
            if not self.sock:
                return

        try:
            msg = json.dumps(vitals) + "\n"
            self.sock.send(msg.encode())
        except Exception as e:
            print("⚠️ Send error:", e)
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

    def update(self):
        vitals = self.generate_vitals()
        t = round(time.time() - self.start_time, 1)
        self.time_axis.append(t)

        # Send data
        self.send_vitals(vitals)

        # Update GUI charts
        for p in PARAMS:
            self.data[p].append(vitals[p])
            ax = self.axes[p]
            ax.clear()
            ax.set_title(p)
            ax.set_ylim(RANGES[p][0] - 5, RANGES[p][1] + 5)
            ax.plot(self.time_axis, self.data[p], color="blue")

        self.fig.tight_layout()
        self.canvas.draw()

        self.root.after(UPDATE_MS, self.update)


# -------- Main --------
if __name__ == "__main__":
    tcp_socket = connect_tcp()
    root = tk.Tk()
    root.title("Vitals Sender")
    app = MonitorSender(root, tcp_socket)
    root.mainloop()
    if tcp_socket:
        tcp_socket.close()
