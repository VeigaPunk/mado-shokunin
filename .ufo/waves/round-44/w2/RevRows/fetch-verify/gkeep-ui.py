"""Floating post-it window. Paste a note, or open the local list."""

from __future__ import annotations

import os
import signal
import subprocess
from datetime import datetime, timezone

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gdk, Gio, GLib, Gtk, Pango

from gkeep.notes import (
    add_note,
    delete_note,
    format_stamp,
    get_note,
    list_notes,
    parse_created,
    summary,
    update_note,
)

FONT = "JetBrainsMonoNL Nerd Font Mono"

CSS = f"""
window.note-mode {{
  background-color: #fff475;
}}
window.list-mode {{
  background-color: #2a2723;
}}
window.note-mode textview,
window.note-mode textview text,
window.list-mode label,
window.note-mode label,
window.note-mode button,
window.note-mode button label,
window.list-mode button,
window.list-mode button label {{
  font-family: "{FONT}";
}}
window.note-mode textview,
window.note-mode textview text {{
  background-color: transparent;
  color: #202124;
  font-size: 14px;
  caret-color: #202124;
}}
window.note-mode textview text selection {{
  background-color: rgba(32, 33, 36, 0.18);
  color: #202124;
}}
label.stamp {{
  color: rgba(32, 33, 36, 0.62);
  font-size: 11px;
}}
window.list-mode label.stamp {{
  color: rgba(32, 33, 36, 0.62);
  font-size: 12px;
}}
label.paper {{
  color: #f3efe6;
  font-size: 13px;
}}
label.hint {{
  color: rgba(32, 33, 36, 0.7);
  font-size: 11px;
}}
window.list-mode label.hint {{
  color: #f3efe6;
}}
label.summary {{
  color: #202124;
  font-size: 13px;
}}
button.ink {{
  background: #202124;
  color: #fff475;
  border: none;
  box-shadow: none;
  border-radius: 2px;
  padding: 6px 12px;
  min-height: 30px;
  min-width: 72px;
  font-size: 12px;
}}
button.ink label {{
  color: #fff475;
}}
button.ink:hover {{
  background: #3c4043;
}}
window.list-mode button.ink {{
  background: #3a3834;
  color: #f3efe6;
}}
window.list-mode button.ink label {{
  color: #f3efe6;
}}
button.slip {{
  background: #fff475;
  color: #202124;
  border: none;
  box-shadow: none;
  border-radius: 2px;
  padding: 8px 10px;
  margin-top: 8px;
}}
button.slip label {{
  color: #202124;
}}
button.slip:hover {{
  background: #ffe96a;
}}
"""


