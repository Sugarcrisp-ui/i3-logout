#!/usr/bin/env python3
import sys
sys.path.append('/home/brett/github-repos/i3-logout')  # Point to clone for Functions.py and GUI.py

import cairo
import gi
import shutil
import GUI
import Functions as fn
import threading
import signal
import os

# Graceful fallback for distro module
try:
    from distro import id
    distr = id()
except (ImportError, ModuleNotFoundError):
    distr = "unknown"

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Wnck", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, Wnck, GLib, GdkX11  # noqa

# Working directory = the repo folder
working_dir = os.path.dirname(os.path.realpath(__file__))
fn.working_dir = working_dir

class TransparentWindow(Gtk.Window):
    cmd_shutdown = "systemctl poweroff"
    cmd_restart = "systemctl reboot"
    cmd_suspend = "systemctl suspend"
    cmd_hibernate = "systemctl hibernate"

    if distr == "artix":
        if os.path.isfile("/usr/bin/loginctl"):
            cmd_shutdown = "loginctl poweroff"
            cmd_restart = "loginctl reboot"
            cmd_suspend = "loginctl suspend"
            cmd_hibernate = "loginctl hibernate"

    cmd_lock = 'betterlockscreen -l dim -- --time-str="%H:%M"'
    wallpaper = "/usr/share/betterlockscreen/wallpapers/wallpaper.jpg"
    d_buttons = [
        "cancel",
        "shutdown",
        "restart",
        "suspend",
        "hibernate",
        "lock",
        "logout",
    ]
    binds = {
        "lock": "K",
        "restart": "R",
        "shutdown": "S",
        "suspend": "U",
        "hibernate": "H",
        "logout": "L",
        "cancel": "Escape",
        "settings": "P",
    }
    theme = "white"
    hover = "#ffffff"
    icon = 64
    font = 11
    buttons = None
    active = False
    opacity = 0.8

    def __init__(self):
        super(TransparentWindow, self).__init__(type=Gtk.WindowType.TOPLEVEL, title="i3 Logout")
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect("delete-event", self.on_close)
        self.connect("destroy", self.on_close)
        self.connect("draw", self.draw)
        self.connect("key-press-event", self.on_keypress)
        self.connect("window-state-event", self.on_window_state_event)
        self.set_decorated(False)

        if not fn.os.path.isdir(fn.home + "/.config/i3-logout"):
            fn.os.mkdir(fn.home + "/.config/i3-logout")

        self.screen = self.get_screen()
        self.display = Gdk.Display.get_default()
        seat = self.display.get_default_seat()
        self.pointer = Gdk.Seat.get_pointer(seat)

        visual = self.screen.get_rgba_visual()
        if visual and self.screen.is_composited():
            self.set_visual(visual)

        fn.get_config(self, Gdk, Gtk, fn.config)

        self.display_on_monitor()

        if self.buttons is None or self.buttons == [""]:
            self.buttons = self.d_buttons

        self.set_app_paintable(True)
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.KEY_RELEASE_MASK |
            Gdk.EventMask.STRUCTURE_MASK
        )
        self.present()

        GUI.GUI(self, Gtk, GdkPixbuf, working_dir, fn.os, Gdk, fn)

        if not fn.os.path.isfile("/tmp/i3-logout.lock"):
            with open("/tmp/i3-logout.lock", "w") as f:
                f.write("")

    def display_on_monitor(self):
        print("#### i3-logout ####")
        try:
            if self.pointer.get_has_cursor():
                screen, x, y = self.pointer.get_position()
                session_type = os.environ.get("XDG_SESSION_TYPE")
                if session_type == "wayland":
                    print("[WARN]: Wayland - mouse position not available")
                if screen is not None and x != 0 and y != 0:
                    display = self.pointer.get_display()
                    if display is not None:
                        monitor = display.get_monitor_at_point(x, y)
                        geometry = monitor.get_geometry()
                        self.set_size_request(geometry.width, geometry.height)
                        self.move(x, y)
                        self.fullscreen()
                else:
                    self.display_on_default()
            else:
                self.display_on_default()
        except Exception as e:
            print(f"[ERROR]: {e}")
            self.display_on_default()

    def display_on_default(self):
        monitor = self.display.get_monitor(0)
        geometry = monitor.get_geometry()
        self.set_size_request(geometry.width, geometry.height)
        self.fullscreen()

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, self.opacity)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def on_keypress(self, widget=None, event=None, data=None):
        shortcut_keys = [
            self.binds.get("cancel"),
            self.binds.get("shutdown"),
            self.binds.get("restart"),
            self.binds.get("suspend"),
            self.binds.get("logout"),
            self.binds.get("lock"),
            self.binds.get("hibernate"),
            self.binds.get("settings"),
        ]
        for key in shortcut_keys:
            if event.keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
                self.click_button(widget, key)
                break

    def on_mouse_in(self, widget, event, data):
        try:
            # Delegate to Functions.button_active which updates images/labels
            fn.button_active(self, data, GdkPixbuf)
        except Exception:
            pass
        try:
            event.window.set_cursor(Gdk.Cursor(Gdk.CursorType.HAND2))
        except Exception:
            pass

    def on_mouse_out(self, widget, event, data):
        if not self.active:
            try:
                # Reset button highlights / sensitivities
                fn.button_toggled(self, "")
            except Exception:
                pass
        try:
            event.window.set_cursor(None)
        except Exception:
            pass

    def on_click(self, widget, event, data):
        self.click_button(widget, data)

    def on_window_state_event(self, widget, ev):
        self.__is_fullscreen = bool(ev.new_window_state & Gdk.WindowState.FULLSCREEN)

    def click_button(self, widget, data=None):
        try:
            # Determine action name from key (data may be a key like 'S' or the action name)
            action = None
            if data in self.binds.values():
                action = [k for k, v in self.binds.items() if v == data][0]
            else:
                action = data

            if action == "cancel":
                self.on_close()
            elif action == "settings":
                try:
                    if self.popover.get_visible():
                        self.popover.hide()
                    else:
                        self.popover.show_all()
                except Exception:
                    pass
            elif action == "lock":
                try:
                    self.__exec_cmd(self.cmd_lock)
                finally:
                    Gtk.main_quit()
            elif action == "shutdown":
                self.__exec_cmd(self.cmd_shutdown)
            elif action == "restart":
                self.__exec_cmd(self.cmd_restart)
            elif action == "suspend":
                self.__exec_cmd(self.cmd_suspend)
            elif action == "hibernate":
                self.__exec_cmd(self.cmd_hibernate)
            elif action == "logout":
                cmd = fn._get_logout()
                if cmd:
                    self.__exec_cmd(cmd)
        except Exception as e:
            print(e)

    def __exec_cmd(self, cmdline):
        fn.os.system(cmdline)

    def on_save_clicked(self, widget=None):
        # Placeholder for save settings handler called from GUI
        # Implement saving logic in future; for now just print and close popover
        try:
            if hasattr(self, 'popover') and self.popover:
                self.popover.hide()
        except Exception:
            pass

    def on_close(self, widget=None, data=None):
        if os.path.isfile("/tmp/i3-logout.lock"):
            os.unlink("/tmp/i3-logout.lock")
        if os.path.isfile("/tmp/i3-logout.pid"):
            os.unlink("/tmp/i3-logout.pid")
        Gtk.main_quit()

def signal_handler(sig, frame):
    print("\ni3-logout is Closing.")
    if os.path.isfile("/tmp/i3-logout.lock"):
        os.unlink("/tmp/i3-logout.lock")
    if os.path.isfile("/tmp/i3-logout.pid"):
        os.unlink("/tmp/i3-logout.pid")
    Gtk.main_quit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    if not os.path.isfile("/tmp/i3-logout.lock"):
        with open("/tmp/i3-logout.pid", "w") as f:
            f.write(str(os.getpid()))
        w = TransparentWindow()
        w.show_all()
        Gtk.main()
    else:
        print("i3-logout did not close properly. Remove /tmp/i3-logout.lock with sudo.")