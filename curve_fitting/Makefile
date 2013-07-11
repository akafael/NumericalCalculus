SUBDIRS = tex src
#CC = gcc
#CCFLAGS = -Wall

#SOURCES = main2.c datalogger.c ui.c calibration.c
#HEADERS = main2.h datalogger.h ui.h #$(wildcard *.h)
CLEANDIRS = $(SUBDIRS:%=clean-%)

#SOURCES = main.c
#OBJECTS = $(wildcard $(SUBDIRS)/*.o) main.o
#HEADERS = $(wildcard *.h)

#@echo Subdirs: $(SUBDIRS)

#EXECUTABLE = main

.PHONY: all
#all: subdirs $(SOURCES) $(HEADERS) $(SUBDIRS) newrleg

.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	@$(MAKE) -C $@
@echo Objects: $(OBJECTS)

OBJECTS = $(wildcard tex/*.pdf)
#OBJECTS+= $(wildcard src/*.o)

.PHONY: print
print:
#        @echo Sources: $(SOURCES)
        @echo Objects: $(OBJECTS)
#	@echo Headers: $(HEADERS)
#        @echo Executable: newrleg

        @echo Subdirs: $(SUBDIRS)
        @echo Cleandirs: $(CLEANDIRS)

.PHONY: subdirs $(CLEANDIRS)
clean: $(CLEANDIRS)
	$(CLEANDIRS): 
		@$(MAKE) -C $(@:clean-%=%) clean
#		-rm -f newrleg *.o