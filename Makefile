FILES_TO_RPM = eos_exporter res/eos_exporter.unit
SPECFILE = $(shell find . -type f -name *.spec)
BUILD_DATE = $(shell date +%FT%T%z)
GO_VERSION = $(shell go version | awk '{print $$3}')
GIT_COMMIT = $(shell git rev-parse --short HEAD)
PACKAGE  = $(shell awk '$$1 == "Name:"     { print $$2 }' $(SPECFILE) )
VERSION  = $(shell git describe --abbrev=0 | sed 's/^v//g' )
RELEASE  = $(shell awk '$$1 == "Release:"  { print $$2 }' $(SPECFILE) )
OS_ARCH = $(shell echo "$$(uname -s)/$$(uname -m)")
rpmbuild = ${shell pwd}/rpmbuild

.PHONY: build

descr:
	@echo "You are building the EOS exporter binary."

build:
	go generate
	go build .

run:
	go run eos_exporter.go

clean:
	@rm -f .build_date .git_commit .go_version .version eos_exporter
	@rm -rf $(PACKAGE)-$(VERSION)
	@rm -rf $(rpmbuild)
	@rm -rf *rpm

rpmdefines=--define='_topdir ${rpmbuild}' \
        --define='_sourcedir %{_topdir}/SOURCES' \
        --define='_builddir %{_topdir}/BUILD' \
        --define='_srcrpmdir %{_topdir}/SRPMS' \
        --define='_rpmdir %{_topdir}/RPMS'

dist: clean
	go generate
	go build .
	
	@mkdir -p $(PACKAGE)-$(VERSION)
	@cp -r $(FILES_TO_RPM) $(PACKAGE)-$(VERSION)
	tar cpfz ./$(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION)

prepare: dist
	@mkdir -p $(rpmbuild)/RPMS/x86_64
	@mkdir -p $(rpmbuild)/SRPMS/
	@mkdir -p $(rpmbuild)/SPECS/
	@mkdir -p $(rpmbuild)/SOURCES/
	@mkdir -p $(rpmbuild)/BUILD/
	@mv $(PACKAGE)-$(VERSION).tar.gz $(rpmbuild)/SOURCES 
	@cp $(SPECFILE) $(rpmbuild)/SOURCES 

srpm: prepare $(SPECFILE)
	@sed -i 's/_VERSION_/$(VERSION)/g' $(SPECFILE)
	rpmbuild --nodeps -bs $(rpmdefines) $(SPECFILE)
	#cp $(rpmbuild)/SRPMS/* .

rpm: srpm
	@sed -i 's/_VERSION_/$(VERSION)/g' $(SPECFILE)
	rpmbuild --nodeps -bb $(rpmdefines) $(SPECFILE)
	cp $(rpmbuild)/RPMS/x86_64/* .

all: descr build
