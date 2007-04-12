%define name    kino
%define version 1.0.0
%define release %mkrel 1

Summary: 	GNOME DV-editing utility
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
Source0: 	http://prdownloads.sf.net/kino/%{name}-%{version}.tar.bz2
URL: 		http://www.kinodv.org/
License: 	GPL
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
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
Requires:	udev
Requires:	mjpegtools
Requires(post):	shared-mime-info
Requires(postun):	shared-mime-info

#gw needed by the scripts in /usr/share/kino/scripts
Requires:	ffmpeg
#it needs rawplay
Requires:	smilutils
BuildRequires:	libffmpeg-devel
Epoch:		2

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
%setup -q

%build
%configure2_5x	--with-quicktime --disable-local-ffmpeg
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%makeinstall_std
rm -rf %{buildroot}%{_sysconfdir}/hotplug/ %{buildroot}%{_libdir}/hotplug

%find_lang %{name}

mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="kino"\
title="Kino"\
longtitle="Video editor for DV format"\
needs="x11"\
icon="video_section.png"\
section="Multimedia/Video"\
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GNOME" \
  --add-category="GTK" \
  --add-category="Video" \
  --add-category="Recorder" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*
 
%post
%update_menus
update-mime-database %{_datadir}/mime > /dev/null

%postun
%update_menus 
update-mime-database %{_datadir}/mime > /dev/null

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog NEWS README* TODO
%{_sysconfdir}/udev/rules.d/kino.rules
%{_bindir}/*
%{_menudir}/*
%{_datadir}/mime/packages/kino.xml
%{_mandir}/man1/*
%{_datadir}/kino/
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_libdir}/kino-gtk2/

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}


