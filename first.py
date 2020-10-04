import gi
#import Calib
from Calib import *
from multiprocessing import Process
import subprocess
from EyeTracker import *
from Sidebox import *
#from sdbx import *
from tkinter import *
import cv2
import os
from Settings import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class First(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Observer")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)
        # Stack grid
        grid = Gtk.Grid(column_homogeneous=True, row_spacing=20, column_spacing=10)
        self.add(grid)

        # Tab stack
        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        grid.attach(stack, 0, 1, 1, 1)  # row 0, col 1, width 1, height 1
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT) # Left to right animation
        stack.set_transition_duration(500)  # 500 for optimal animation

        # Stack switching extra
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        grid.attach(stack_switcher, 0, 0, 1, 1) # Place switcher at position row 0, col 0, width 1, height 1

        # Tab labels
        lbl1 = Gtk.Label(label="Calibrate to ensure accuracy")
        lbl2 = Gtk.Label(label="Perform calibration before tracking")
        lbl3 = Gtk.Label(label="Settings for more control")
        lbl4 = Gtk.Label(label="Code reserved by MCMS Group-IV of 2020")

        # Calibration tab
        grid2 = Gtk.Grid(column_homogeneous=True, row_spacing=10)
        button1 = Gtk.Button(label="Start calibration")
        button1.connect("clicked", self.calb)
        grid2.add(lbl1)
        grid2.attach_next_to(button1, lbl1, Gtk.PositionType.BOTTOM, 1, 1)
        name1 = "Calibrate"
        title1 = "Calibration"
        stack.add_titled(grid2, name1, title1)
        

        # Tracking tab
        grid3 = Gtk.Grid(column_homogeneous=True, row_spacing=10)
        button2 = Gtk.Button(label="Start tracking")
        button2.connect("clicked", self.trck)
        grid3.add(lbl2)
        grid3.attach_next_to(button2, lbl2, Gtk.PositionType.BOTTOM, 1, 1)
        name2 = "Track"         # Internal title
        title2 = "Tracking"     # Tab title
        stack.add_titled(grid3, name2, title2)

        #Settings tab
        grid4 = Gtk.Grid(column_homogeneous=True, row_spacing=10)
        button3 = Gtk.Button(label="Open Settings")
        button3.connect("clicked", self.sett)
        grid4.add(lbl3)
        grid4.attach_next_to(button3, lbl3, Gtk.PositionType.BOTTOM, 1, 1)
        name3 = "Settings"
        title3 = "Settings"
        stack.add_titled(grid4, name3, title3)

        # About tab
        grid5 = Gtk.Grid(column_homogeneous=True, row_spacing=10)
        grid5.add(lbl4)
        name4 = "About"
        title4 = "About"
        stack.add_titled(grid5, name4, title4)

    def calb(self, button):     # Start calibration
        root=tk.Tk()
        c=Calib(root)
        c.display(root)
        root.mainloop()
    def A(self):
        sdbx = Sidebox()
        sdbx.disp()
        sdbx.root.mainloop()
    def B(self):
        e=EyeTracker()
        c=True
        while c:
            e.eyeTracking()
            #print(key)
            try:
                check=open("check.txt","r")
                c=False
            except FileNotFoundError:
                c=True
            
        e.stopTracking()
        del e
    def trck(self, button):     # Start tracking
        try:
            calt = open("calt.txt", "r")
            calv = str(calt.read(1))
            print(calv)

        except FileNotFoundError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Calibration not performed")
            dialog.format_secondary_text("Please calibrate before tracking")
            dialog.run()
            print("ERROR dialog closed")
            dialog.destroy()

        finally:
            calt.close()

        if(calv!="1"):
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Calibration not performed")
            dialog.format_secondary_text("Please calibrate before tracking")
            dialog.run()
            print("ERROR dialog closed")
            dialog.destroy()
        else:
             p1=Process(target=self.A)
             p1.start()
             p2=Process(target=self.B)
             p2.start()
                 
    def sett(self, button):     # Open settings
        Settings.show()

    def val_read(self):
        try:
            f_d = open("dtv.txt", "r")
            fd = float(f_d.read(3))     # Reads 3 characters: 0, . and after decimal
        finally:
            f_d.close()

        try:
            f_t = open("tvv.txt", "r")
            ft = int(f_t.read(2))       # Reads max. two chars
        finally:
            f_t.close()

if __name__ == "__main__":
    win = First()
    win.show_all()
    Gtk.main()
