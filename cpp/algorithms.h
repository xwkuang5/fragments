#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))
#define MAX(X, Y) (((X) > (Y)) ? (X) : (Y))

void swap(int *array, int i, int j);
void print_array(int *array, int size);
int array_sum(int *array, int low, int high);
int *maximum_subarray(int *array, int low, int high);
int *maximum_cross_middle_subarray(int *array, int low, int mid, int high);
int *naive_maximum_subarray(int *array, int low, int high);

int randomized_partition(int *array, int low, int high);
int randomized_select(int *array, int low, int high, int i);

#endif