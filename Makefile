# Makefile for building the core C++ static library

LIBDIR = lib
INCLUDEDIR = include
SRCDIR = src
LIBNAME = libgridfit.a

$(LIBDIR)/$(LIBNAME): $(SRCDIR)/interp.cpp $(INCLUDEDIR)/interp.h
	@mkdir -p $(LIBDIR)
	g++ -c $(SRCDIR)/interp.cpp -I$(INCLUDEDIR) -o $(LIBDIR)/interp.o
	ar rcs $(LIBDIR)/$(LIBNAME) $(LIBDIR)/interp.o

.PHONY: clean
clean:
	rm -rf $(LIBDIR)/*.o $(LIBDIR)/$(LIBNAME)
