%define debug_package %{nil}

Name:           traefik
Version:        2.5.6
Release:        2%{?dist}
Summary:        The Cloud Native Application Proxy
ExclusiveArch:  x86_64

Group:          System Environment/Daemons
License:        MIT
URL:            https://traefik.io/
Source0:        https://github.com/traefik/traefik/releases/download/v%{version}/traefik_v%{version}_linux_amd64.tar.gz
Source1:        traefik.service
Source2:        traefik.sysconfig
Source3:        https://github.com/traefik/traefik/raw/v%{version}/traefik.sample.toml
Source4:        LICENSE

BuildRequires:  systemd-units

Requires(pre):  shadow-utils
Requires:       systemd glibc

%description
Traefik (pronounced traffic) is a modern HTTP reverse proxy and load balancer
that makes deploying microservices easy. Traefik integrates with your existing 
infrastructure components (Docker, Swarm mode, Kubernetes, Marathon, Consul, 
Etcd, Rancher, Amazon ECS, ...) and configures itself automatically and dynamically. 
Pointing Traefik at your orchestrator should be the only configuration step you need.

%prep

%setup -c

%build

%install
install -D %{name} %{buildroot}/%{_bindir}/%{name}
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -D %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}/%{name}.toml
install -D %{SOURCE4} %{buildroot}/%{_docdir}/%{name}/LICENSE

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} user" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
case "$1" in
  0)
    # This is an uninstallation.
    getent passwd %{name} >/dev/null && userdel %{name}
    getent group %{name} >/dev/null && groupdel %{name}
  ;;
  1)
    # This is an upgrade.
  ;;
esac
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/traefik
%dir %attr(750, root, %{name}) %{_sysconfdir}/%{name}
%attr(644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/traefik.toml

%doc %{_docdir}/%{name}/LICENSE

%changelog
* Fri Dec 24 2021 Diftraku <diftraku@gmail.com> - 2.5.6-2
- Add AmbientCapabilities to systemd unit

* Fri Dec 24 2021 Diftraku <diftraku@gmail.com> - 2.5.6-1
- update to v2.5.6

* Sun Apr 28 2021 Diftraku <diftraku@gmail.com> - 2.4.8-1
- update to v2.4.8

* Sat Feb 27 2021 Diftraku <diftraku@gmail.com> - 2.4.5-1
- update to v2.4.5
- use tarballed distribution

* Wed Apr 25 2018 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.5.4-1
- update to v1.5.4
- ensure user and group are deleted only for uninstallations

* Mon Sep 26 2016 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.0.2-2
- fix service syntax for configfile flag in systemd unit

* Tue Sep 20 2016 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.0.2-1
- initial version: v1.0.2
