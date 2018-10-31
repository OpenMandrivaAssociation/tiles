%{?_javapackages_macros:%_javapackages_macros}
%global master_version 3
Name:          tiles
Version:       2.2.2
Release:       11.3
Summary:       Java templating framework for web application user interfaces
Group:         Development/Java
License:       ASL 2.0
Url:           http://tiles.apache.org/
Source0:       http://www.apache.org/dist/%{name}/v%{version}/%{name}-%{version}-src.tar.gz
# wget -O tiles-master-3-pom.xml http://svn.apache.org/repos/asf/tiles/maven/tags/tiles-master-3/pom.xml
Source1:       %{name}-master-%{master_version}-pom.xml
# force tomcat 7.x apis use
Source2:       %{name}-%{version}-2-depmap
# remove shale-test and maven-taglib-plugin
# change 
#  org.codehaus.mojo rat-maven-plugin in org.apache.rat apache-rat-plugin
#  org.codehaus.mojo jxr-maven-plugin in org.apache.maven.plugins maven-jxr-plugin
# use tomcat 7.x apis
Patch0:        %{name}-%{version}-fix-build.patch
# replace ognl ognl 2.7.3 with apache-commons-ognl
Patch1:        %{name}-%{version}-commons-ognl.patch
# add tiles-master relativePath
Patch2:        %{name}-%{version}-parent-pom.patch
# build fix fot tomcat 7.x apis
Patch3:        %{name}-%{version}-servlet-servlet30.patch
Patch4:        %{name}-%{version}-jsp-servlet30.patch

BuildRequires: java-devel

BuildRequires: apache-commons-digester
BuildRequires: apache-commons-ognl
BuildRequires: freemarker
BuildRequires: mvel
BuildRequires: portlet-2.0-api
BuildRequires: slf4j
BuildRequires: tomcat-lib
BuildRequires: tomcat-el-2.2-api
BuildRequires: tomcat-jsp-2.2-api
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: velocity-tools
BuildRequires: mvn(org.slf4j:jcl-over-slf4j)
BuildRequires: mvn(org.slf4j:slf4j-jdk14)

# test deps
%if 0
BuildRequires: mvn(org.easymock:easymockclassextension) >= 2.4
BuildRequires: mvn(org.apache.shale:shale-test) >= 1.0.5
%endif
BuildRequires: junit

BuildRequires: maven-local
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin

# requires by remote-resources-plugin
BuildRequires: mvn(org.apache.maven.shared:maven-artifact-resolver)
BuildRequires: mvn(org.apache.maven.shared:maven-shared-components:pom:)

BuildArch:     noarch

%description
Apache Tiles is a templating framework built to simplify the
development of web application user interfaces. Tiles allows
authors to define page fragments which can be assembled into
a complete page at runtime. These fragments, or tiles, can
be used as simple includes in order to reduce the duplication
of common page elements or embedded within other tiles to
develop a series of reusable templates. These templates
streamline the development of a consistent look and feel
across an entire application. Tiles grew in popularity as a
component of the popular Struts framework. It has since been
extracted from Struts and is now integrated with various
frameworks, such as Struts 2 and Shale.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0

%patch3 -p0
%patch4 -p0

# require org.springframework spring-webmvc-portlet 2.5.6
%pom_disable_module tiles-portlet-wildcard src/pom.xml
# org.springframework spring-web 2.5.6
%pom_disable_module tiles-servlet-wildcard src/pom.xml
# depends on previous artifacts
%pom_disable_module tiles-extras src/pom.xml
%pom_disable_module assembly src/pom.xml

sed -i "s|<artifactId>jasper-el|<artifactId>tomcat-jasper-el|" src/tiles-el/pom.xml

sed -i "s|<groupId>javax.servlet</groupId>|<groupId>org.apache.tomcat</groupId>|" src/tiles-core/pom.xml \
 src/tiles-api/pom.xml \
 src/tiles-velocity/pom.xml \
 src/tiles-servlet/pom.xml \
 src/tiles-compat/pom.xml \
 src/tiles-portlet/pom.xml \
 src/tiles-jsp/pom.xml \
 src/tiles-extras/pom.xml \
 src/tiles-freemarker/pom.xml \
 src/tiles-el/pom.xml \
 src/tiles-servlet-wildcard/pom.xml

sed -i "s|<artifactId>servlet-api</artifactId>|<artifactId>tomcat-servlet-api</artifactId>|" src/tiles-core/pom.xml \
 src/tiles-api/pom.xml \
 src/tiles-velocity/pom.xml \
 src/tiles-servlet/pom.xml \
 src/tiles-compat/pom.xml \
 src/tiles-portlet/pom.xml \
 src/tiles-jsp/pom.xml \
 src/tiles-extras/pom.xml \
 src/tiles-freemarker/pom.xml \
 src/tiles-el/pom.xml \
 src/tiles-servlet-wildcard/pom.xml

%pom_remove_parent src
#cp -p %{SOURCE1} pom.xml

%build

cd src
# TODO
# extras
# portlet-wildcard
# servlet-wildcard
%mvn_file :%{name}-api %{name}/api
%mvn_file :%{name}-compat %{name}/compat
%mvn_file :%{name}-core %{name}/core
%mvn_file :%{name}-el %{name}/el
%mvn_file :%{name}-freemarker %{name}/freemarker
%mvn_file :%{name}-jsp %{name}/jsp
%mvn_file :%{name}-mvel %{name}/mvel
%mvn_file :%{name}-ognl %{name}/ognl
%mvn_file :%{name}-portlet %{name}/portlet
%mvn_file :%{name}-servlet %{name}/servlet
%mvn_file :%{name}-template %{name}/template
%mvn_file :%{name}-velocity %{name}/velocity

# test skip for unavailable deps
%mvn_build -f -- -Dmaven.local.depmap.file="%{SOURCE2}"

%install

(
cd src
%mvn_install
)

%files -f src/.mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt NOTICE.txt

%files javadoc -f src/.mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-8
- Drop easymock2 BR - not needed.

* Wed Jul 10 2013 gil cattaneo <puntogil@libero.it> 2.2.2-7
- switch to XMvn
- minor changes to adapt to current guideline

* Tue Feb 19 2013 gil cattaneo <puntogil@libero.it> 2.2.2-6
- added maven-artifact-resolver and maven-shared-components as BR

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 gil cattaneo <puntogil@libero.it> 2.2.2-2
- Fixed list of files in the main package

* Sat May 26 2012 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm
