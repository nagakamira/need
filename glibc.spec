Name:           glibc
Version:        2.24
Release:        1
Summary:        The GNU libc libraries.
Group:          System/Base
License:        GPLv2+ LGPLv2+
URL:            http://www.gnu.org/software/libc/
Source0:        %{name}-%{version}.tar.xz
Source1:        ld.so.conf
Source3:        nsswitch.conf

BuildRequires:       autoconf
BuildRequires:       automake
BuildRequires:       binutils
BuildRequires:       gcc
BuildRequires:       gettext
BuildRequires:       kernel-headers
BuildRequires:       libcap-devel
BuildRequires:       libstdc++-static
BuildRequires:       texinfo
Requires:       tzdata
Requires:       linux-headers
Requires:       base-files

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

%prep
%setup -q

%build
	mkdir -p build
	cd build
	../configure --prefix=/usr          \
	             --libexecdir=/usr/lib \
	             --with-headers=/usr/include \
	             --enable-kernel=4.1.0 \
	             --enable-bind-now \
        	     --enable-add-ons \
        	     --enable-static-nss \
        	     --disable-profile \
        	     --disable-werror \
        	     --without-cvs \
        	     --without-gd \
        	     --without-selinux \
        	     --enable-lock-elision \
        	     --enable-obsolete-rpc        \
        	     --enable-stackguard-randomization \
        	     --enable-multi-arch
	make

%install
	cd build
	make install_root=%{buildroot} install
	mkdir -pv %{buildroot}/etc/ld.so.conf.d
	rm -vf %{buildroot}/sbin/sln \
		%{buildroot}/usr/bin/rpcinfo
	install -d %{buildroot}/etc/ld.so.conf.d %{buildroot}/usr/lib/locale
	cp -v ../nscd/nscd.conf %{buildroot}/etc/nscd.conf
	mkdir -pv %{buildroot}/var/cache/nscd
	install -v -Dm644 ../nscd/nscd.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/nscd.conf
	install -v -Dm644 ../nscd/nscd.service %{buildroot}/lib/systemd/system/nscd.service
	install -m644 ../posix/gai.conf %{buildroot}/etc/gai.conf
	install -m 0644 %{_sourcedir}/{nsswitch.conf,ld.so.conf} %{buildroot}/etc
	rm -rf	%{buildroot}/usr/bin/tzselect
	rm -rf	%{buildroot}/usr/sbin/z{dump,ic}

%files
%defattr(-,root,root,-)
%doc

%changelog
