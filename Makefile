TARGET = fire_planes
LIBS = -lm
CC = gcc
CFLAGS = -g -Wall

.PHONY: default all clean clobber

default: $(TARGET)
all: default

OBJECTS = fire_planes.o
HEADERS = $(wildcard *.h)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall $(LIBS) -o $@

clean:
	-rm -f *.o
	-rm -f $(TARGET)

clobber: clean
	-rm -f massif.out.*
