# archlinux-logout

Graphical logout and lock screen utility for Arch Linux, maintained by Sugarcrisp-ui.

## Dependencies

- python
- python-gobject
- libwnck3
- python-psutil
- python-cairo
- python-distro
- i3lock-color
- betterlockscreen (optional, for enhanced lock screen features)

## Installation

```bash
git clone https://github.com/Sugarcrisp-ui/archlinux-logout.git
cd archlinux-logout
makepkg -si

If symlink fails, run the following
ln -sf ~/dotfiles/.config/archlinux-logouts/archlinux-logout.conf ~/.config/archlinux-logout/archlinux-logout.conf

This widget, displays a transparent window allowing quick access to various power features:

- Logout (L)
- Reboot (R)
- Shutdown (S)
- Suspend (U)
- Hibernate (H)
- Lock (K)

Additional configuration provided includes:

- Setting the widget opacity
- Icon size
- Font size
- Theme selection

More info about the tool via our 21+ videos

https://www.youtube.com/playlist?list=PLlloYVGq5pS7KfhUhcQaUAGV28kmA2OSt


