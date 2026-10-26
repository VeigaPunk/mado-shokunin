#!/bin/sh
# CritAssimilation (mado r44 w1): verify every quoted string at a computed locator.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
P=$L/.ufo/waves/round-44/fetch
PK=/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge
q() { # q <tag> <file> <quote>
  tag=$1; f=$2; s=$3
  hits=$(grep -nF -- "$s" "$f" | cut -d: -f1 | tr '\n' ',')
  words=$(printf '%s' "$s" | wc -w)
  printf '%-9s lines=%-6s words=%-3s %s\n' "$tag" "${hits:-MISS}" "$words" "$f"
}
q W1732  "$P/Hyprland-Window.cpp" 'void CWindow::sendWindowSize(bool force) {'
q W1741  "$P/Hyprland-Window.cpp" 'const auto REPORTSIZE = realToReportSize();'
q W1753  "$P/Hyprland-Window.cpp" 'm_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());'
q W1514  "$P/Hyprland-Window.cpp" 'void CWindow::onAck(uint32_t serial) {'
q W1520  "$P/Hyprland-Window.cpp" 'm_pendingSizeAck = *SERIAL;'
q W1526  "$P/Hyprland-Window.cpp" 'ackedSize          = m_pendingSizeAck->second; // apply pending size. We pinged, the window ponged.'
q W1865  "$P/Hyprland-Window.cpp" 'return m_wlSurface->resource()->m_current.ackedSize;'
q W2515  "$P/Hyprland-Window.cpp" '"Map request dispatched, monitor {}, window pos: {:5j}, window size: {:5j}"'
q X355   "$P/Hyprland-XDGShell.cpp" 'm_pendingApply.size = size;'
q X455   "$P/Hyprland-XDGShell.cpp" 'm_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);'
q X605   "$P/Hyprland-XDGShell.cpp" 'm_events.ack.emit(serial);'
q X635   "$P/Hyprland-XDGShell.cpp" 'm_scheduledSerial = wl_display_next_serial(g_pCompositor->m_wlDisplay);'
q XML841 "$P/xdg-shell.xml" 'The window geometry specified in the configure'
q XML1150 "$P/xdg-shell.xml" 'The width and height arguments specify a hint to the window'
q XML564 "$P/xdg-shell.xml" 'must make an ack_configure request sometime before the commit'
q XML1166 "$P/xdg-shell.xml" 'Clients must send an ack_configure in response to this event.'
q G485   "$P/gdktoplevel-wayland.c" 'gdk_toplevel_notify_compute_size (GDK_TOPLEVEL (surface), &size);'
q G492   "$P/gdktoplevel-wayland.c" 'geometry.min_width = size.min_width;'
q G503   "$P/gdktoplevel-wayland.c" 'gdk_wayland_toplevel_set_geometry_hints (wayland_toplevel, &geometry, mask);'
q G525   "$P/gdktoplevel-wayland.c" 'gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,'
q G1333  "$P/gdktoplevel-wayland.c" 'XDG_SHELL_CALL (xdg_toplevel, set_min_size, toplevel, min_width, min_height);'
q K474   "$P/gkeep-ui.py" 'window = Gtk.ApplicationWindow(application=self, title="gkeep")'
q K475   "$P/gkeep-ui.py" 'window.set_decorated(False)'
q K476   "$P/gkeep-ui.py" 'window.set_default_size(420, 500)'
q K167   "$P/gkeep-ui.py" 'close.add_css_class("ink")'
q K449   "$P/gkeep-ui.py" 'application_id="org.omarchy.gkeep"'
q CSS87  "$P/gkeep-ui.py" 'min-height: 30px;'
q CSS88  "$P/gkeep-ui.py" 'min-width: 72px;'
q R12-34 "$PK/gkeep-client-size-request-r12.md" 'the acknowledgement is tracked — which is precisely the mechanism by which a'
q R12-45 "$PK/gkeep-client-size-request-r12.md" 'The file contains **no** `set_size_request` call at all: the only size'
q R12-52 "$PK/gkeep-client-size-request-r12.md" 'a GTK4 window with no minimum-size request will adopt the size'
q R12-53 "$PK/gkeep-client-size-request-r12.md" 'The one way the rendered geometry could differ from'
q R13-39 "$PK/gkeep-rendered-geometry-record-r13.md" 'client can acknowledge or refuse; it cannot substitute a different number'
q R13-50 "$PK/gkeep-rendered-geometry-record-r13.md" 'Map request dispatched, monitor {}, window pos: {:5j}, window size: {:5j}'
q R10-41 "$PK/gkeep-size-rule-application-r10.md" "comes from the client's real size (S298):"
q R10-47 "$PK/gkeep-size-rule-application-r10.md" 'whatever the client actually used.'
q R15-40 "$PK/gkeep-geometry-never-recorded-r15.md" 'The chain of derivations the lane assembled over three rounds — the window'
