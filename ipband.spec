Summary:	IP bandwidth watchdog
Summary(pl):	Monitor ruchu IP
Name:		ipband
Version:	0.7.2
Release:	3
License:	GPL
Group:		Networking/Utilities
Source0:	http://ipband.sourceforge.net/%{name}-%{version}.tgz
# Source0-md5:	964d7e1e5392d0ede548f7173c0deb85
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-PLD_rc.patch
Patch2:		%{name}-paths.patch
URL:		http://ipband.sf.net/
BuildRequires:	libpcap-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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

%description -l pl
ipband jest bazuj±cym na pcap monitorem ruchu IP. S³ucha na
interfejsie sieciowym w trybie promiscuous, liczy ruch przypadaj±cy na
podsieci oraz wykorzystanie pasma i zaczyna szczegó³owe logowanie
je¿eli podany próg dla danej podsieci zostanie przekroczony.

To narzêdzie mo¿e byæ pomocne w ¶rodowisku WAN (frame relay, ISDN) z
ograniczonym pasmem do wykrywania ¼ród³a nadmiernego ruchu, kiedy
niektóre ³±cza staj± siê wysycone do takiego stopnia, ¿e gubione s±
poprawne pakiety.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make}

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
if [ -f /var/lock/subsys/ipband ]; then
	/etc/rc.d/init.d/ipband restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ipband start\" to start ipband daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ipband ]; then
		/etc/rc.d/init.d/ipband stop 1>&2
	fi
	/sbin/chkconfig --del ipband
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ipband
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipband.conf
%attr(754,root,root) /etc/rc.d/init.d/ipband
%attr(640,root,root) %ghost /var/log/ipband.log
%{_mandir}/man1/ipband.1*
