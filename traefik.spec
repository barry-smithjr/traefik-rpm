%define debug_package %{nil}

Name:           traefik
Version:        1.5.4
Release:        1%{?dist}
Summary:        Træfɪk, a modern reverse proxy
ExclusiveArch:  x86_64

Group:          System Environment/Daemons
License:        MIT
URL:            https://traefik.io/
Source0:        https://github.com/containous/traefik/releases/download/v%{version}/traefik_linux-amd64
Source1:        traefik.service
Source2:        traefik.sysconfig
Source3:        https://raw.githubusercontent.com/containous/traefik/master/traefik.sample.toml
Source4:        LICENSE

BuildRequires:  systemd-units

Requires(pre):  shadow-utils
Requires:       systemd glibc

%description
Træfɪk is a modern HTTP reverse proxy and load balancer made to deploy
microservices with ease. It supports several backends (Docker, Swarm,
Mesos/Marathon, Consul, Etcd, Zookeeper, BoltDB, Rest API, file...) to manage
its configuration automatically and dynamically.

%prep

%build

%install
install -D %{SOURCE0} %{buildroot}/%{_bindir}/traefik
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -D %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}/traefik.toml
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
* Wed Apr 25 2018 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.5.4-1
- update to v1.5.4
- ensure user and group are deleted only for uninstallations

* Mon Sep 26 2016 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.0.2-2
- fix service syntax for configfile flag in systemd unit

* Tue Sep 20 2016 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.0.2-1
- initial version: v1.0.2
