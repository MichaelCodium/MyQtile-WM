import  os
from collections.abc import Callable

import libqtile.resources
import subprocess
from libqtile import hook
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
    
    #wallpaper
    subprocess.run(["feh", "--bg-fill", "/mnt/storage/Media/Picture/Wallpaper/victoria-harbour-6144x3456-11445.jpg"])

    #Screen locker process
    subprocess.Popen(["xfce4-screensaver"])
mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Alt_L", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle stack splitting"),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.spawn("xfce4-appfinder")), 

    # Launch apps/commands
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Raise volume by 5 percent"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Lower volume by 5 percent"),
    Key(["mod4"], "t", lazy.spawn("xfce4-taskmanager"), desc="Launch Task Manager"),
    Key(["mod4"], "l", lazy.spawn("xfce4-screensaver-command --lock"), desc="Lock the screen"),
    Key([mod], "f", lazy.spawn("thunar"), desc="Launch file browser Thunar"),
    Key([mod], "b", lazy.spawn("firefox"), desc="Launch browser Firefox"),   
    Key([mod], "v", lazy.spawn("pavucontrol"), desc="Launch volume interface Pavucontrol"),
    Key([mod], "s", lazy.spawn("scrot -e 'mv $f /home/xunlai/Pictures/Screenshots/ && notify-send \"Screenshot saved\"'")),
     
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# Swith between workspaces/groups and also take windows to suchs
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus="0362fc", border_width=2, margin=8),
    layout.Bsp(border_focus="0362fc", border_width=2, margin=8),
    layout.Max(border_width=1, margin=4),
    layout.MonadWide(border_focus="0362fc", border_width=2, margin=8),
    layout.Matrix(border_focus="0362fc", border_width=2, margin=8),
    #layout.MonadTall(border_focus="#3483eb", border_normal="#3483eb", border_width=5, margin=4),
    #layout.Stack(num_stacks=2),
    
    
    #layout.RatioTile(border_focus="0362fc", border_width=2, margin=8),
    #layout.Tile(border_focus="0362fc", border_width=2, margin=8),
    #layout.TreeTab(),
    #layout.VerticalTile(border_focus="0362fc", border_width=2, margin=8),
    #layout.Zoomy(border_focus="0362fc", border_width=2, margin=8),
]

widget_defaults = dict(
    font="TerminessTTF Nerd Font",
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
screens = [
    Screen(
        top=bar.Bar(
            [
               widget.CurrentLayout(
                            fontsize=(17),
               ),
               widget.GroupBox(
                            fontsize=(17),
               ),
               #widget.Prompt(),
              widget.TextBox("",
                            fontsize=(90),
                            foreground="000000",
                            background='8F8F88',
                            padding=-14,
                            ),
               widget.TextBox(" ",
                            fontsize=(1),
                            background='8F8F88',
                            ),
                widget.WindowName(
                            
                            foreground="ffffff",
                            background="8F8F88",
                    
                            ),
                widget.Chord(
                            chords_colors={
                            "launch": ("#ff0000", "#ffffff"),
                            },
                            name_transform=lambda name: name.upper(),
                            ),
              widget.TextBox("",
                            fontsize=(90),
                            foreground="8F8F88",
                            background='ffffff',
                            padding=-14,
                            ),
               widget.TextBox(" ",
                            fontsize=(1),
                            background='ffffff',
                            ),
                 widget.Systray(
                            icon_size=(24),
                            background="ffffff"
                    
                            ),
                widget.TextBox(" ",
                            fontsize=(1),
                            background='ffffff',
                            ),
                widget.TextBox("",
                            fontsize=(90),
                            foreground="ffffff",
                            background='3483eb',
                            padding=-14,
                            ),
               widget.TextBox(" ",
                            fontsize=(1),
                            background='3483eb',
                            ),
                widget.TextBox("󰻠",
                            fontsize=(35),
                            background='3483eb',
                            ),
                widget.CPU(
                            background='3483eb',
                            format='{load_percent:>6.2f}% '
                            ),
                widget.TextBox("󰏈",
                            fontsize=(30),
                            background="3483eb"
                            ),
                widget.ThermalSensor(
                            tag_sensor="Core 0",
                            background="3483eb",
                            update_interval=1,
                            
                            ),                           
                widget.TextBox("",
                            fontsize=(90),
                            foreground="3483eb",
                            background='0dd459',
                            padding=-14,
                            ),
                widget.TextBox("  ",
                            fontsize=(1),
                            background='0dd459',
                            ),
                widget.TextBox("",
                            fontsize=(30),
                            background='0dd459',
                            ),
                widget.Memory(
                            background='0dd459',
                            format='{MemUsed:.0f}{mm}',
                            ),
                #Swidget.TextBox(" "),
                widget.TextBox("",
                            fontsize=(90),
                            foreground="0dd459",
                            background='9f11c2',
                            padding=-14,
                            ),
               widget.TextBox(" ",
                            fontsize=(1),
                            background='9f11c2',
                            ),
               widget.TextBox("󰈀",
                            fontsize=(30),
                            background='9f11c2',
                            ),
                widget.Net(
                            background='9f11c2',
                            format='{down} ↓↑ {up}'
                            ),
                widget.TextBox("",
                            fontsize=(90),
                            foreground="9f11c2",
                            background='c2b911',
                            padding=-14,
                            ),
                widget.TextBox(" ",
                            fontsize=(1),
                            background='c2b911',
                            ),
                widget.TextBox("",
                            fontsize=(30),
                            background='c2b911',
                            ),
                widget.Clock(
                            background='c2b911',
                            format="%a %dth %H:%M "
                            ),
               widget.TextBox("",
                            fontsize=(90),
                            foreground="c2b911",
                            background='000000',
                            padding=-14,
                            ),
             widget.QuickExit(
                            default_text=('󰐥'),
                            countdown_format='{}',
                            fontsize=(35),
                            max_chars=(0),
                            ),
              widget.TextBox(" ",
                            fontsize=(1),
                            background='000000',
                            ), 
            ],
            34,
            border_width=[1, 1, 1, 1],  # Draw top and bottom borders
            margin=[4,4,4,4],
            border_color="0362fc"  # Borders are magenta
        ),
    ),
]

# Instead of screens, you can define a function here to specify which Screen
# should correspond to which Output.
fake_screens: list[Screen] | None = None

# Instead of screens or fake screens, you can define a function here that
# returns a list of Screen objects based on the list of Outputs; that way you
# can decide based on e.g. the number of screens, or which ports are plugged
# in exactly what do render in each bar for each screen.
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_timers = []  # type: list
idle_inhibitors = []  # type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
