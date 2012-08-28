Summary:	GNOME DV-editing utility
Name: 		kino
Version:	1.3.4
Release:	9
Epoch:		2
License:	GPLv2+
Group:		Video
URL:		http://www.kinodv.org/
Source0: 	http://downloads.sourgeforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		kino-1.3.4-fix-desktop-file.patch
Patch1:		kino-1.3.4-videodev.h.patch
Patch2:		kino-1.3.2-fix-str-fmt.patch
Patch3:		kino-1.3.4-use-soundwrapper.patch
Patch4:		kino-1.3.4-ffmpeg0.8.patch
Patch5:		kino-1.3.4-libav-0.8.patch
Patch6:		kino-1.3.4-link.patch
BuildRequires:	a52dec-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libavc1394)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libiec61883)
BuildRequires:	pkgconfig(libquicktime)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	imagemagick
Requires:	udev
Requires:	mjpegtools
Requires:	soundwrapper
#gw needed by the scripts in /usr/share/kino/scripts
Requires:	ffmpeg
#it needs rawplay
Requires:	smilutils

%description
The new generation of digital camcorders use the Digital Video (DV) data
format. Kino allows you to record, create, edit, and play movies recorded
with DV camcorders. Unlike other editors, this program uses many keyboard
commands for fast navigating and editing inside the movie.

%package	devel
Group:		Development/C++
Summary:	Header files for kino plugin development
Requires:	%{name} = %{EVRD}
Requires:	pkgconfig(samplerate)
Requires:	pkgconfig(libdv)
Requires:	pkgconfig(libgnomeui-2.0)
Requires:	pkgconfig(libxml-2.0)
Requires:	ffmpeg-devel

%description	devel
This contains the C++ headers needed to build extensions for kino.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p0

%build
autoreconf -fi
# More ffmpeg encoder name changes
sed -i -e 's,vcodec h264,vcodec libx264,g' scripts/exports/*
sed -i -e 's,acodec mp3,acodec libmp3lame,g' scripts/exports/ffmpeg_mp3.sh
#export CPPFLAGS="%{optflags} -I%{_includedir}/libavcodec -I%{_includedir}/libavdevice -I%{_includedir}/libavformat -I%{_includedir}/libavcodec -I%{_includedir}/libpostproc -I%{_includedir}/libswscale"
%configure2_5x	--enable-quicktime --disable-local-ffmpeg
%make

%install
mkdir -p %{buildroot}%{_bindir}
%makeinstall_std

rm -rf %{buildroot}%{_sysconfdir}/hotplug/ %{buildroot}%{_libdir}/hotplug

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog NEWS README* TODO
%{_sysconfdir}/udev/rules.d/kino.rules
%{_bindir}/*
%{_datadir}/mime/packages/kino.xml
%{_mandir}/man1/*
%{_datadir}/kino/
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%{_libdir}/kino-gtk2/

%files devel
%{_includedir}/%{name}

