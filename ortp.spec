Name:           ortp
Version:        0.20.0
Release:        10%{?dist}
Summary:        A C library implementing the RTP protocol (RFC3550)
Epoch:          1

Group:          System Environment/Libraries
License:        LGPLv2+ and VSL
URL:            http://www.linphone.org/eng/documentation/dev/ortp.html
Source:         http://download.savannah.gnu.org/releases/linphone/ortp/sources/%{name}-%{version}.tar.gz

Patch0:         ortp-0.20.0-bz#1005212-bounds-checking.patch
Patch1:         ortp-0.20.0-bz#1005255-unsafe-shared-memory.patch
Patch2:         ortp-0.20.0-bz#1005216-hardcoded-username.patch
Patch3:         ortp-0.20.0-bz#1005218-length-check.patch
Patch4:         ortp-0.20.0-bz#1005219-sign-overflow-checks.patch
Patch5:         ortp-0.20.0-bz#1005261-domain-socket.patch

BuildRequires:  doxygen
BuildRequires:  graphviz

BuildRequires:  libtool perl-Carp
BuildRequires:  libsrtp-devel
BuildRequires:  openssl-devel
%if 0%{?fedora} > 16
BuildRequires:  libzrtpcpp-devel >= 2.1.0
%endif

%description
oRTP is a C library that implements RTP (RFC3550).

%package        devel
Summary:        Development libraries for ortp
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       libsrtp-devel
%if 0%{?fedora} > 16
Requires:       libzrtpcpp-devel
%endif

%description    devel
Libraries and headers required to develop software with ortp.

%prep
%setup0 -q
autoreconf -i -f

%patch0 -p1 -b .bounds-checking
%patch1 -p1 -b .unsafe-shared-memory
%patch2 -p1 -b .hardcoded-username
%patch3 -p1 -b .length-check
%patch4 -p1 -b .sign-overflow-checks
%patch5 -p1 -b .domain-socket

%build
%configure --disable-static \
%if 0%{?fedora} > 16
           --enable-zrtp=yes \
%endif
           --enable-ipv6 \
           --enable-ssl-hmac


make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;
rm doc/html/html.tar
rm -r %{buildroot}%{_datadir}/doc/ortp

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog TODO
%{_libdir}/libortp.so.8*

%files devel
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/libortp.so
%{_libdir}/pkgconfig/ortp.pc

%changelog
* Mon Feb 10 2014 Jan Grulich <jgrulich@redhat.com> - 1:0.20.0-10
- Add check for user UID when connecting to pipe (#1005261)
- Add length check in stunEncodeMessage (#1005218)
- Add sign and overflow checks (#1005219)
- Remove hardcoded username and password (#1005216)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:0.20.0-9
- Mass rebuild 2014-01-24

* Wed Jan 22 2014 Jan Grulich <jgrulich@redhat.com> - 1:0.20.0-8
- Set better permissions for shared memory (#1005255)
- Sanity checks (#1005212)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:0.20.0-7
- Mass rebuild 2013-12-27

* Wed Aug 14 2013 Jan Grulich <jgrulich@redhat.com> - 1:0.20.0-6
- Fix multilib regression from RPMdiff (#884133)

* Sat Mar 23 2013 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-5
- autoreconf in %%prep (#926292)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-2
- ortp-0.20.0
- BR: libzrtpcpp-devel for F17+

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.18.0-1
- ortp-0.18.0
- drop patches for issues fixed in upstream (retval and unused vars)

* Tue Sep 27 2011 Dan Horák <dan[at]danny.cz> - 1:0.16.5-2
- fix another gcc warning and move all fixes to one patch

* Fri Sep  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.16.5-1
- ortp-0.16.5
- add BR: libsrtp-devel openssl-devel

* Tue Mar 15 2011 Karsten Hopp <karsten@redhat.com> 0.16.1-3.1
- fix build error (unused variable)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep  2 2010 Dan Horák <dan[at]danny.cz> - 1:0.16.1-2
- fix "ignoring return value" warning

* Mon Nov 30 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1:0.16.1-1
- Updated to 0.16.1, removed old patch
- removed autotool calls, and using install -p

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.5.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.4.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.14.2-0.3.20080211
- fix license tag
- epoch bump to fix pre-release versioning

* Thu Feb 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.2-0.20080211.2%{?dist}
- Update to 0.14.2 snapshot

* Tue Feb  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.2
- Apply patch to remove -Werror from the build (for PPC).

* Fri Feb  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.1
- Update to 0.14.1 (using CVS snapshot until official release is available).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.13.1-4
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-2
- Fix URL

* Mon Apr 23 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-1
- Update to 0.13.1
- BR doxygen and graphviz for building documentation

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.0-1
- Update to 0.13.0
- ortp-devel BR pkgconfig
- Add ldconfig scriptlets

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.12.0-1
- Update to 0.12.0

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-2
- Bring back -Werror patch (needed for building on PPC)

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-1
- Update to 0.11.0
- Remove ortp-0.8.1-Werror.patch

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-3
- Bump release and rebuild

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-2
- Rebuild for Fedora Extras 5

* Tue Jan  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-1
- Upstream update

* Thu Dec 22 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-2
- Added ortp.pc to -devel

* Sat Dec  3 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-1
- Upstream update

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-6
- Fix a typo in Requires on -devel

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-5
- Add missing Requires on -devel

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-4
- Split from linphone
