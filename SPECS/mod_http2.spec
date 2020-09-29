# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}

Name:		mod_http2
Version:	1.11.3
Release:	3%{?dist}.1
Summary:	module implementing HTTP/2 for Apache 2
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://icing.github.io/mod_h2/
Source0:	https://github.com/icing/mod_h2/releases/download/v%{version}/mod_http2-%{version}.tar.gz
BuildRequires:	pkgconfig, httpd-devel >= 2.4.20, libnghttp2-devel >= 1.7.0, openssl-devel >= 1.0.2
Requires:	httpd-mmn = %{_httpd_mmn}
Conflicts:      httpd < 2.4.25-8

# https://bugzilla.redhat.com/show_bug.cgi?id=1741860
# https://bugzilla.redhat.com/show_bug.cgi?id=1741864
# https://bugzilla.redhat.com/show_bug.cgi?id=1741868
Patch200: httpd-2.4.34-CVE-2019-9511-and-9516-and-9517.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1866560
Patch201: mod_http2-1.11.3-CVE-2020-9490.patch

%description
The mod_h2 Apache httpd module implements the HTTP2 protocol (h2+h2c) on
top of libnghttp2 for httpd 2.4 servers.

%prep
%setup -q

%patch200 -p1 -b .CVE-2019-9511-and-9516-and-9517
%patch201 -p1 -b .CVE-2020-9490

%build
%configure
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/etc/httpd/share/doc/

# create configuration
mkdir -p %{buildroot}%{_httpd_modconfdir}
echo "LoadModule http2_module modules/mod_http2.so" > %{buildroot}%{_httpd_modconfdir}/10-h2.conf
echo "LoadModule proxy_http2_module modules/mod_proxy_http2.so" > %{buildroot}%{_httpd_modconfdir}/10-proxy_h2.conf

%check
make check

%files
%doc README README.md ChangeLog AUTHORS
%license LICENSE
%config(noreplace) %{_httpd_modconfdir}/10-h2.conf
%config(noreplace) %{_httpd_modconfdir}/10-proxy_h2.conf
%{_httpd_moddir}/mod_http2.so
%{_httpd_moddir}/mod_proxy_http2.so

%changelog
* Tue Aug 18 2020 Lubos Uhliarik <luhliari@redhat.com> - 1.11.3-3.1
- Resolves: #1869072 - CVE-2020-9490 httpd:2.4/mod_http2: httpd: Push diary
  crash on specifically crafted HTTP/2 header

* Thu Aug 29 2019 Lubos Uhliarik <luhliari@redhat.com> - 1.11.3-3
- Resolves: #1744999 - CVE-2019-9511 httpd:2.4/mod_http2: HTTP/2: large amount
  of data request leads to denial of service
- Resolves: #1745086 - CVE-2019-9516 httpd:2.4/mod_http2: HTTP/2: 0-length
  headers leads to denial of service
- Resolves: #1745154 - CVE-2019-9517 httpd:2.4/mod_http2: HTTP/2: request for
  large response leads to denial of service

* Thu Apr  4 2019 Joe Orton <jorton@redhat.com> - 1.11.3-2
- update release (#1695587)

* Tue Oct 16 2018 Lubos Uhliarik <luhliari@redhat.com> - 1.11.3-1
- new version 1.11.3
- Resolves: #1633401 - CVE-2018-11763 mod_http2: httpd:  DoS for HTTP/2
  connections by continuous SETTINGS

* Wed May  2 2018 Joe Orton <jorton@redhat.com> - 1.10.20-1
- update to 1.10.20

* Wed Apr 18 2018 Joe Orton <jorton@redhat.com> - 1.10.18-1
- update to 1.10.18

* Thu Mar 29 2018 Joe Orton <jorton@redhat.com> - 1.10.16-1
- update to 1.10.16 (CVE-2018-1302)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov  7 2017 Joe Orton <jorton@redhat.com> - 1.10.13-1
- update to 1.10.13

* Fri Oct 20 2017 Joe Orton <jorton@redhat.com> - 1.10.12-1
- update to 1.10.12

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Joe Orton <jorton@redhat.com> - 1.10.10-1
- update to 1.10.10

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul  6 2017 Joe Orton <jorton@redhat.com> - 1.10.7-1
- update to 1.10.7

* Mon Jun 12 2017 Joe Orton <jorton@redhat.com> - 1.10.6-1
- update to 1.10.6

* Tue May 16 2017 Joe Orton <jorton@redhat.com> - 1.10.5-1
- update to 1.10.5

* Mon Apr 10 2017 Luboš Uhliarik <luhliari@redhat.com> - 1.10.1-1
- Initial import (#1440780).
