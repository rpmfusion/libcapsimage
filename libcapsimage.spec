# Disable debug package. Useless as this is closed source.
%define         debug_package %{nil}

Name:           libcapsimage
Version:        2.0.0
Release:        9%{?dist}
Summary:        Provides IPF support, primarily for UAE/E-UAE
Group:          System Environment/Libraries
License:        SPSFLA
URL:            http://www.softpres.org/?id=download
# Download URLs cannot be placed here but are available from:
# http://www.softpres.org/?id=download
Source0:        ipfdevlib_linux.tgz
Source1:        ipflib_linux-i686.tgz
Source2:        ipflib_linux-amd64.tgz
Source3:        ipflib_linux-ppc.tgz
#BuildRequires:  libstdc++-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  i686 x86_64 ppc

%description
Provides support for reading IPF files, an Amiga disk image format developed by
the Amiga Preservation Society, as part of the C.A.P.S. project.


%package devel
Summary:        Development files for libcapsimage
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for libcapsimage


%prep

%ifarch %{ix86}
%setup -qn ipfdevlib_linux -a1
%endif

%ifarch x86_64
%setup -qn ipfdevlib_linux -a2
%endif

%ifarch ppc
%setup -qn ipfdevlib_linux -a3
%endif

# Convert from DOS to UNIX Text
sed -i 's/\r//' LICENSE


%build
%ifarch %{ix86}
pushd ipflib_linux-i686
ln -sv libcapsimage.so.2.0 libcapsimage.so
popd
pushd examples
gcc %{optflags} -I ../include ipfinfo.c -o ipfinfo -L../ipflib_linux-i686/ -lcapsimage -s
popd
%endif


%ifarch x86_64
pushd ipflib_linux-amd64
ln -sv libcapsimage.so.2.3 libcapsimage.so
popd
pushd examples
gcc %{optflags} -I ../include ipfinfo.c -o ipfinfo -L../ipflib_linux-amd64/ -lcapsimage -lstdc++ -s
popd
%endif


%ifarch ppc
pushd ipflib_linux-ppc
ln -sv libcapsimage.so.2.0 libcapsimage.so
popd
pushd examples
gcc %{optflags} -I ../include ipfinfo.c -o ipfinfo -L../ipflib_linux-ppc/ -lcapsimage -s
popd
%endif
sleep 3m


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_bindir} \
         %{buildroot}%{_includedir}/caps
install -pm0644 include/caps/capsimage.h %{buildroot}%{_includedir}/caps

%ifarch %{ix86}
install -pm0755 ipflib_linux-i686/libcapsimage.so.2.0 %{buildroot}%{_libdir}
install -pm0755 examples/ipfinfo %{buildroot}%{_bindir}
pushd %{buildroot}%{_libdir}
ln -s libcapsimage.so.2.0 libcapsimage.so.2
ln -s libcapsimage.so.2.0 libcapsimage.so
popd
%endif

%ifarch x86_64
install -pm0755 ipflib_linux-amd64/libcapsimage.so.2.3 %{buildroot}%{_libdir}
install -pm0755 examples/ipfinfo %{buildroot}%{_bindir}
pushd %{buildroot}%{_libdir}
ln -s libcapsimage.so.2.3 libcapsimage.so.2
ln -s libcapsimage.so.2.3 libcapsimage.so
popd
%endif

%ifarch ppc
install -pm0755 ipflib_linux-ppc/libcapsimage.so.2.0 %{buildroot}%{_libdir}
install -pm0755 examples/ipfinfo %{buildroot}%{_bindir}
pushd %{buildroot}%{_libdir}
ln -s libcapsimage.so.2.0 libcapsimage.so.2
ln -s libcapsimage.so.2.0 libcapsimage.so
popd
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libcapsimage.so.*
%{_bindir}/ipfinfo
%doc HISTORY LICENSE README


%files devel
%defattr(-,root,root,-)
%{_includedir}/caps
%{_libdir}/libcapsimage.so


%changelog
* Thu Oct 23 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.0-9
- add a small delay during build to circumvent a race on the RPM Fusion buildsys

* Mon Oct 20 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.0-8
- make package "ExclusiveArch: i686 x86_64 ppc" and remove the
  "BuildArch: i686"; maybe plague then does what it's supposed
  to do

* Thu Sep 04 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.0.0-7
- Rebuild for rpmfusion inclusion.

* Thu Mar 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 2.0.0-6
- Compile ipfinfo, don't use precompiled version (its broken)

* Wed Mar 05 2008 Ian Chapman <packages[AT]amiga-hardware.com> 2.0.0-5
- Added support for x86_64
- Various clean ups to the spec

* Fri Jun 02 2006 Ian Chapman <packages[AT]amiga-hardware.com> 2.0.0-4
- Removed duplicate documentation from devel package
- Improved architecture checking
- Replaced %%{__sed} with sed

* Sat May 06 2006 Ian Chapman <packages[AT]amiga-hardware.com> 2.0.0-3.iss
- Altered spec file to better follow Fedora packaging guidelines
- LICENSE now converted from DOS text to UNIX
- Added library symlinks instead of only relying on ldconfig

* Mon Oct 25 2005 Ian Chapman <packages[AT]amiga-hardware.com> 2.0.0-2.iss
- Fixes for deprecated fields no longer supported by the latest rpmbuild
- Added support for building on PPC
- Now includes ipfinfo in RPM and installs to bindir

* Wed Dec 01 2004 Ian Chapman <packages[AT]amiga-hardware.com> 2.0.0-1.iss
- Initial Release
