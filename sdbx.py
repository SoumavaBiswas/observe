import tkinter as tk, pyautogui as pg, subprocess
from multiprocessing import Process
from tkinter import *

class sdbx:

    def __init__(self, root):
        self.master = root
        root.resizable(0, 0)
        root.geometry("50x250")
        root.columnconfigure(1, weight=1)
        root.overrideredirect(True)
        root.wait_visibility()
        root.wm_attributes('-alpha', 0.7)
        self.w = int(root.winfo_screenwidth())
        self.h = int(root.winfo_screenheight())
        root.geometry("+{0}+{1}".format(self.w-50,int(self.h/2)-125))

    def disp(self):
        self.bf4 = Frame(root)
        self.bf4.pack(side = "bottom")
        self.bf1 = Frame(root)
        self.bf1.pack(side = "bottom")
        self.bf2 = Frame(root)
        self.bf2.pack(side = "bottom")
        self.bf3 = Frame(root)
        self.bf3.pack(side = "bottom")
        self.bf5 = Frame(root)
        self.bf5.pack(side = "bottom")
        self.photo5 = tk.PhotoImage(file="cli.png")
        tk.Button(self.bf5,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo5, compound="top", command=self.mcli).pack(side="left")
        self.photo1 = tk.PhotoImage(file="u.png")
        tk.Button(self.bf3,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo1, compound="top", command=self.sup).pack(side="left")
        self.photo2 = tk.PhotoImage(file="d.png")
        tk.Button(self.bf2,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo2, compound="top", command=self.sdn).pack(side="left")
        self.photo3 = tk.PhotoImage(file="cls.png")
        tk.Button(self.bf1,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo3, compound="top", command=self.mcls).pack(side="left")
        self.photo4 = tk.PhotoImage(file="sdn.png")
        tk.Button(self.bf4,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo4, compound="top", command=root.destroy).pack(side="left")

    def sup(self):
        self.psi = pg.position()
        pg.click(x=self.w/2, y=self.h/2)
        pg.scroll(+10)
        pg.moveTo(self.psi.x, self.psi.y)

    def sdn(self):
        self.psi = pg.position()
        pg.click(x=self.w/2, y=self.h/2)
        pg.scroll(-10)
        pg.moveTo(self.psi.x, self.psi.y)

    def cls(self):
        subprocess.call(["xdotool", "selectwindow", "windowclose"])

    def cli(self):
        subprocess.call(["setsid", "mousetweaks", "--dwell", "--dwell-time=0.8", "&"])

    def msup(self):
        p1 = Process(target = self.sup)
        p1.start()

    def msdn(self):
        p2 = Process(target = self.sdn)
        p2.start()

    def mcls(self):
        p3 = Process(target = self.cls)
        p3.start()

    def mcli(self):
        p4 = Process(target = self.cli)
        p4.start()

if __name__=='__main__':
    root = tk.Tk()
    s = sdbx(root)
    s.disp()
    root.mainloop()
