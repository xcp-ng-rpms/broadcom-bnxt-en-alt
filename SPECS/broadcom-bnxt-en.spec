%define vendor_name Broadcom
%define vendor_label broadcom
%define driver_name bnxt-en

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 1.10.0
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-broadcom-bnxt-en/archive?at=1.10.0&format=tgz&prefix=driver-broadcom-bnxt-en-1.10.0#/broadcom-bnxt-en-1.10.0.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-broadcom-bnxt-en/archive?at=1.10.0&format=tgz&prefix=driver-broadcom-bnxt-en-1.10.0#/broadcom-bnxt-en-1.10.0.tar.gz) = de256024042fab2737cd4d687689266e76d7329c


BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{__make} KVER=%{kernel_version}

%install
%{?cov_wrap} %{__make} PREFIX=%{buildroot} KVER=%{kernel_version} BCMMODDIR=/lib/modules/%{kernel_version}/%{module_dir} DEPMOD=/bin/true install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Tue Jan 22 2019 Deli Zhang <deli.zhang@citrix.com> - 1.10.0-1
- CP-30070: Upgrade broadcom-bnxt-en driver to version 1.10.0
