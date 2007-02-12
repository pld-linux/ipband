Summary:	IP bandwidth watchdog
Summary(pl.UTF-8):   Monitor ruchu IP
Name:		ipband
Version:	0.8
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://ipband.sourceforge.net/%{name}-%{version}.tgz
# Source0-md5:	a43dc863c044e7e5665d3e16d4c49770
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-PLD_rc.patch
Patch2:		%{name}-paths.patch
URL:		http://ipband.sourceforge.net/
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ipband

%description
ipband is pcap based IP traffic monitor. It listens to a network
interface in promiscuous mode, tallies per-subnet traffic and
bandwidth usage and starts detailed logging if specified threshold for
the specific subnet is exceeded.

This utility could be handy in a limited bandwidth WAN environment
(frame relay, ISDN etc. circuits) to pinpoint offending traffic source
if certain links become saturated to the point where legitimate
packets start getting dropped.

%description -l pl.UTF-8
ipband jest bazującym na pcap monitorem ruchu IP. Słucha na
interfejsie sieciowym w trybie promiscuous, liczy ruch przypadający na
podsieci oraz wykorzystanie pasma i zaczyna szczegółowe logowanie
jeżeli podany próg dla danej podsieci zostanie przekroczony.

To narzędzie może być pomocne w środowisku WAN (frame relay, ISDN) z
ograniczonym pasmem do wykrywania źródła nadmiernego ruchu, kiedy
niektóre łącza stają się wysycone do takiego stopnia, że gubione są
poprawne pakiety.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/log

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/log/ipband.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipband
%service ipband restart "ipband daemon"

%preun
if [ "$1" = "0" ]; then
	%service ipband stop
	/sbin/chkconfig --del ipband
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/ipband
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipband.conf
%attr(754,root,root) /etc/rc.d/init.d/ipband
%attr(640,root,root) %ghost /var/log/ipband.log
%{_mandir}/man1/ipband.1*
