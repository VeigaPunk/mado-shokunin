# excerpt of /home/vgpnk/Projects/gkeep/gkeep/ui.py lines 446-495 at gkeep HEAD 133b867 (operator project, read-only copy)
# full-file sha256 07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a
class GkeepApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.omarchy.gkeep",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.board: Board | None = None
        self.pending_mode = "capture"

    def do_startup(self):
        Gtk.Application.do_startup(self)
        provider = Gtk.CssProvider()
        provider.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_command_line(self, command_line):
        args = command_line.get_arguments()[1:]
        mode = args[0] if args else "capture"
        self.pending_mode = "list" if mode == "list" else "capture"
        self.activate()
        return 0

    def do_activate(self):
        if self.board is None:
            window = Gtk.ApplicationWindow(application=self, title="gkeep")
            window.set_decorated(False)
            window.set_default_size(420, 500)
            self.board = Board(window)
            window.set_child(self.board.stack)
            self.add_window(window)
        if self.pending_mode == "list":
            self.board.show_list()
        else:
            self.board.show_capture()


def run(mode: str) -> int:
    app = GkeepApp()
    return app.run(["gkeep", mode])

