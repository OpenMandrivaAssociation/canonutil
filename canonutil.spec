%define		extraversion %nil

Summary: 	Maintenance tool for Canon inkjet printers
Name: 		canonutil
Version: 	0.07
Release: 	9
License: 	GPL
Group: 		Graphics
URL: 		http://xwtools.automatix.de/
Source0: 	CanonUtil-%{version}%{extraversion}.tar.bz2
Source1:	canonutil.png.bz2
Patch0:		canonuti-0.07-fltk-1.1.patch
BuildRequires: 	libfltk-devel
BuildRequires:	mesaglu-devel
BuildRequires:  imagemagick
ExclusiveArch:  %{ix86}

%description
CanonUtil does all needed maintenance tasks for Canon inkjet printers:

- Nozzle check page
- Nozzle cleaning
- Nozzle adjustment
- Printer reset
- Power saving control

%prep
%setup -q -n CanonUtil-%{version}%{extraversion}
%patch0 -p1
bzcat %{SOURCE1} > icon.png

# Fix path for help file
perl -p -i -e 's:CanonUtil.html:/usr/lib/CanonUtil/CanonUtil.html:' CanonUtilFltkMw.cpp

#if [ -d /usr/lib64 ]; then
#  perl -p -i -e 's:lib:lib64:' configure
#fi

%build
./configure --prefix /usr

%make fltk

# convert icons to required format
convert icon.png -resize 32x32 canonutil.png
convert icon.png -resize 16x16 canonutil_mini.png
convert icon.png -resize 48x48 canonutil_large.png

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}

# The Makefile does not support DESTDIR
./configure --prefix %{buildroot}/usr

# We cannot SUID root the executable here, so de-activate appropriate lines
# in the Makefile
perl -p -i -e 's/chmod/:/' Makefile
perl -p -i -e 's/chown/:/' Makefile

%makeinstall install-fltk

# icons
install -d %{buildroot}%{_datadir}/icons
install -m 644 canonutil.png %{buildroot}%{_datadir}/icons/
install -d %{buildroot}%{_datadir}/icons/mini
install -m 644 canonutil_mini.png %{buildroot}%{_datadir}/icons/mini/canonutil.png
install -d %{buildroot}%{_datadir}/icons/large
install -m 644 canonutil_large.png %{buildroot}%{_datadir}/icons/large/canonutil.png

# menu stuff
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-canonutil.desktop
[Desktop Entry]
Type=Application
Exec=/usr/bin/CanonUtil
Name=CanonUtil
Comment=Maintenance tool for Canon inkjet printers
Categories=HardwareSettings;
Icon=canonutil
EOF

%files
%doc CHANGES.txt LICENCE.txt README
# This should run SGID sys, so that it can access the printer device files
# when started by a normal user
%attr(2755,lp,sys) %_bindir/CanonUtil
%{_libdir}/CanonUtil
%{_datadir}/applications/mandriva-*.desktop
%{_datadir}/icons/*.png
%{_datadir}/icons/mini/*.png
%{_datadir}/icons/large/*.png



%changelog
* Fri Jun 15 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.07-8
+ Revision: 805866
- rebuild for fltk libs
- cleaned up spec

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.07-7mdv2011.0
+ Revision: 610095
- rebuild

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.07-6mdv2010.0
+ Revision: 436930
- rebuild

* Sat Dec 13 2008 Funda Wang <fwang@mandriva.org> 0.07-5mdv2009.1
+ Revision: 313960
- add patch fixing build with fltk 1.1

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.07-5mdv2009.0
+ Revision: 243434
- rebuild
- fix mesaglu-devel BR

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 0.07-3mdv2008.1
+ Revision: 132878
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Rebuilt.
    - Import canonutil




* Thu Jan 19 2006 Till Kamppeter <till@mandriva.com> 0.07-2mdk
- Does not work on 64-bit -> Added "ExclusiveArch: %%{ix_86}".
- Introduced %%mkrel.

* Sun Nov 28 2003 Till Kamppeter <till@mandrakesoft.com> 0.07-1mdk
- Updated to version 0.07.

* Fri Sep 12 2003 Till Kamppeter <till@mandrakesoft.com> 0.03-1mdk
- Initial release.
