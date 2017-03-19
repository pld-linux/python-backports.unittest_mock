#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Make mock available as unittest.mock regardless of Python version
Summary(pl.UTF-8):	Udostępnienie modułu mock jako unittest.mock niezależnie od wersji Pythona
Name:		python-backports.unittest_mock
Version:	1.2.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/backports.unittest_mock
Source0:	https://files.pythonhosted.org/packages/source/b/backports.unittest_mock/backports.unittest_mock-%{version}.tar.gz
# Source0-md5:	f7f129ad8734c5837f66fdd880938ec4
URL:		https://pypi.python.org/pypi/backports.unittest_mock
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 2.8
%endif
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.15.0
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
%if "%{py3_ver}" < "3.3"
BuildRequires:	python3-mock
%endif
BuildRequires:	python3-pytest >= 2.8
%endif
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.15.0
BuildRequires:	sed >= 4.0
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
BuildRequires:	python3-rst.linker
%endif
Requires:	python-backports
Requires:	python-mock
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides a function "install()" which makes the "mock"
module available as "unittest.mock" on Python 3.2 and earlier.

Also advertises a pytest plugin which configures unittest.mock
automatically.

%description -l pl.UTF-8
Ten moduł udostępnia funkcję "install()", czyniącą moduł "mock"
dostępny jako "unittest.mock" w Pythonie 3.2 i wcześniejszym.

Udostępnia także wtyczkę pytest automatycznie konfigurującą
unittest.mock.

%package -n python3-backports.unittest_mock
Summary:	Make mock available as unittest.mock regardless of Python version
Summary(pl.UTF-8):	Udostępnienie modułu mock jako unittest.mock niezależnie od wersji Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-backports.unittest_mock
This module provides a function "install()" which makes the "mock"
module available as "unittest.mock" on Python 3.2 and earlier.

Also advertises a pytest plugin which configures unittest.mock
automatically.

%description -n python3-backports.unittest_mock -l pl.UTF-8
Ten moduł udostępnia funkcję "install()", czyniącą moduł "mock"
dostępny jako "unittest.mock" w Pythonie 3.2 i wcześniejszym.

Udostępnia także wtyczkę pytest automatycznie konfigurującą
unittest.mock.

%package apidocs
Summary:	API documentation for backports.unittest_mock
Summary(pl.UTF-8):	Dokumentacja API modułu backports.unittest_mock
Group:		Documentation

%description apidocs
API documentation for backports.unittest_mock.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu backports.unittest_mock.

%prep
%setup -q -n backports.unittest_mock-%{version}

%build
%if %{with python2}
%py_build

%{?with_tests:%{__python} -m pytest tests}
%endif

%if %{with python3}
%py3_build

%{?with_tests:%{__python3} -m pytest tests}
%endif

%if %{with doc}
TOPDIR=$(pwd)
cd docs
PYTHONPATH=$TOPDIR \
sphinx-build -b html . html
%{__rm} -r html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install

%if "%{py3_ver}" >= "3.3"
# pythonegg dependency generator resolves dependencies using python version running
# the generator; avoid unwanted python3egg(mock) dependency
%{__sed} -i '/^\[:python_version=="2\.7"/,/^mock$/ d' $RPM_BUILD_ROOT%{py3_sitescriptdir}/backports.unittest_mock-%{version}-py*.egg-info/requires.txt
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py_sitescriptdir}/backports/unittest_mock
%{py_sitescriptdir}/backports.unittest_mock-%{version}-py*-nspkg.pth
%{py_sitescriptdir}/backports.unittest_mock-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-backports.unittest_mock
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py3_sitescriptdir}/backports
%{py3_sitescriptdir}/backports/unittest_mock
%{py3_sitescriptdir}/backports.unittest_mock-%{version}-py*-nspkg.pth
%{py3_sitescriptdir}/backports.unittest_mock-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*
%endif
