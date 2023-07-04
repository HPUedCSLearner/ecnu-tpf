OBJDIR	 = ./build
OBJECTS	 = $(OBJDIR)/main.o $(OBJDIR)/master.o $(OBJDIR)/slave.o
SRCDIR   = ./src
SWCC     = swgcc

all: main.o master.o slave.o a.out

a.out: $(OBJECTS) | dir
	$(SWCC) -mhybrid  $^ -o $(OBJDIR)/a.out

main.o: $(SRCDIR)/main.c | dir
	$(SWCC) -mhost -c  $< -o $(OBJDIR)/main.o

master.o: $(SRCDIR)/master.c | dir
	$(SWCC) -mhost -c  $< -o $(OBJDIR)/master.o

slave.o: $(SRCDIR)/slave.c | dir
	$(SWCC) -mslave -msimd -c  $< -o $(OBJDIR)/slave.o

dir:
	@mkdir -p $(OBJDIR)

.PHONY: cl

cl:
	rm -rf ./build