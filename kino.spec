Summary: 	GNOME DV-editing utility
Name: 		kino
Version:	1.3.4
Release: 	8
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

%changelog
* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 2:1.3.4-8
+ Revision: 677486
- bump rel
- cleanup spec file
- build with kernel > 2.6.38.2

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.3.4-7
+ Revision: 666028
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.3.4-6mdv2011.0
+ Revision: 606264
- rebuild

* Mon Nov 09 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2:1.3.4-5mdv2010.1
+ Revision: 463541
- rebuild for new ffmpeg

* Fri Nov 06 2009 Colin Guthrie <cguthrie@mandriva.org> 2:1.3.4-4mdv2010.1
+ Revision: 460802
- Due to use of OSS, kino should use soundwrapper

* Wed Sep 09 2009 Frederik Himpe <fhimpe@mandriva.org> 2:1.3.4-3mdv2010.0
+ Revision: 435963
- Update to new version 1.3.4
- Rediff desktop file patch

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Mon Feb 09 2009 Funda Wang <fwang@mandriva.org> 2:1.3.3-2mdv2009.1
+ Revision: 338845
- mp3lame patch not needed anymore (fixed already in 1.3.0)

* Thu Jan 29 2009 Funda Wang <fwang@mandriva.org> 2:1.3.3-1mdv2009.1
+ Revision: 335164
- New version 1.3.3

* Mon Dec 29 2008 Funda Wang <fwang@mandriva.org> 2:1.3.2-4mdv2009.1
+ Revision: 320833
- fix str fmt

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sat Nov 08 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.3.2-3mdv2009.1
+ Revision: 301004
- rebuilt against new libxcb

* Tue Oct 14 2008 Adam Williamson <awilliamson@mandriva.org> 2:1.3.2-2mdv2009.1
+ Revision: 293772
- nuke stray Source0 line
- rebuild for new ffmpeg major
- clean up the requires
- improve snapshot / release conditionals

* Thu Aug 21 2008 Funda Wang <fwang@mandriva.org> 2:1.3.2-1mdv2009.0
+ Revision: 274528
- New version 1.3.2

* Wed Aug 13 2008 Funda Wang <fwang@mandriva.org> 2:1.3.1-1mdv2009.0
+ Revision: 271383
- BR intltool
- New version 1.3.1

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Apr 30 2008 Funda Wang <fwang@mandriva.org> 2:1.3.0-1mdv2009.0
+ Revision: 199384
- add ffmpeg includedir
- Rediff ffmpeg patch
- New version 1.3.0

* Sat Mar 08 2008 Anssi Hannula <anssi@mandriva.org> 2:1.2.0-5mdv2008.1
+ Revision: 182224
- do not change encoder names for backports

