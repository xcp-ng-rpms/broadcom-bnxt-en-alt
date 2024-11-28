%define vendor_name Broadcom
%define vendor_label broadcom
%define driver_name bnxt-en
%define module_dir override

# Upstream versioning of these drivers is... peculiar.
# There are at least 3 different versions for a given driver distribution from Dell.
# The sources archive contains two versions: e.g. netxtreme-bnxt_en-1.10.0-214.0.253.1.tar.gz
# We use the first one as the RPM Version (like Citrix does) and append the second one to the Release.
# Note : we found that the first version (e.g. 1.10.0) does not uniquely identify a driver release,
# so the second part is also necessary (although Citrix does not retain it in its RPM versioning).
#
# In the download page, the 214.0.253.1 is also written 21.40.25.31, someone probably knows why...
# There's also another version displayed on top of the driver page, and this is the version that
# the corresponding firmware usually says it requires.
# Example: 21.4.2. Maybe it comes from [21].[4]0.[2]5.31?
# If someone has sensible explanations to what appears like a mess to me, contact me!
# (e-mail address for Samuel Verschelde available in the changelog)

%define _version 1.10.3
%define other_version 231.0.162.0

# Just for documenting
# version_whatever = --- # e.g 21.4.2

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: %{_version}_%{other_version}
Release: 1%{?dist}
License: GPL

# Old comment retained as documentation:
# Source extracted from https://dl.dell.com/FOLDER05739713M/1/Bcom_LAN_214.0.253.1_NXE_Linux_Source_214.0.253.1.tar.gz
# which was found in https://www.dell.com/support/home/us/en/19/drivers/driversdetails?driverId=727T5&osCode=SLE15&productCode=poweredge-r6415
# (not very straightforward... Same search for RHEL used to give an older result...)
# (And the latest I found was older than what XS had...)

# New comment:
# Source extracted from Broadcom.com
# URL: https://www.broadcom.com/products/ethernet-connectivity/network-adapters
# Version on website: 231.1.162.1
# Source version: 231.0.162.0
# - extracted tarball bcm_231.1.162.1b.tar.gz that contains sources and various RPMs
# - extracted source tarball, here named bnxt_en-1.10.3-231.0.162.0.tar.gz
# - rename folder to driver-broadcom-bnxt-en-$VERSION
# - regenerate tarball with name broadcom-bnxt-en-$VERSION
Source: broadcom-bnxt-en-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-broadcom-bnxt-en-%{version}

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
* Thu Nov 28 2024 David Morel <david.morel@vates.tech> - 1.10.2_231.0.162.0-1
- Update to version 1.10.2_231.0.162.0
- Synced from broadcom.com

* Wed Nov 15 2023 Gael Duperrey <gduperrey@vates.tech> - 1.10.2_227.0.130.0-1
- Update to version 1.10.2_227.0.130.0
- Synced from broadcom.com

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.10.0_216.0.119.1-3
- Rebuild for XCP-ng 8.3

* Wed Aug 19 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.10.0_216.0.119.1-2
- Rebuild for XCP-ng 8.2

* Tue Mar 10 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.10.0_216.0.119.1-1
- Update to 1.10.0_216.0.119.1

* Tue Jan 28 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.10.0_216.0.119.0-1
- Update to 1.10.0_216.0.119.0

* Tue Dec 17 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.10.0-214.0.253.1.2
- remove depmod configuration, not needed anymore since XCP-ng 8.0

* Tue Nov 19 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.10.0-214.0.253.1.1
- Update to 1.10.0-214.0.253.1
- Add long comment in spec file regarding the versioning imbroglio

* Tue Mar 12 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.9.2-5
- Override module directory for depmod to make sure our alternative driver takes precedence
- Simplify module path (simply /lib/modules/{version}/override/)

* Fri Feb 15 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.9.2-1
- New version 1.9.2

* Fri Nov 16 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.8.54-1
- New version 1.8.54
