# NOTE:
# - a2p is provided by standard Perl distribution (perl-tools)
#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define		pdir	App
%define		pnam	a2p
%include	/usr/lib/rpm/macros.perl
Summary:	Awk to Perl translator
Name:		perl-App-a2p
Version:	1.007
Release:	0.1
License:	GPL+ or Artistic
Group:		Development/Tools
Source0:	http://www.cpan.org/authors/id/L/LE/LEONT/App-a2p-%{version}.tar.gz
# Source0-md5:	7626c175024931f2153e16f2a5edf858
Patch0:		App-a2p-1.007-Remove-alarm-call-from-test.patch
Patch1:		App-a2p-1.007-a2p-y.patch
URL:		http://search.cpan.org/dist/App-a2p/
BuildRequires:	byacc
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
%if %{with tests}
BuildRequires:	perl(Test::More) >= 0.89
BuildRequires:	perl-Devel-FindPerl
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package delivers a2p tool which takes an awk script specified on
the command line and produces a comparable Perl script.

%prep
%setup -q -n App-a2p-%{version}
%patch0 -p1
%patch1 -p1

%build
# Regenerate a2p.c from a2p.y
byacc a2p.y
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"
%{__make}
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README LICENSE
%attr(755,root,root) %{_bindir}/a2p
%{_mandir}/man1/a2p.1*
%{perl_vendorlib}/App/a2p.pm
