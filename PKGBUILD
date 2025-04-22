# Maintainer: Sugarcrisp-ui <brettcrisp2@gmail.com>
pkgname=i3-logout
pkgver=1.0
pkgrel=4
pkgdesc="Graphical logout and lock screen utility for i3, maintained by Sugarcrisp-ui"
arch=('any')
url="https://github.com/Sugarcrisp-ui/i3-logout"
license=('GPL3')
depends=('python' 'python-gobject' 'libwnck3' 'python-psutil' 'python-cairo' 'python-distro' 'i3lock-color')
install=i3-logout.install
source=(
  'i3-logout.install'
  'i3-logout-files.tar.gz'
)
noextract=('i3-logout-files.tar.gz')
sha256sums=(
  'e1f5ef275d79b086504e02ac4f4f33c0e72184ca5af65f42fbe331e5ec098725'
  '527a10f8fe5bb90c52d3b1900a91b1e9f4bdf1b1a9d81a5c7309f11fa59a9f40'
)

package() {
  # Extract tarball
  tar -xzf "$srcdir/i3-logout-files.tar.gz" -C "$srcdir"

  # Install config
  install -Dm644 "$srcdir/etc/i3-logout.conf" "$pkgdir/etc/i3-logout.conf"

  # Install binaries
  install -Dm755 "$srcdir/usr/bin/i3-logout" "$pkgdir/usr/bin/i3-logout"
  install -Dm755 "$srcdir/usr/bin/betterlockscreen" "$pkgdir/usr/bin/betterlockscreen"

  # Install desktop file
  install -Dm644 "$srcdir/usr/share/applications/betterlockscreen.desktop" \
    "$pkgdir/usr/share/applications/betterlockscreen.desktop"

  # Install Python files
  install -d "$pkgdir/usr/share/i3-logout"
  cp -r "$srcdir/usr/share/i3-logout/"*.py "$pkgdir/usr/share/i3-logout/"

  install -d "$pkgdir/usr/share/betterlockscreen"
  cp -r "$srcdir/usr/share/betterlockscreen/"*.py "$pkgdir/usr/share/betterlockscreen/"

  # Install images and wallpapers
  install -d "$pkgdir/usr/share/betterlockscreen/images"
  cp -r "$srcdir/usr/share/betterlockscreen/images/"* "$pkgdir/usr/share/betterlockscreen/images/"

  install -d "$pkgdir/usr/share/betterlockscreen/wallpapers"
  cp -r "$srcdir/usr/share/betterlockscreen/wallpapers/"* "$pkgdir/usr/share/betterlockscreen/wallpapers/"

  # Install themes
  install -d "$pkgdir/usr/share/i3-logout-themes"
  cp -r "$srcdir/usr/share/i3-logout-themes/"* "$pkgdir/usr/share/i3-logout-themes/"

  # Install icon
  install -Dm644 "$srcdir/usr/share/icons/hicolor/scalable/apps/better-lock-screen.svg" \
    "$pkgdir/usr/share/icons/hicolor/scalable/apps/better-lock-screen.svg"

  # Install documentation
  install -d "$pkgdir/usr/share/doc/i3-logout"
  cp -r "$srcdir/usr/share/doc/i3-logout/"* "$pkgdir/usr/share/doc/i3-logout/"
}
