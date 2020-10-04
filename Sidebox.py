import tkinter as tk, pyautogui as pg, subprocess
from multiprocessing import Process
from tkinter import *
from EyeTracker import *
import os
import pynput
from pynput.keyboard import Key,Controller
class Sidebox:

    def __init__(self):
        try:
            os.remove("check.txt")
        except FileNotFoundError:
            print()
        with open('settings.txt') as f: 
                self.settings=[word for line in f for word in line.split()]
        f.close()
        print(self.settings[0],self.settings[1])
        self.keyboard=Controller()
        self.root = tk.Tk()
        self.up=0
        self.down=0
        pg.FAILSAFE=False
        self.root.resizable(0, 0)
        self.root.geometry("50x300")
        self.root.columnconfigure(1, weight=1)
        self.root.overrideredirect(True)
        self.root.wait_visibility()
        self.root.wm_attributes('-alpha', 0.7)
        self.w = int(self.root.winfo_screenwidth())
        self.h = int(self.root.winfo_screenheight())
        self.root.geometry("+{0}+{1}".format(self.w-50,int(self.h/2)-125))

    def disp(self):
        self.bf4 = Frame(self.root)
        self.bf4.pack(side = "bottom")
        self.bf1 = Frame(self.root)
        self.bf1.pack(side = "bottom")
        self.bf2 = Frame(self.root)
        self.bf2.pack(side = "bottom")
        self.bf3 = Frame(self.root)
        self.bf3.pack(side = "bottom")
        self.bf5 = Frame(self.root)
        self.bf5.pack(side = "bottom")
        self.bf6 = Frame(self.root)
        self.bf6.pack(side = "bottom")
        
        self.photo5 = tk.PhotoImage(file="cli.png")
        tk.Button(self.bf5,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo5, compound="top", command=self.mcli).pack(side="left")
        self.photo1 = tk.PhotoImage(file="u.png")
        tk.Button(self.bf3,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo1, compound="top", command=self.sup).pack(side="left")
        self.photo2 = tk.PhotoImage(file="d.png")
        tk.Button(self.bf2,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo2, compound="top", command=self.sdn).pack(side="left")
        self.photo3 = tk.PhotoImage(file="cross.png")
        tk.Button(self.bf1,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo3, compound="top", command=self.mcls).pack(side="left")
        self.photo4 = tk.PhotoImage(file="sdn.png")
        tk.Button(self.bf4,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo4, compound="top", command=self.mcli1).pack(side="left")
        self.photo6 = tk.PhotoImage(file="minimize.png")
        tk.Button(self.bf6,  height="50", width="50", borderwidth=0, highlightthickness=0, relief="flat", image=self.photo6, compound="top", command=self.ecls).pack(side="left")

    def sup(self):
        '''self.psi = pg.position()
        pg.click(x=self.w/2, y=self.h/2)
        pg.scroll(+10)
        #pg.moveTo(self.psi.x, self.psi.y)'''
        self.keyboard.press(Key.page_up)
        self.Keyboard.release(Key.page_up)

    def sdn(self):
        #self.down=1
        '''self.psi = pg.position()
        pg.click(x=self.w/2, y=self.h/2)
        pg.scroll(-10)
        pg.moveTo(self.psi.x, self.psi.y)'''
        self.keyboard.press(Key.page_down)
        self.keyboard.release(Key.page_down)

    def cls(self):
        subprocess.call(["xdotool", "selectwindow", "windowclose"])

    def cli(self):
        subprocess.call(["mousetweaks", "-s"])
        subprocess.call(["setsid", "mousetweaks", "--dwell", self.settings[0],self.settings[1], "&"])
    def cli1(self):
        self.cald=open("check.txt","w")
        self.cald.write("1")
        self.cald.close()
        print("wrote")
        subprocess.call(["mousetweaks", "-s"])
        
    def cls1(self):
        '''self.cald=open("check.txt","w")
        self.cald.write("1")
        self.cald.close()
        print("wrote")'''
        subprocess.call(["xdotool", "selectwindow", "windowminimize"])

        
    def msup(self):
        p1 = Process(target = self.sup)
        p1.start()
        #p1.join()

    def msdn(self):
        p2 = Process(target = self.sdn)
        p2.start()
        #p2.join()

    def mcls(self):
        p3 = Process(target = self.cls)
        p3.start()
        #p3.join()

    def mcli(self):
        p4 = Process(target = self.cli)
        p4.start()
        #p4.join()
        
    def mcli1(self):
        p5 = Process(target=self.cli1)
        p5.start()
        self.root.destroy()
        
    def ecls(self):
        p6=Process(target=self.cls1)
        p6.start()

if __name__=='__main__':
    sdbx = Sidebox()
    sdbx.disp()
    sdbx.root.mainloop()
