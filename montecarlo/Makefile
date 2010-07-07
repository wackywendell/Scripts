# A very generic makefile for c++ programs.
# just replace the target name (and make sure that the MAIN variable is correct)
# and that all the source files are in one directory, and it should work. 

# this is the filename of the final executable
TARGET := montecarlo
MAIN = main.cpp

SRCS := $(wildcard *.cpp)
HEADS := $(wildcard *.hpp)
# any x.hpp is assumed to compile to an object x.o
# can't assume that with x.cpp : e.g. main.cpp has no main.o
OBJS := $(patsubst %.hpp,%.o,$(HEADS))
FLAGS = -Wall

all : $(TARGET)

$(TARGET) : $(OBJS) $(MAIN)
	@echo Making final executable $(TARGET)
	g++ $(FLAGS) -o "$(TARGET)" $(MAIN) $(OBJS)

%.o : %.cpp %.hpp
	@echo Making $@
	g++ $(FLAGS) -c -o $@ $<

run : all
	./$(TARGET)

# notice the dash before 'rm' - that tells make to ignore errors
clean :
	@echo Deleting main and object files
	-rm $(TARGET) *.o
	