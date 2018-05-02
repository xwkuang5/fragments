#ifndef SORT_H
#define SORT_H
#include <stdio.h>
#include <stdlib.h>

void swap(int *array, int i, int j);

int left(int index);
int right(int index);
void max_heapify(int *array, int size, int index);
void build_heap(int *array, int size);
void heap_sort(int *array, int size);


int hoare_partition(int *array, int low, int high);
int partition(int *array, int low, int high);
void qsort(int *array, int low, int high);

void merge_sort(int *array, int low, int high);
void merge(int *array, int low, int mid, int high);

void selection_sort(int *array, int low, int high);

void insertion_sort(int *array, int low, int high);

void bubble_sort(int *array, int low, int high);

void counting_sort(int *array, int low, int high, int k);

void mix_insertion_merge_sort(int *array, int low, int high, int k);

#endif
