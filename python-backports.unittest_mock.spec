#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Make mock available as unittest.mock regardless of Python version
Summary(pl.UTF-8):	Udostępnienie modułu mock jako unittest.mock niezależnie od wersji Pythona
Name:		python-backports.unittest_mock
Version:	1.5
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/backports.unittest_mock
Source0:	https://files.pythonhosted.org/packages/source/b/backports.unittest_mock/backports.unittest_mock-%{version}.tar.gz
# Source0-md5:	b089b2d4ef9740ef2bb0616e2f1303bb
URL:		https://pypi.python.org/pypi/backports.unittest_mock
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-black-multipy
BuildRequires:	python-pytest-flake8
%endif
BuildRequires:	python-setuptools >= 1:31.0.1
BuildRequires:	python-setuptools_scm >= 1.15.0
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
%if "%{py3_ver}" < "3.3"
BuildRequires:	python3-mock
%endif
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black-multipy
BuildRequires:	python3-pytest-flake8
%endif
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 1.15.0
BuildRequires:	sed >= 4.0
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-jaraco.packaging >= 3.2
BuildRequires:	python3-rst.linker >= 1.9
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

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=backports.unittest_mock,pytest_black_multipy,pytest_flake8 \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=backports.unittest_mock,pytest_black_multipy,pytest_flake8 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
# packaged in python-backports
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/backports/__init__.py*
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/backports/unittest_mock
%{py_sitescriptdir}/backports.unittest_mock-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-backports.unittest_mock
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%dir %{py3_sitescriptdir}/backports
%{py3_sitescriptdir}/backports/__init__.py
%{py3_sitescriptdir}/backports/__pycache__
%{py3_sitescriptdir}/backports/unittest_mock
%{py3_sitescriptdir}/backports.unittest_mock-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
