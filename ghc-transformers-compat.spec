#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	transformers-compat
Summary:	A small compatibility shim for the transformers library
Summary(pl.UTF-8):	Mała nakładka zgodności dla biblioteki transformers
Name:		ghc-%{pkgname}
Version:	0.6.5
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/package/transformers-compat-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4da06165ca543de01f5419c47f53442a
URL:		http://hackage.haskell.org/package/transformers-compat
# ghc < 8 requires also ghc-fail 4.9.x
BuildRequires:	ghc >= 8.0
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-generic-deriving >= 1.10
BuildRequires:	ghc-generic-deriving < 2
BuildRequires:	ghc-ghc-prim
BuildRequires:	ghc-mtl >= 2.0
BuildRequires:	ghc-mtl < 2.2
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-transformers < 0.6
%if %{with prof}
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-generic-deriving-prof >= 1.10
BuildRequires:	ghc-ghc-prim-prof
BuildRequires:	ghc-mtl-prof >= 2.0
BuildRequires:	ghc-transformers-prof >= 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-generic-deriving >= 1.10
Requires:	ghc-ghc-prim
Requires:	ghc-mtl >= 2.0
Requires:	ghc-transformers >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package includes backported versions of types that were added to
transformers in transformers 0.3, 0.4, and 0.5 for users who need
strict transformers 0.2 or 0.3 compatibility to run on old versions of
the platform, but also need those types.

%description -l pl.UTF-8
Ten pakiet zawiera zbackportowane wersje biblioteki types, które
zostały dodane do biblioteki transformers w wersji 0.3, 0.4 oraz 0.5
dla użytkowników, którzy potrzebują ścisłej zgodności z transformers
0.2 lub 0.3, aby działały na starszej wersji platformy, ale potrzebują
też nowych typów.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-generic-deriving-prof >= 1.10
Requires:	ghc-ghc-prim-prof
Requires:	ghc-mtl-prof
Requires:	ghc-transformers-prof >= 0.2

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStransformers-compat-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStransformers-compat-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStransformers-compat-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/Generic
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/Generic/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/Generic/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStransformers-compat-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/Classes/Generic/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