* Tue Feb 05 2008 Adam Williamson <awilliamson@mandriva.org> 2:1.2.0-4mdv2008.1
+ Revision: 162530
- add ffmpeg.patch and a couple of sed substitutions to fix encoder names that have been changed in recent ffmpeg (#37467)
- drop mjpegopts.patch (turned out to be useless)

* Wed Jan 09 2008 Adam Williamson <awilliamson@mandriva.org> 2:1.2.0-3mdv2008.1
+ Revision: 146991
- hopefully fix #36533 (uses non-existent options for yuvdeinterlace and yuvdenoise) with mjpegopts.patch

* Sat Jan 05 2008 Adam Williamson <awilliamson@mandriva.org> 2:1.2.0-2mdv2008.1
+ Revision: 145651
- new license policy
- remove creation of a symlink (fixed upstream)
- fd.o icons (bug #36410)
- minor cleanups

* Wed Jan 02 2008 Funda Wang <fwang@mandriva.org> 2:1.2.0-1mdv2008.1
+ Revision: 140297
- Fix desktop file

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Giuseppe GhibÃ² <ghibo@mandriva.com>
    - Release 1.2.0.

* Tue Aug 07 2007 Funda Wang <fwang@mandriva.org> 2:1.1.1-1mdv2008.0
+ Revision: 59712
- New version 1.1.1

* Tue Jul 24 2007 Funda Wang <fwang@mandriva.org> 2:1.1.0-1mdv2008.0
+ Revision: 54920
- New version 1.1.0

* Fri Jul 13 2007 Adam Williamson <awilliamson@mandriva.org> 2:1.0.1-0.20070712.1mdv2008.0
+ Revision: 51759
- bump to latest CVS to test fix for #31867

* Sun Jul 08 2007 Adam Williamson <awilliamson@mandriva.org> 2:1.0.0-2mdv2008.0
+ Revision: 49653
- fix kino2raw symlink (#31792)


* Wed Mar 14 2007 Austin Acton <austin@mandriva.org> 1.0.0-1mdv2007.1
+ Revision: 143841
- 1.0.0
- remove unneeded patches
- force system ffmpeg

* Thu Mar 01 2007 Emmanuel Andry <eandry@mandriva.org> 2:0.9.5-2mdv2007.1
+ Revision: 130399
- rebuild for libgii

* Wed Jan 17 2007 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 2:0.9.5-1mdv2007.1
+ Revision: 110002
- add desktop-file-utils to buildrequires
- build against libffmpeg on all platforms
- new release: 0.9.6
  regenerate P1
  some spec cleaning/cosmetics

* Fri Dec 22 2006 Christiaan Welvaart <spturtle@mandriva.org> 2:0.9.2-2mdv2007.1
+ Revision: 101543
- add BuildRequires: libdv-devel libiec61883-devel libxv-devel
- Import kino

* Wed Sep 06 2006 Nicolas Lécureuil <neoclust@mandriva.org> 2:0.9.2-1mdv2007.0
- New version 0.9.2

* Mon Jul 17 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.8.1-1mdv2007.0
- XDG

* Thu Apr 20 2006 Stefan van der Eijk <stefan@eijk.nu> 2:0.8.1-3mdk
- fix x86_64 build

* Wed Apr 19 2006 Stefan van der Eijk <stefan@eijk.nu> 2:0.8.1-2mdk
- BuildRequires: alsa-lib-devel & perl-XML-Parser

* Wed Apr 19 2006 Jerome Martin <jmartin@mandriva.org> 2:0.8.1-1mdk
- 0.8.1
- BuildRequires: libquicktime-devel and remove BuildConflict

* Tue Apr 18 2006 Stefan van der Eijk <stefan@eijk.nu> 0.7.6-5mdk
- %%mkrel
- BuildRequires
- Remove "BuildRequires: libquicktime-devel" for now
- URL

* Sat Sep 03 2005 Olivier Blin <oblin@mandriva.com> 0.7.6-4mdk
- require udev instead of hotplug

* Sun Aug 28 2005 Olivier Blin <oblin@mandriva.com> 0.7.6-3mdk
- move broken hotplug script to udev rule

* Sat Jul 23 2005 Laurent MONTEL <lmontel@mandriva.com> 0.7.6-2mdk
- Fix build on MDK <= 2006

* Tue May 31 2005 Götz Waschk <waschk@mandriva.org> 0.7.6-1mdk
- update file list
- patch for new libquicktime
- new source URL
- New release 0.7.6

* Sat Feb 12 2005 Austin Acton <austin@mandrake.org> 0.7.5-3mdk
- requires mjpegtools

* Sat Jan 29 2005 Austin Acton <austin@mandrake.org> 0.7.5-2mdk
- rebuild for libraw1394

* Fri Dec 03 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.5-1mdk
- always define hotplugdir
- new version

* Sat Oct 23 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.7.3-2mdk
- hotplugdir fixes

* Wed Aug 11 2004 Austin Acton <austin@mandrake.org> 0.7.3-1mdk
- 0.7.3

* Wed Jul 28 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.2-1mdk
- drop patch 1
- fix URLs
- New release 0.7.2

* Thu Jun 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.7.1-4mdk
- Rebuild

* Mon May 24 2004 Austin Acton <austin@mandrake.org> 0.7.1-3mdk
- requires smilutils

* Fri May 14 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.1-2mdk
- fix devel deps

* Thu Apr 15 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.1-1mdk
- add hotplug and locale files
- fix buildrequires
- fix menu entry
- new version

* Thu Apr 15 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.0-5mdk
- new version

* Sat Apr 03 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.0-5mdk
- new dv

