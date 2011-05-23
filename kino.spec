Summary: 	GNOME DV-editing utility
Name: 		kino
Version:	1.3.4
Release: 	8
Epoch:		2
Source0: 	http://downloads.sourgeforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		kino-1.3.4-fix-desktop-file.patch
Patch1:		kino-1.3.4-videodev.h.patch
Patch2:		kino-1.3.2-fix-str-fmt.patch
Patch3:		kino-1.3.4-use-soundwrapper.patch
URL: 		http://www.kinodv.org/
License: 	GPLv2+
Group: 		Video
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	a52dec-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	libavc1394-devel
BuildRequires:	libdv-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libiec61883-devel
BuildRequires:	libquicktime-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libxv-devel
BuildRequires:	libv4l-devel
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libsamplerate-devel
Requires:	libdv-devel
Requires:	libgnomeui2-devel
Requires:	libxml2-devel
Requires:	libffmpeg-devel

%description	devel
This contains the C++ headers needed to build extensions for kino.

%prep
%setup -qn %{name}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1

%build
# More ffmpeg encoder name changes
sed -i -e 's,vcodec h264,vcodec libx264,g' scripts/exports/*
sed -i -e 's,acodec mp3,acodec libmp3lame,g' scripts/exports/ffmpeg_mp3.sh
#export CPPFLAGS="%{optflags} -I%{_includedir}/libavcodec -I%{_includedir}/libavdevice -I%{_includedir}/libavformat -I%{_includedir}/libavcodec -I%{_includedir}/libpostproc -I%{_includedir}/libswscale"
%configure2_5x	--enable-quicktime --disable-local-ffmpeg
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%makeinstall_std

rm -rf %{buildroot}%{_sysconfdir}/hotplug/ %{buildroot}%{_libdir}/hotplug

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_includedir}/%{name}