def ping_waybar() -> None:
    if os.environ.get("GKEEP_NO_SIGNAL"):
        return
    try:
        number = int(signal.SIGRTMIN) + 12
        subprocess.run(
            ["pkill", f"-{number}", "waybar"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, ValueError):
        pass


class Board:
    def __init__(self, window: Gtk.Window):
        self.window = window
        self.note_id: str | None = None
        self.draft_created = datetime.now(timezone.utc)
        self._painting = False

        self.buffer = Gtk.TextBuffer()
        self.face = self.buffer.create_tag("face", font=f"{FONT} 14", foreground="#202124")
        self.buffer.connect("changed", self._on_changed)
        self.view = Gtk.TextView(
            buffer=self.buffer,
            wrap_mode=Gtk.WrapMode.WORD_CHAR,
            accepts_tab=False,
            left_margin=2,
            right_margin=2,
            top_margin=6,
        )
        self.view.set_vexpand(True)
        self.view.set_hexpand(True)

        self.stamp = Gtk.Label(xalign=1)
        self.stamp.add_css_class("stamp")
        self.stamp.set_width_chars(13)

        self.hint = Gtk.Label(xalign=0)
        self.hint.add_css_class("hint")
        self.hint.set_hexpand(True)

        close = Gtk.Button(label="Close")
        close.add_css_class("ink")
        close.connect("clicked", lambda *_: self.window.close())

        paste = Gtk.Button(label="Paste")
        paste.add_css_class("ink")
        paste.connect("clicked", self.on_paste)

        copy = Gtk.Button(label="Copy")
        copy.add_css_class("ink")
        copy.connect("clicked", self.on_copy)

        save = Gtk.Button(label="Save")
        save.add_css_class("ink")
        save.connect("clicked", self.on_save)

        self.delete_btn = Gtk.Button(label="Delete")
        self.delete_btn.add_css_class("ink")
        self.delete_btn.connect("clicked", self.on_delete)

        listing = Gtk.Button(label="All notes")
        listing.add_css_class("ink")
        listing.connect("clicked", lambda *_: self.show_list())

        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        actions.append(paste)
        actions.append(save)
        actions.append(self.delete_btn)
        actions.append(listing)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.append(close)
        header.append(copy)
        spacer = Gtk.Label()
        spacer.set_hexpand(True)
        header.append(spacer)
        header.append(self.stamp)

        edit = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        edit.set_margin_top(14)
        edit.set_margin_bottom(14)
        edit.set_margin_start(16)
        edit.set_margin_end(16)
        edit.append(header)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_child(self.view)
        edit.append(scroll)
        edit.append(self.hint)
        edit.append(actions)

        self.rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.list_hint = Gtk.Label(xalign=0)
        self.list_hint.add_css_class("hint")

        new_btn = Gtk.Button(label="New note")
        new_btn.add_css_class("ink")
        new_btn.connect("clicked", lambda *_: self.show_capture(force=True))

        list_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title = Gtk.Label(label="notes", xalign=0)
        title.add_css_class("paper")
        title.set_hexpand(True)
        list_header.append(title)
        list_header.append(new_btn)

        list_scroll = Gtk.ScrolledWindow()
        list_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        list_scroll.set_vexpand(True)
        list_scroll.set_child(self.rows)

        listing_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        listing_page.set_margin_top(14)
        listing_page.set_margin_bottom(14)
        listing_page.set_margin_start(14)
        listing_page.set_margin_end(14)
        listing_page.append(list_header)
        listing_page.append(self.list_hint)
        listing_page.append(list_scroll)

        self.stack = Gtk.Stack()
        self.stack.add_named(edit, "edit")
        self.stack.add_named(listing_page, "list")

        keys = Gtk.EventControllerKey()
        keys.connect("key-pressed", self._on_key)
        window.add_controller(keys)

    def _body(self) -> str:
        start, end = self.buffer.get_bounds()
        return self.buffer.get_text(start, end, True)

    def _paint(self) -> None:
        start, end = self.buffer.get_bounds()
        if start.compare(end) == 0:
            return
        self._painting = True
        try:
            self.buffer.apply_tag(self.face, start, end)
        finally:
            self._painting = False

    def _focus_editor(self) -> bool:
        self.view.grab_focus()
        return False

    def _on_changed(self, *_args) -> None:
        if self.delete_btn.get_label() == "Confirm":
            self.delete_btn.set_label("Delete")

    def _set_mode(self, mode: str) -> None:
        if mode == "list":
            self.window.add_css_class("list-mode")
            self.window.remove_css_class("note-mode")
        else:
            self.window.add_css_class("note-mode")
            self.window.remove_css_class("list-mode")

    def _set_stamp(self, when: datetime) -> None:
        self.stamp.set_text(format_stamp(when))

    def _dirty(self) -> bool:
        body = self._body()
        if self.note_id is None:
            return bool(body.strip())
        note = get_note(self.note_id)
        if note is None:
            return bool(body.strip())
        return body != note.get("body", "")

    def show_capture(self, force: bool = False) -> None:
        drafting = self.stack.get_visible_child_name() == "edit" and self._dirty()
        if drafting and not force:
            self._set_mode("note")
            self.window.present()
            GLib.idle_add(self._focus_editor)
            return
        self.note_id = None
        self.draft_created = datetime.now(timezone.utc)
        self.buffer.set_text("")
        self.hint.set_text("")
        self.delete_btn.set_visible(False)
        self.delete_btn.set_label("Delete")
        self._set_stamp(self.draft_created)
        self._set_mode("note")
        self.stack.set_visible_child_name("edit")
        self.window.present()
        GLib.idle_add(self._focus_editor)

    def show_note(self, note_id: str) -> None:
        note = get_note(note_id)
        if note is None:
            self.show_list()
            return
        self.note_id = note_id
        self.buffer.set_text(note.get("body", ""))
        self._paint()
        self._set_stamp(parse_created(note))
        self.hint.set_text("")
        self.delete_btn.set_label("Delete")
        self.delete_btn.set_visible(True)
        self._set_mode("note")
        self.stack.set_visible_child_name("edit")
        self.window.present()
        GLib.idle_add(self._focus_editor)

    def show_list(self) -> None:
        self._clear(self.rows)
        notes = list_notes()
        if not notes:
            self.list_hint.set_text("No notes yet")
        else:
            self.list_hint.set_text("")
            for note in notes:
                self.rows.append(self._row(note))
        self._set_mode("list")
        self.stack.set_visible_child_name("list")
        self.window.present()

    def _row(self, note: dict) -> Gtk.Button:
        button = Gtk.Button()
        button.add_css_class("slip")
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        stamp = Gtk.Label(label=format_stamp(parse_created(note)), xalign=0)
        stamp.add_css_class("stamp")
        stamp.set_width_chars(13)
        body = Gtk.Label(label=summary(note.get("body", "")), xalign=0)
        body.add_css_class("summary")
        body.set_hexpand(True)
        body.set_ellipsize(Pango.EllipsizeMode.END)
        box.append(stamp)
        box.append(body)
        button.set_child(box)
        note_id = note["id"]
        button.connect("clicked", lambda *_b, nid=note_id: self.show_note(nid))
        return button

    def on_paste(self, *_args) -> None:
        clipboard = self.view.get_clipboard()
        clipboard.read_text_async(None, self._pasted)

    def _pasted(self, clipboard, result) -> None:
        try:
            text = clipboard.read_text_finish(result)
        except GLib.Error:
            self.hint.set_text("Could not read the clipboard")
            return
        if not text:
            self.hint.set_text("Clipboard is empty")
            return
        self.buffer.insert_at_cursor(text)
        self.hint.set_text("")
        self.view.grab_focus()

    def on_copy(self, *_args) -> None:
        body = self._body()
        if not body:
            self.hint.set_text("Nothing to copy")
            return
        # The window's own clipboard dies with this process; wl-copy keeps serving it.
        try:
            subprocess.run(
                ["wl-copy", "--type", "text/plain;charset=utf-8"],
                input=body.encode(),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            self.view.get_clipboard().set(body)
        self.hint.set_text("Copied")

    def on_save(self, *_args) -> None:
        body = self._body()
        try:
            if self.note_id:
                note = update_note(self.note_id, body)
            else:
                note = add_note(body, created=self.draft_created)
                self.note_id = note["id"]
                self.delete_btn.set_visible(True)
        except ValueError:
            self.hint.set_text("Write something first")
            return
        self._set_stamp(parse_created(note))
        self.hint.set_text("Saved")
        ping_waybar()

    def on_delete(self, *_args) -> None:
        if not self.note_id:
            return
        if self.delete_btn.get_label() != "Confirm":
            self.delete_btn.set_label("Confirm")
            return
        delete_note(self.note_id)
        self.note_id = None
        ping_waybar()
        self.show_list()

    def _on_key(self, _controller, keyval, _keycode, state) -> bool:
        if keyval == Gdk.KEY_Escape:
            self.window.close()
            return True
        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            self.on_save()
            return True
        return False

    @staticmethod
    def _clear(box: Gtk.Box) -> None:
        child = box.get_first_child()
        while child is not None:
            nxt = child.get_next_sibling()
            box.remove(child)
            child = nxt


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
