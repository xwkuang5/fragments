CFLAGS=-Wall
cc=gcc

sort: sort.o
	cc sort.o -o sort $(FLAGS)

sort.o: sort.c sort.h
	cc -c sort.c

algorithms: algorithms.o
	cc algorithms.o -o algorithms $(FLAGS)

algorithms.o: algorithms.h algorithms.c
	cc -c algorithms.c

