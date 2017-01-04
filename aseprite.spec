Name:           aseprite-gpl
Version:        1.1.8
Release:        1
Summary:        Animated sprite editor & pixel art tool
Group:          Graphics/Editors and Converters
License:        GPLv2+
URL:            https://github.com/aseprite-gpl/aseprite/

Source0:        %{name}-%{version}.tar.gz


BuildRequires:  cmake
BuildRequires:  pkgconfig(x11)

%description
Aseprite (aka ASE, Allegro Sprite Editor) is an open source program to
create animated sprites & pixel art. Sprites are little images that can
be used in your website or in a video game. You can draw characters with
movement, intros, textures, patterns, backgrounds, logos, color palettes,
isometric levels, etc.

Since the official upstream Aseprite source code is not free software 
anymore, this is a fork based in the latest GPLv2 version.

%prep

%setup -q

# Stable version
sed -i data/gui.xml src/config.h -e 's/-dev//'

%build

mkdir build; cd build

%cmake .. -DENABLE_UPDATER=OFF \
       -DENABLE_WEBSERVER=OFF \
       -DLIBPIXMAN_INCLUDE_DIR:PATH=%{_includedir}/pixman-1 \
       -DLIBPIXMAN_LIBRARY:FILEPATH=%{_libdir}/libpixman-1.so
%make_build
cd ..

%install
%make_install -C build

for size in 16 32 48 64; do
  install -D -m644 data/icons/ase${size}.png \
          %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/aseprite.png
done

install -d %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/aseprite.desktop
[Desktop Entry]
Name=Aseprite
GenericName=Sprite editor
Comment=%{summary}
Exec=aseprite
Icon=aseprite
Type=Application
Categories=Graphics;2DGraphics;RasterGraphics;
EOF

%files
%doc CONTRIBUTING.md README.md
%{_bindir}/aseprite
%{_datadir}/aseprite/
%{_datadir}/applications/aseprite.desktop
%{_datadir}/icons/hicolor/*/apps/aseprite.png
