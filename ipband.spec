Summary:	IP bandwidth watchdog.
Name:		ipband
Version:	0.7
Release:	1
License:	GPL
Group:		Networking/Utilities
Group(cs):	Sí»ové/Utility
Group(da):	Netværks/Værktøj
Group(de):	Netzwerkwesen/Dienstprogramme
Group(es):	Red/Utilitarios
Group(fr):	Réseau/Utilitaires
Group(is):	Verkfræði/Tól
Group(it):	Rete/Utility
Group(no):	Nettverks/Verktøy
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Group(pt):	Rede/Utilidades
Group(ru):	óÅÔÅ×ÙÅ/ðÒÉÌÏÖÅÎÉÑ
Group(sl):	Omre¾ni/Pripomoèki
Group(sv):	Nätverk/Verktyg
Source0:	http://ipband.sourceforge.net/%{name}-%{version}.tgz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-PLD_rc.patch
Requires:	libpcap
BuildRequires:	libpcap-devel
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
URL:		http://ipband.sf.net
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/ipband

%description
ipband is pcap based IP traffic monitor. It listens to a network
interface in promiscuous mode, tallies per-subnet traffic and
bandwidth usage and starts detailed logging if specified threshold for
the specific subnet is exceeded.

This utility could be handy in a limited bandwidth WAN environment
(frame relay, ISDN etc. circuits) to pinpoint offending traffic source
if certain links become saturated to the point where legitimate
packets start getting dropped.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
%{_mandir}/man1/ipband.1*
%attr(755,root,root) %{_bindir}/ipband
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipband.conf
%attr(754,root,root) /etc/rc.d/init.d/ipband

%clean
rm -rf $RPM_BUILD_ROOT
