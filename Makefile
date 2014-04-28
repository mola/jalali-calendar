PKGNAME = Jalali-applet
VERSION= 1.6.4
PYTHON=python
PKGDIR = /usr/share/jalali-calendar
LIBDIR = /usr/lib/


install:
	mkdir -p $(DESTDIR)$(PKGDIR)
	mkdir -p $(DESTDIR)$(PKGDIR)/date
	mkdir -p $(DESTDIR)$(LIBDIR)/bonobo/servers

	install -p -m644 COPYING $(DESTDIR)$(PKGDIR)/.
	install -p -m755 src/*.py $(DESTDIR)$(PKGDIR)/.
	install -p -m644 src/138*.xml $(DESTDIR)$(PKGDIR)/.
	install -p -m644 src/*.glade $(DESTDIR)$(PKGDIR)/.
	install -p -m644 src/GNOME_PyJcalendarApplet.server $(DESTDIR)/$(LIBDIR)/bonobo/servers
	install -p -m644 pixmaps/date/*.png $(DESTDIR)$(PKGDIR)/date/.
	install -p -m644 pixmaps/*.png $(DESTDIR)$(PKGDIR)/.

	chmod +x $(DESTDIR)$(PKGDIR)/jcalendar.py