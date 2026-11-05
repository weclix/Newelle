# __main__.py
#
# Launcher for the installed Python package (entry point newelle.__main__:main).
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gettext
import os
import signal
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

APP_ID = 'io.github.qwersyk.Newelle'
DATA_DIR = Path(__file__).resolve().parent / '_data'
SHARE_DIR = DATA_DIR / 'share'


def setup_environment():
    """Expose the bundled schema, icons and translations to GLib and GTK.

    GLib reads these variables once, so this must run before Gio or Gtk is used.
    The schema goes through GSETTINGS_SCHEMA_DIR because it takes precedence
    over every data dir; a stale schema left in ~/.local/share by an old
    install would otherwise shadow the bundled one.
    """
    schema_dirs = [str(SHARE_DIR / 'glib-2.0' / 'schemas')]
    if os.environ.get('GSETTINGS_SCHEMA_DIR'):
        schema_dirs.append(os.environ['GSETTINGS_SCHEMA_DIR'])
    os.environ['GSETTINGS_SCHEMA_DIR'] = os.pathsep.join(schema_dirs)

    data_dirs = os.environ.get('XDG_DATA_DIRS') or '/usr/local/share:/usr/share'
    os.environ['XDG_DATA_DIRS'] = os.pathsep.join([str(SHARE_DIR), data_dirs])

    localedir = str(SHARE_DIR / 'locale')
    gettext.bindtextdomain('newelle', localedir)
    gettext.textdomain('newelle')
    gettext.install('newelle', localedir)


def preload_gtk4_layer_shell():
    """Load gtk4-layer-shell before GTK pulls in libwayland-client.

    The library hooks libwayland-client, so it only works when loaded first;
    otherwise Gtk4LayerShell.is_supported() reports False and Voice Mode
    falls back to X11 positioning.
    """
    import ctypes

    try:
        ctypes.CDLL('libgtk4-layer-shell.so.0', mode=ctypes.RTLD_GLOBAL)
    except OSError:
        pass


def forward_voice_request(arguments):
    """Toggle an existing instance without importing the UI or AI handlers."""
    if arguments != ['--voice']:
        return None

    from gi.repository import Gio, GLib

    try:
        connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        owner = connection.call_sync(
            'org.freedesktop.DBus',
            '/org/freedesktop/DBus',
            'org.freedesktop.DBus',
            'GetNameOwner',
            GLib.Variant('(s)', (APP_ID,)),
            GLib.VariantType.new('(s)'),
            Gio.DBusCallFlags.NO_AUTO_START,
            1000,
            None,
        ).unpack()[0]
    except GLib.Error:
        # No existing instance (or no session bus): use normal startup.
        return None

    platform_data = {}
    for variable, key in (
        ('DESKTOP_STARTUP_ID', 'desktop-startup-id'),
        ('XDG_ACTIVATION_TOKEN', 'activation-token'),
    ):
        value = os.environ.get(variable)
        if value:
            platform_data[key] = GLib.Variant('s', value)
    try:
        # Target the unique owner so a concurrent shutdown cannot cause D-Bus
        # to launch another instance or deliver the toggle to a replacement.
        connection.call_sync(
            owner,
            '/io/github/qwersyk/Newelle',
            'org.freedesktop.Application',
            'ActivateAction',
            GLib.Variant('(sava{sv})', ('voice_mode', [], platform_data)),
            GLib.VariantType.new('()'),
            Gio.DBusCallFlags.NO_AUTO_START,
            5000,
            None,
        )
    except GLib.Error as error:
        if Gio.DBusError.get_remote_error(error) in {
            'org.freedesktop.DBus.Error.NameHasNoOwner',
            'org.freedesktop.DBus.Error.ServiceUnknown',
            'org.freedesktop.DBus.Error.UnknownObject',
            'org.freedesktop.DBus.Error.UnknownMethod',
        }:
            return None
        # Do not retry an uncertain delivery (e.g. a timeout): a second toggle
        # could close the pill that the first request just opened.
        print(error, file=sys.stderr)
        return 1
    return 0


def main():
    setup_environment()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    preload_gtk4_layer_shell()

    forwarded_status = forward_voice_request(sys.argv[1:])
    if forwarded_status is not None:
        return forwarded_status

    from gi.repository import Gio
    resource = Gio.Resource.load(str(DATA_DIR / 'newelle.gresource'))
    resource._register()

    try:
        app_version = version('newelle')
    except PackageNotFoundError:
        app_version = 'unknown'

    from newelle import main as app
    return app.main(app_version)


if __name__ == '__main__':
    sys.exit(main())
