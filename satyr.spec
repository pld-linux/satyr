Summary:	Tools to create anonymous, machine-friendly problem reports
Summary(pl.UTF-8):	Analizator śladów wywołań tworzonych przez GDB
Name:		satyr
Version:	0.5
Release:	1
License:	GPL v2+
Group:		Development/Tools
Source0:	https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.xz
# Source0-md5:	5d14eecc4b927c56a4368d3f5f6cfff4
Patch0:		%{name}-libopcodes.patch
Patch1:		%{name}-rpm5.patch
Patch2:		%{name}-rpm45.patch
Patch3:		%{name}-format.patch
URL:		http://fedorahosted.org/abrt/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	binutils-devel
BuildRequires:	elfutils-devel
BuildRequires:	libtool
BuildRequires:	libunwind-devel >= 1.1
BuildRequires:	pkgconfig
BuildRequires:	rpm-devel
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Satyr is a library that can be used to create and process
microreports. Microreports consist of structured data suitable to be
analyzed in a fully automated manner, though they do not necessarily
contain sufficient information to fix the underlying problem. The
reports are designed not to contain any potentially sensitive data to
eliminate the need for review before submission. Included is a tool
that can create microreports and perform some basic operations on
them.

%description -l pl.UTF-8
Satyr to biblioteka do tworzenia i przetwarzania mikroraportów.
Mikroraporty składają się ze strukturalnych danych nadających się do
analizy w sposób całkowicie automatyczny, ale niekoniecznie
zawierających pełne informacje do naprawienia problemu. Raporty są
zaprojektowane tak, żeby nie zawierały żadnych potencjalnie wrażliwych
danych, aby nie było potrzeby przeglądania ich przed wysłaniem. Do
pakietu jest dołączone narzędzie potrafiące tworzyć mikroraporty i
wykonywać na nich podstawowe operacje.

%package libs
Summary:	Satyr library - automatic problem management with anonymous reports
Summary(pl.UTF-8):	Biblioteka Satyr do automatycznego zarządzania problemami z anonimowymi zgłoszeniami
Group:		Libraries

%description libs
Satyr library - automatic problem management with anonymous reports.

%description libs -l pl.UTF-8
Biblioteka Satyr do automatycznego zarządzania problemami z
anonimowymi złoszeniami.

%package devel
Summary:	Header files for Satyr library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Satyr
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Satyr library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Satyr.

%package -n python-satyr
Summary:	Python bindings for Satyr library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki Satyr
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-modules

%description -n python-satyr
Python bindings for Satyr library.

%description -n python-satyr -l pl.UTF-8
Wiązania Pythona do biblioteki Satyr.

%prep
%setup -q
%patch0 -p1
%if "%{_rpmversion}" >= "5.0"
%patch1 -p1
%else
%patch2 -p1
%endif
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{py_sitedir}/satyr/*.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/satyr
%{_mandir}/man1/satyr.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsatyr.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsatyr.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsatyr.so
%{_includedir}/satyr
%{_pkgconfigdir}/satyr.pc

%files -n python-satyr
%defattr(644,root,root,755)
%dir %{py_sitedir}/satyr
%{py_sitedir}/satyr/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/satyr/_satyr.so
