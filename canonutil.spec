%define		extraversion %nil

Summary: 	Maintenance tool for Canon inkjet printers
Name: 		canonutil
Version: 	0.07
Release: 	%mkrel 3
License: 	GPL
Group: 		Graphics
Source0: 	CanonUtil-%{version}%{extraversion}.tar.bz2
Source1:	canonutil.png.bz2
URL: 		http://xwtools.automatix.de/
BuildRequires: 	libfltk-devel libMesaGLU-devel
BuildRequires:  ImageMagick
Prefix: 	%{_prefix}
ExclusiveArch:  %{ix86}

%description
CanonUtil does all needed maintenance tasks for Canon inkjet printers:

- Nozzle check page
- Nozzle cleaning
- Nozzle adjustment
- Printer reset
- Power saving control

%prep
rm -rf ${RPM_BUILD_DIR}/%{name}-%{version}%{extraversion}
rm -rf ${RPM_BUILD_DIR}/%{name}

%setup -q -n CanonUtil-%{version}%{extraversion}
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

rm -fr %buildroot
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}

# The Makefile does not support DESTDIR
./configure --prefix %{buildroot}/usr

# We cannot SUID root the executable here, so de-activate appropriate lines
# in the Makefile
perl -p -i -e 's/chmod/:/' Makefile
perl -p -i -e 's/chown/:/' Makefile

%makeinstall install-fltk

%find_lang %{name}

# icons
install -d $RPM_BUILD_ROOT%{_datadir}/icons
install -m 644 canonutil.png $RPM_BUILD_ROOT%{_datadir}/icons/
install -d $RPM_BUILD_ROOT%{_datadir}/icons/mini
install -m 644 canonutil_mini.png $RPM_BUILD_ROOT%{_datadir}/icons/mini/canonutil.png
install -d $RPM_BUILD_ROOT%{_datadir}/icons/large
install -m 644 canonutil_large.png $RPM_BUILD_ROOT%{_datadir}/icons/large/canonutil.png

# menu stuff
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-canonutil.desktop
[Desktop Entry]
Type=Application
Exec=/usr/bin/CanonUtil
Name=CanonUtil
Comment=Maintenance tool for Canon inkjet printers
Categories=HardwareSettings;
Icon=canonutil
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CHANGES.txt LICENCE.txt README
# This should run SGID sys, so that it can access the printer device files
# when started by a normal user
%attr(2755,lp,sys) %_bindir/CanonUtil
%_libdir/CanonUtil
%{_datadir}/applications/mandriva-*.desktop
%_datadir/icons/*.png
%_datadir/icons/mini/*.png
%_datadir/icons/large/*.png
