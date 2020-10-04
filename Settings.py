import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Settings(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)

        grid = Gtk.Grid(row_spacing=5, column_spacing=5)
        self.add(grid)

        lbl1 = Gtk.Label(label="Wait time")
        lbl1.set_xalign(0)

        grid.add(lbl1)

        adjustment1 = Gtk.Adjustment(value=0.5, lower=0.2, upper=3.0, step_increment=0.1, page_increment=0, page_size=0)
        self.spinbutton1 = Gtk.SpinButton()
        self.spinbutton1.configure(adjustment1, 0.1, 1)

        grid.attach_next_to(self.spinbutton1, lbl1, Gtk.PositionType.RIGHT, 1, 1)

        lbl2 = Gtk.Label(label="Amount")
        lbl2.set_xalign(0)

        grid.attach_next_to(lbl2, lbl1, Gtk.PositionType.BOTTOM, 1, 1)  # row 0, col 1, width 1, height 1

        adjustment2 = Gtk.Adjustment(value=0, lower=0, upper=30, step_increment=1, page_increment=1, page_size=0)
        self.spinbutton2 = Gtk.SpinButton()
        self.spinbutton2.configure(adjustment2, 1, 0)

        grid.attach_next_to(self.spinbutton2, lbl2, Gtk.PositionType.RIGHT, 1, 1)

        button1 = Gtk.Button(label="Save settings")
        button1.connect("clicked", self.sv) # Start save function

        grid.attach_next_to(button1, lbl2, Gtk.PositionType.BOTTOM, 2, 1)  # row 0, col 1, width 1, height 1

    def sv(self, button):

        # Store values
        dtv = "{:.1f}".format(round((float(self.spinbutton1.get_value())), 1))
        tvv = (int(self.spinbutton2.get_value()))

        # Debugging
        print("Dwell: ",dtv)
        print("Threshold: ",tvv)

        # Write values to files
        try:
             f=open("settings.txt","w")
             f.write('--dwell-time={} --threshold={}'.format(dtv,tvv))
        finally:
             f.close()

        
        self.destroy()   # Close window

    def show():
        win = Settings()
        win.show_all()
        Gtk.main()
