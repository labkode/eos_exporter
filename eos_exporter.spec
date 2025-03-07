#
# eos_exporter spec file
#
%define version _VERSION_

Name: eos_exporter
Summary: The Prometheus EOS exporter exposes EOS metrics.
Version: %{version}
Release: 1
License: AGPLv3
BuildRoot: %{_tmppath}/%{name}-buildroot
Group: CERN-IT/ST
BuildArch: x86_64
Source: %{name}-%{version}.tar.gz

BuildRequires: systemd

%description
This RPM provides a binary and a systemd unit to run the eos_exporter in the EOS instance's MGMs.

# Don't do any post-install weirdness, especially compiling .py files
%define __os_install_post %{nil}

%{?systemd_requires}
Requires: systemd

#Pre installation/upgrade of RPM section
%pre      

%prep
%setup -n %{name}-%{version}

%install
# server versioning

# installation
rm -rf %buildroot/
mkdir -p %buildroot/usr/local/bin
mkdir -p %buildroot/opt/eos_exporter/bin
mkdir -p %buildroot/etc/logrotate.d
mkdir -p %buildroot/var/log/eos_exporter
install -m 755 eos_exporter %buildroot/opt/eos_exporter/bin/eos_exporter
install -D -m 644 %{name}.unit %{buildroot}%{_unitdir}/%{name}.service

%clean
rm -rf %buildroot/

%files
%defattr(-,root,root,-)
/var/log/eos_exporter/
/opt/eos_exporter/bin/*
%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%changelog
* Mon Oct 17 2022 Roberto Valverde <rvalverd@cern.ch> 0.0.12-1
- Added eos recycle and eos who collectors. 
* Thu Jun 24 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.11-1
- Remove -a flag from eos ns stat (NS collector ~7s scrape time), excludes batch user info.
* Thu Jun 22 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.10-1
- Fix NS collector, fix unmarshalling issues.
* Thu May 10 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.9-1
- Add IO stat collector, with its metrics.
* Thu Apr 26 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.8-1
- Introduce batch overload metrics.
* Thu Mar 09 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.7-1
- Improve the release title for GitHub tagged-releases, and improve systemd unit logs.
* Thu Feb 22 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.5-1
- First version that is not a pre-release with proper systemd unit.
* Thu Feb 17 2022 Aritz Brosa Iartza <aritz.brosa.iartza@cern.ch> 0.0.4-1
- First version with RPMs building enabled.

