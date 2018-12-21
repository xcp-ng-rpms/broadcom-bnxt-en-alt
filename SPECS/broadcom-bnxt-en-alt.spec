%define vendor_name Broadcom
%define vendor_label broadcom
%define driver_name bnxt-en


Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 1.8.54
Release: 1
License: GPL
# Source extracted from https://docs.broadcom.com/docs/bnxt_en-1.8.54-1.rhel7u4.src.rpm
Source: netxtreme-bnxt_en-%{version}.tar.gz

BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%define module_dir updates/xcp-ng/bnxt_en-%{version}

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n netxtreme-bnxt_en-%{version}

%build
cd bnxt_en
%{?cov_wrap} %{__make} KVER=%{kernel_version}

%install
cd bnxt_en
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
/lib/modules/%{kernel_version}/%{module_dir}/*.ko

%changelog
* Fri Nov 16 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.8.54-1
- New version 1.8.54
