import gi                               # Importing PyGObject
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Welcome(Gtk.Assistant):
    def __init__(self):
        Gtk.Assistant.__init__(self)
        self.set_title("Welcome Tour")
        #self.set_default_size(600, 300)

        self.connect("cancel", self.on_cancel_clicked)
        self.connect("close", self.on_close_clicked)
        self.connect("apply", self.on_apply_clicked)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(box1)
        self.set_page_type(box1, Gtk.AssistantPageType.INTRO)
        self.set_page_title(box1, "Welcome Tour")
        label0 = Gtk.Label(label="Welcome to ObServe")
        box1.pack_start(label0, True, True, 0)
        self.set_page_complete(box1, True)

        calb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(calb)
        self.set_page_type(calb, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(calb, "Calibration")
        label1 = Gtk.Label(label="1. Move head to each button.")
        label1.set_xalign(0.0)
        label1a = Gtk.Label(label="2.Click on the button.")
        label1a.set_xalign(0.0)
        label1b = Gtk.Label(label="3. Buttons would disappear.")
        label1b.set_xalign(0.0)
        label1c = Gtk.Label(label="4. After button 4 is gone, close your eyes for 2 seconds and click.")
        label1c.set_xalign(0.0)
        calb.pack_start(label1, False, False, 0)
        calb.pack_start(label1a, False, False, 0)
        calb.pack_start(label1b, False, False, 0)
        calb.pack_start(label1c, False, False, 0)
        self.set_page_complete(calb, True)

        trck = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(trck)
        self.set_page_type(trck, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(trck, "Tracking")
        label2 = Gtk.Label(label="Calibrate before tracking.")
        label2.set_xalign(0.0)
        trck.pack_start(label2, False, False, 0)
        self.set_page_complete(trck, True)

        util = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(util)
        self.set_page_type(util, Gtk.AssistantPageType.PROGRESS)
        self.set_page_title(util, "Utilities")
        image1 = Gtk.Image()
        image1.set_from_file("c.jpg")
        util.pack_start(image1, True, True, 0)
        self.set_page_complete(util, True)

        done = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(done)
        self.set_page_type(done, Gtk.AssistantPageType.SUMMARY)
        self.set_page_title(done, "All done")
        label7 = Gtk.Label(label="We hope you have a great experience!")
        done.pack_start(label7, True, True, 0)
        self.set_page_complete(done, True)

    def on_apply_clicked(self, *args):
        print("The 'Apply' button has been clicked")

    def on_close_clicked(self, *args):
        print("The 'Close' button has been clicked")
        Gtk.main_quit()

    def on_cancel_clicked(self, *args):
        print("The Assistant has been cancelled.")
        Gtk.main_quit()

    """def on_complete_toggled(self, checkbutton):
        welcome.set_page_complete(self.trck, checkbutton.get_active())"""

if __name__=='__main__':
    welcome = Welcome()
    welcome.show_all()
    Gtk.main()
