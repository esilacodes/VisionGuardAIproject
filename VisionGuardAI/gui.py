
import tkinter as tk
from tkinter import messagebox
from db import Database
from camera import Camera

class App:
    def __init__(self):
        self.db = Database()
        self.cam = Camera()

        self.root = tk.Tk()
        self.root.title("VisionGuardAI")
        self.root.geometry("1000x600")

        self.login_ui()

    def run(self):
        self.root.mainloop()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # LOGIN
    def login_ui(self):
        self.clear()

        tk.Label(self.root, text="SIGN IN", font=("Arial", 20)).pack()

        self.user = tk.Entry(self.root)
        self.user.pack()

        self.pw = tk.Entry(self.root, show="*")
        self.pw.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Go Sign Up", command=self.signup_ui).pack()

    def signup_ui(self):
        self.clear()

        tk.Label(self.root, text="SIGN UP", font=("Arial", 20)).pack()

        self.su_user = tk.Entry(self.root)
        self.su_user.pack()

        self.su_pw = tk.Entry(self.root, show="*")
        self.su_pw.pack()

        self.su_tel = tk.Entry(self.root)
        self.su_tel.pack()

        tk.Button(self.root, text="Register", command=self.signup).pack()
        tk.Button(self.root, text="Back", command=self.login_ui).pack()

    def signup(self):
        ok, msg = self.db.add_user(
            self.su_user.get(),
            self.su_pw.get(),
            self.su_tel.get()
        )
        messagebox.showinfo("Info", msg)

    def login(self):
        if self.db.login(self.user.get(), self.pw.get()):
            self.dashboard()
        else:
            messagebox.showerror("Error", "Login failed")

    # DASHBOARD
    def dashboard(self):
        self.clear()

        left = tk.Frame(self.root, width=200, bg="gray")
        left.pack(side="left", fill="y")

        main = tk.Frame(self.root)
        main.pack(side="right", expand=True, fill="both")

        tk.Button(left, text="Dashboard", command=lambda: self.view(main,"dash")).pack(fill="x")
        tk.Button(left, text="Live", command=lambda: self.view(main,"live")).pack(fill="x")
        tk.Button(left, text="Start", command=self.cam.start).pack(fill="x")
        tk.Button(left, text="Stop", command=self.cam.stop).pack(fill="x")
        tk.Button(left, text="Logout", command=self.login_ui).pack(side="bottom")

        self.view(main,"dash")

    def view(self, frame, mode):
        for w in frame.winfo_children():
            w.destroy()

        if mode == "dash":
            tk.Label(frame, text="Dashboard").pack()

        elif mode == "live":
            tk.Label(frame, text="Live View").pack()
