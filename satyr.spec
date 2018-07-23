#
# Conditional build:
%bcond_without	apidocs	# Doxygen API documentation
%bcond_without	python3	# CPython 3.x binding
#
Summary:	Tools to create anonymous, machine-friendly problem reports
Summary(pl.UTF-8):	Analizator śladów wywołań tworzonych przez GDB
Name:		satyr
Version:	0.26
Release:	4
License:	GPL v2+
Group:		Development/Tools
#Source0Download: https://github.com/abrt/satyr/releases
Source0:	https://github.com/abrt/satyr/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8f1f99315b0bac193712f8ee3bc3a832
Patch0:		%{name}-rpm5.patch
Patch1:		%{name}-rpm45.patch
URL:		https://github.com/abrt/satyr
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	binutils-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	elfutils-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.6
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-devel >= 4.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	btparser
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# satyr-python(3) man page exists in both python packages
%define		_duplicate_files_terminate_build	0

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
Obsoletes:	btparser-libs

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
Obsoletes:	btparser-devel

%description devel
Header files for Satyr library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Satyr.

%package apidocs
Summary:	API documentation for Satyr library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Satyr
Group:		Documentation

%description apidocs
API documentation for Satyr library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Satyr.

%package -n python-satyr
Summary:	Python 2 bindings for Satyr library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki Satyr
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-modules
Obsoletes:	python-btparser

%description -n python-satyr
Python 2 bindings for Satyr library.

%description -n python-satyr -l pl.UTF-8
Wiązania Pythona 2 do biblioteki Satyr.

%package -n python3-satyr
Summary:	Python 3 bindings for Satyr library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki Satyr
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python3-modules

%description -n python3-satyr
Python 3 bindings for Satyr library.

%description -n python3-satyr -l pl.UTF-8
Wiązania Pythona 3 do biblioteki Satyr.

%prep
%setup -q
%if "%{_rpmversion}" >= "5.0"
%patch0 -p1
%else
%patch1 -p1
%endif

printf '%s' '%{version}' > satyr-version

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-doxygen-docs} \
	--disable-silent-rules \
	%{!?with_python3:--without-python3}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{py_sitedir}/satyr/*.la


%py_postclean

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/satyr/*.la
%endif

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
%attr(755,root,root) %ghost %{_libdir}/libsatyr.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsatyr.so
%{_includedir}/satyr
%{_pkgconfigdir}/satyr.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidoc/html/{search,*.css,*.html,*.js,*.png}
%endif

%files -n python-satyr
%defattr(644,root,root,755)
%dir %{py_sitedir}/satyr
%{py_sitedir}/satyr/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/satyr/_satyr.so
%{_mandir}/man3/satyr-python.3*

%if %{with python3}
%files -n python3-satyr
%defattr(644,root,root,755)
%dir %{py3_sitedir}/satyr
%{py3_sitedir}/satyr/__init__.py
%attr(755,root,root) %{py3_sitedir}/satyr/_satyr3.so
%{py3_sitedir}/satyr/__pycache__
%{_mandir}/man3/satyr-python.3*
%endif
