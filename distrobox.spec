Name: distrobox
Version: 1.6.0.1
Release: alt1
Summary: Another tool for containerized command line environments on Linux
License: GPL-3.0
Group: System/Configuration/Other
Url: https://github.com/89luca89/distrobox
# Source-url: https://github.com/89luca89/distrobox/archive/%version.tar.gz?/%name-%version.tar.gz
Source: %name-%version.tar
Patch: distrobox-1.6.0.1-alt-fix-nvidia-integration.patch
Patch2: distrobox-1.6.0.1-upstream-fix-sudo-password.patch

BuildRequires: %_bindir/convert

Requires: podman systemd %_bindir/cut
%filter_from_requires /\/\(usr\/\)\{0,1\}lib\/systemd\/systemd/d
%filter_from_requires /pacman/d
%filter_from_requires /dnf/d
%filter_from_requires /apt/d
%filter_from_requires /\/sbin\/init/d
%filter_from_requires /\/bin\/sh/d

%description
Use any linux distribution inside your terminal. Distrobox uses podman
or docker to create containers using the linux distribution of your
choice. Created container will be tightly integrated with the host,
allowing to share the HOME directory of the user, external storage,
external usb devices and graphical apps (X11/Wayland) and audio.

%prep
%setup
%patch -p1
%patch2 -p1

%build
%install
./install -P %buildroot/%prefix

# Move the icon
mkdir -p %buildroot%_iconsdir/hicolor/scalable/apps
mv %buildroot%_iconsdir/terminal-distrobox-icon.svg \
%buildroot%_iconsdir/hicolor/scalable/apps
# Generate more icon sizes
for sz in 16 22 24 32 36 48 64 72 96 128 256; do
  mkdir -p %buildroot%_iconsdir/hicolor/${sz}x${sz}/apps
  convert terminal-distrobox-icon.svg -resize ${sz}x${sz} \
%buildroot%_iconsdir/hicolor/${sz}x${sz}/apps/terminal-distrobox-icon.png
done

%check
%buildroot%_bindir/%name list -V
for i in create enter export init list rm stop host-exec; do
%buildroot%_bindir/%name-$i -V
done

%files
%_man1dir/%{name}*
%_bindir/%name
%_bindir/%name-create
%_bindir/%name-enter
%_bindir/%name-export
%_bindir/%name-init
%_bindir/%name-list
%_bindir/%name-rm
%_bindir/%name-stop
%_bindir/%name-host-exec
%_bindir/%name-ephemeral
%_bindir/%name-generate-entry
%_bindir/%name-upgrade
%_bindir/%name-assemble
%_iconsdir/hicolor/*/apps/terminal-distrobox-icon.png
%_iconsdir/hicolor/scalable/apps/terminal-distrobox-icon.svg
%_datadir/bash-completion/completions/%{name}*

%changelog
* Tue Feb 20 2024 Boris Yumankulov <boriabloger@altlinux.org> 1.6.0.1-alt1
- new version (1.6.0.1) with rpmgs script

