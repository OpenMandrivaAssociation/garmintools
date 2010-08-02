%define major 4
%define libname %mklibname garmintools %{major}
%define develname %mklibname garmintools -d

Summary:	Communication tools for Garmin devices
Name:		garmintools
Version:	0.10
Release:	%mkrel 1
License:        GPLv2+
Group:		File tools
URL:		http://code.google.com/p/garmintools/
Source0:	http://garmintools.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:	51-garmin.rules
Source2:	garmintools.conf
Patch0:		garmintools-0.10-linkage_fix.diff
BuildRequires:	libusb-devel
BuildRequires:	libgarmin-devel
Requires:	udev
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
This software provides Linux users with the ability to communicate with the
Garmin Forerunner 305 via the USB interface. All of the documented Garmin
protocols as of Rev C (May 19, 2006) for the USB physical link implemented.
This means that if you have a Garmin with a USB connection to a PC, you ought
to be able to use this software to communicate with it.

%package -n	%{libname}
Summary:	Shared library for garmintools
Group:		System/Libraries

%description -n	%{libname}
This software provides Linux users with the ability to communicate with the
Garmin Forerunner 305 via the USB interface. All of the documented Garmin
protocols as of Rev C (May 19, 2006) for the USB physical link implemented.
This means that if you have a Garmin with a USB connection to a PC, you ought
to be able to use this software to communicate with it.

%package -n	%{develname}
Summary:	Development and documentation files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
Development libraries, header files and documentation for %{name}.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

%build
mkdir -p python
touch python/Makefile.in
autoreconf -fi

%configure2_5x \
    --enable-static=no

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
rm -rf %{buildroot}

%makeinstall_std INSTALL="install -p"

install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -d %{buildroot}%{_sysconfdir}/modprobe.d
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/51-garmin.rules
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/modprobe.d/garmintools.conf

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -n %{libname}
/sbin/ldconfig
# remove garmin_gps module if loaded, see README
rmmod garmin_gps &>/dev/null || true

%postun -n %{libname}
/sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man*/*.1*

%files -n %{libname}
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README
%{_libdir}/*.so.%{major}*
%{_libdir}/lib*.so.*
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%config(noreplace) %{_sysconfdir}/modprobe.d/*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so

