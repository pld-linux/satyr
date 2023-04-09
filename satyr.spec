#
# Conditional build:
%bcond_without	apidocs	# Doxygen API documentation
%bcond_with	rpm5	# build with rpm5
#
Summary:	Tools to create anonymous, machine-friendly problem reports
Summary(pl.UTF-8):	Analizator śladów wywołań tworzonych przez GDB
Name:		satyr
Version:	0.42
Release:	1
License:	GPL v2+
Group:		Development/Tools
#Source0Download: https://github.com/abrt/satyr/releases
Source0:	https://github.com/abrt/satyr/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	279394a6c93f3a086e052b6a3355900f
Patch0:		%{name}-rpm5.patch
URL:		https://github.com/abrt/satyr
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	binutils-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	json-c-devel
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	nettle-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	rpm-devel >= 4.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.507
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	btparser < 0.27
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
Requires:	json-c-devel
Obsoletes:	btparser-libs < 0.27

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
Requires:	json-c-devel
Obsoletes:	btparser-devel < 0.27

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

%package -n python3-satyr
Summary:	Python 3 bindings for Satyr library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki Satyr
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python3-modules >= 1:3.6
Obsoletes:	python-btparser < 0.27
Obsoletes:	python-satyr < 0.30

%description -n python3-satyr
Python 3 bindings for Satyr library.

%description -n python3-satyr -l pl.UTF-8
Wiązania Pythona 3 do biblioteki Satyr.

%prep
%setup -q
%{?with_rpm5:%patch0 -p1}

printf '%s' '%{version}' > satyr-version

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-doxygen-docs} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{py3_sitedir}/satyr/*.la

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/satyr
%{_mandir}/man1/satyr.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsatyr.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsatyr.so.4

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

%files -n python3-satyr
%defattr(644,root,root,755)
%dir %{py3_sitedir}/satyr
%{py3_sitedir}/satyr/__init__.py
%attr(755,root,root) %{py3_sitedir}/satyr/_satyr3.so
%{py3_sitedir}/satyr/__pycache__
