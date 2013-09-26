debian
======

Copy all the configuration and scripts into scripts1.0 following
the defined structure.


usr/
└── local
    ├── sbin

usr/
└── local
    ├── smoothsec


Edit the DEBIAN/control file

build the package with: fakeroot dpkg-deb --build scripts1.0

Test it: dpkg -i scripts1.0.deb
