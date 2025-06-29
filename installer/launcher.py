import tkinter as tk
import subprocess
import threading
from pathlib import Path
import sys
import tkinter.messagebox as messagebox
from tkinter import scrolledtext
import datetime

if getattr(sys, 'frozen', False):
    # If running as a PyInstaller EXE
    ROOT_DIR = Path(sys.executable).resolve().parent
else:
    # If running as a Python script
    ROOT_DIR = Path(__file__).resolve().parent.parent

MAKE_SCRIPT = ROOT_DIR / "scripts" / "make.ps1"
SERVER_PROCESS = None

# ------------------ Core Logic ------------------ #

def run_task(task):
    def task_thread():
        try:
            disable_all_buttons()
            log_box.configure(state="normal")
            log_box.insert(tk.END, f">>> Running task: {task}\n", "bold")
            log_box.see(tk.END)
            log_box.configure(state="disabled")

            process = subprocess.Popen(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(MAKE_SCRIPT), task],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            for line in process.stdout:
                log_box.configure(state="normal")
                log_box.insert(tk.END, line)
                log_box.see(tk.END)
                log_box.configure(state="disabled")

            process.wait()

            log_box.configure(state="normal")
            if process.returncode == 0:
                log_box.insert(tk.END, f"\n>>> Task '{task}' completed successfully.\n\n", "success")
            else:
                log_box.insert(tk.END, f"\n>>> Task '{task}' failed with exit code {process.returncode}\n\n", "error")
            log_box.see(tk.END)
            log_box.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Task '{task}' failed:\n{e}")
        finally:
            enable_all_buttons()

    threading.Thread(target=task_thread, daemon=True).start()


def open_env_editor():
    def edit():
        try:
            env_path = ROOT_DIR / ".env"
            subprocess.Popen(["notepad.exe", str(env_path)], shell=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    threading.Thread(target=edit, daemon=True).start()


def run_server():
    def server_thread():
        global SERVER_PROCESS
        if SERVER_PROCESS is None:
            SERVER_PROCESS = subprocess.Popen(
                ["python", "-m", "api.main"],
                cwd=ROOT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            disable_controls_during_server()
            log("FastAPI server started")

            def stream_logs():
                for line in SERVER_PROCESS.stdout:
                    log_box.configure(state="normal")
                    log_box.insert(tk.END, line)
                    log_box.configure(state="disabled")
                    log_box.see(tk.END)

            threading.Thread(target=stream_logs, daemon=True).start()
    threading.Thread(target=server_thread, daemon=True).start()


def stop_server():
    def stop_thread():
        global SERVER_PROCESS
        if SERVER_PROCESS:
            try:
                SERVER_PROCESS.terminate()
                SERVER_PROCESS.wait(timeout=5)
                log("FastAPI server stopped")
            except Exception as e:
                log(f"Error stopping server: {e}")
            SERVER_PROCESS = None
            enable_controls_after_server()
    threading.Thread(target=stop_thread, daemon=True).start()


def log(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    log_box.configure(state="normal")
    log_box.insert(tk.END, f"{timestamp} {message}\n")
    log_box.configure(state="disabled")
    log_box.see(tk.END)

button_refs = []

def disable_all_buttons():
    for btn in button_refs:
        btn.config(state="disabled")

def enable_all_buttons():
    for btn in button_refs:
        btn.config(state="normal")

def disable_controls_during_server():
    for btn in button_refs:
        if btn not in [btn_stop_server]:
            btn.config(state="disabled")

def enable_controls_after_server():
    for btn in button_refs:
        btn.config(state="normal")


def clear_logs():
    log_box.configure(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.configure(state="disabled")

root = tk.Tk()
root.title("Tomato Disease Classifier Launcher")
root.geometry("800x600")
root.configure(bg="#f4f4f4")

# ----- Main Frames -----
main_frame = tk.Frame(root, bg="#f4f4f4")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame, bg="#f4f4f4")
left_frame.grid(row=0, column=0, sticky="n")

right_frame = tk.Frame(main_frame, bg="#f4f4f4")
right_frame.grid(row=0, column=1, sticky="n", padx=(30, 0))

# ----- Title -----
tk.Label(left_frame, text="Tomato Disease Classifier", font=("Helvetica", 16, "bold"), bg="#f4f4f4")\
    .grid(row=0, column=0, columnspan=2, pady=(0, 15))

# ----- Main Task Buttons -----
buttons = [
    ("Start All", "start"),
    ("Stop All", "stop"),
    ("Start TF Serving", "start-tf"),
    ("Stop TF Serving", "stop-tf"),
    ("Start Monitoring", "start-monitoring"),
    ("Stop Monitoring", "stop-monitoring"),
    ("Run Unit Tests", "test-unit"),
    ("Run Integration Tests", "test-integration"),
    ("Create ZIP Archive", "package")
]

for i, (label, task) in enumerate(buttons, start=1):
    btn = tk.Button(left_frame, text=label, width=25, bg="#4CAF50", fg="white", relief="raised",
                    command=lambda t=task: run_task(t))
    btn.grid(row=i, column=0, pady=2, sticky="ew")
    button_refs.append(btn)

# ----- Server Controls -----
tk.Label(left_frame, text="Server Controls", font=("Helvetica", 12, "bold"), bg="#f4f4f4")\
    .grid(row=11, column=0, pady=(15, 5))

btn_start_server = tk.Button(left_frame, text="Start Server", width=25, height=2,
                             font=("Helvetica", 11, "bold"), bg="#2196F3", fg="white",
                             command=run_server)
btn_start_server.grid(row=12, column=0, pady=4, sticky="ew")
button_refs.append(btn_start_server)

btn_stop_server = tk.Button(left_frame, text="Stop Server", width=25, height=2,
                            font=("Helvetica", 11, "bold"), bg="#f44336", fg="white",
                            command=stop_server)
btn_stop_server.grid(row=13, column=0, pady=4, sticky="ew")
button_refs.append(btn_stop_server)

# ----- Edit .env -----
btn_env = tk.Button(left_frame, text="Edit Environment (.env)", width=25, bg="#607d8b", fg="white",
                    command=open_env_editor)
btn_env.grid(row=14, column=0, pady=(10, 4), sticky="ew")
button_refs.append(btn_env)

# ----- clear logs -----
btn_clear_logs = tk.Button(right_frame, text="Clear Logs", width=20, bg="#795548", fg="white", command=clear_logs)
btn_clear_logs.grid(row=3, column=0, pady=(0, 10), sticky="e")

# ----- Exit -----
btn_exit = tk.Button(left_frame, text="Exit", width=25, bg="#9e9e9e", fg="white", command=root.quit)
btn_exit.grid(row=15, column=0, pady=(5, 10), sticky="ew")
button_refs.append(btn_exit)

# ----- Log Box -----
tk.Label(right_frame, text="Logs", font=("Helvetica", 13, "bold"), bg="#f4f4f4")\
    .grid(row=0, column=0, sticky="w",pady=(25,0))

log_box = scrolledtext.ScrolledText(right_frame, height=30, width=50, state="disabled", wrap=tk.WORD)
log_box.grid(row=2, column=0, pady=(0, 10), sticky="nsew")
log_box.tag_config("bold", font=("Helvetica", 10, "bold"))
log_box.tag_config("success", foreground="green", font=("Helvetica", 10, "italic"))
log_box.tag_config("error", foreground="red", font=("Helvetica", 10, "italic"))


root.mainloop()
