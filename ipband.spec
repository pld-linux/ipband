Summary:	IP bandwidth watchdog
Summary(pl):	Monitor ruchu IP
Name:		ipband
Version:	0.7
Release:	2
License:	GPL
Group:		Networking/Utilities
Group(cs):	S��ov�/Utility
Group(da):	Netv�rks/V�rkt�j
Group(de):	Netzwerkwesen/Dienstprogramme
Group(es):	Red/Utilitarios
Group(fr):	R�seau/Utilitaires
Group(is):	Net/T�l
Group(it):	Rete/Utility
Group(no):	Nettverks/Verkt�y
Group(pl):	Sieciowe/Narz�dzia
Group(pt_BR):	Rede/Utilit�rios
Group(pt):	Rede/Utilidades
Group(ru):	�������/����������
Group(sl):	Omre�ni/Pripomo�ki
Group(sv):	N�tverk/Verktyg
Source0:	http://ipband.sourceforge.net/%{name}-%{version}.tgz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-PLD_rc.patch
Patch2:		%{name}-paths.patch
URL:		http://ipband.sf.net/
BuildRequires:	libpcap-devel
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
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

%description -l pl
ipband jest bazuj�cym na pcap monitorem ruchu IP. S�ucha na
interfejsie sieciowym w trybie promiscuous, liczy ruch przypadaj�cy
na podsieci oraz wykorzystanie pasma i zaczyna szczeg�owe logowanie
je�eli podany pr�g dla danej podsieci zostanie przekroczony.

To narz�dzie mo�e by� pomocne w �rodowisku WAN (frame relay, ISDN)
z ograniczonym pasmem do wykrywania �r�d�a nadmiernego ruchu, kiedy
niekt�re ��cza staj� si� wysycone do takiego stopnia, �e gubione s�
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

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/log
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
%{_mandir}/man1/ipband.1*
%attr(755,root,root) %{_bindir}/ipband
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipband.conf
%attr(754,root,root) /etc/rc.d/init.d/ipband
%attr(640,root,root) %ghost /var/log/ipband.log
