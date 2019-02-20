%define vendor_name Broadcom
%define vendor_label broadcom
%define driver_name bnxt-en


Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 1.9.2
Release: 1
License: GPL
# Source extracted from https://downloads.dell.com/FOLDER05223333M/1/Bcom_LAN_214.0.166.0_NXE_Linux_Source_214.0.166.0.tar.gz
# which was found in https://www.dell.com/support/home/us/en/19/drivers/driversdetails?driverId=727T5&osCode=SLE15&productCode=poweredge-r6415
# (not very straightforward... Same search for RHEL gives an older result...)
Source: netxtreme-bnxt_en-1.9.2-214.0.150.0.tar.gz

BuildRequires: gcc
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
%autosetup -p1 -n netxtreme-bnxt_en-1.9.2-214.0.150.0

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
* Fri Feb 15 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.9.2-1
- New version 1.9.2

* Fri Nov 16 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.8.54-1
- New version 1.8.54
