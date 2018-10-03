#include "sort.h"

void swap(int *array, int i, int j) {
  if (i == j)
    return;
  int temp = array[i];
  array[i] = array[j];
  array[j] = temp;
  return;
}

void print(int *array, int size) {
  int i;
  for (i = 0; i < size; i++)
    printf("%d ", array[i]);
  printf("\n");
}

int left(int index) { return 2 * index + 1; }

int right(int index) { return 2 * index + 2; }

void max_heapify(int *array, int size, int index) {
  int left_child = left(index);
  int right_child = right(index);
  int largest;
  if (left_child < size && array[left_child] > array[index])
    largest = left_child;
  else
    largest = index;
  if (right_child < size && array[right_child] > array[largest])
    largest = right_child;
  if (largest != index) {
    swap(array, index, largest);
    max_heapify(array, size, largest);
  }
}

void build_heap(int *array, int size) {
  int i;
  for (i = size / 2; i >= 0; i--)
    max_heapify(array, size, i);
}

void heap_sort(int *array, int size) {
  build_heap(array, size);
  int i;
  for (i = size - 1; i >= 1; i--) {
    swap(array, 0, i);
    size--;
    max_heapify(array, size, 0);
  }
}

int hoare_partition(int *array, int low, int high) {
  int i = low - 1;
  int j = high + 1;
  int pivot = array[high];
  while (1) {
    while (array[++i] < pivot)
      ;
    while (array[--j] >= pivot)
      ;
    if (i < j) {
      swap(array, i, j);
    } else {
      return j;
    }
  }
}

int partition(int *array, int low, int high) {
  int pivot = array[high];
  int i = low - 1;
  int j;
  for (j = low; j <= high - 1; j++) {
    if (array[j] <= pivot) {
      i = i + 1;
      swap(array, i, j);
    }
  }
  swap(array, i + 1, high);
  return i + 1;
}

void qsort(int *array, int low, int high) {
  if (low < high) {
    int mid = partition(array, low, high);
    qsort(array, low, mid - 1);
    qsort(array, mid + 1, high);
  }
  return;
}

void merge(int *array, int low, int mid, int high) {
  int n1 = mid - low + 1;
  int n2 = high - mid;
  int *left = (int *)malloc(sizeof(int) * n1);
  int *right = (int *)malloc(sizeof(int) * n2);
  int i, j, k;
  for (i = 0; i < n1; i++) {
    left[i] = array[low + i];
  }
  for (i = 0; i < n2; i++) {
    right[i] = array[mid + 1 + i];
  }
  i = j = k = 0;
  while (i < n1 && j < n2) {
    if (left[i] <= right[j])
      array[low + k++] = left[i++];
    else
      array[low + k++] = right[j++];
  }
  while (i < n1) {
    array[low + k++] = left[i++];
  }
  while (j < n2) {
    array[low + k++] = right[j++];
  }
  free(left);
  free(right);
}

void merge_sort(int *array, int low, int high) {
  if (low < high) {
    int mid = (low + high) / 2;
    merge_sort(array, low, mid);
    merge_sort(array, mid + 1, high);
    merge(array, low, mid, high);
  }
}

void selection_sort(int *array, int low, int high) {
  int len = high - low + 1;
  int i, j;
  for (i = 0; i < len - 1; i++) {
    int min_index = i;
    for (j = i + 1; j < len; j++) {
      if (array[j] < array[min_index]) {
        min_index = j;
      }
    }
    swap(array, i, min_index);
  }
}

void insertion_sort(int *array, int low, int high) {
  if (low < high) {
    int len = high - low + 1;
    int i, j;
    for (i = 1; i < len; i++) {
      int key = array[i];
      j = i - 1;
      while (array[j] > key) {
        array[j + 1] = array[j];
        j--;
      }
      array[j + 1] = key;
    }
  }
}

void bubble_sort(int *array, int low, int high) {
  int i, j;
  for (i = 0; i < high - low + 1; i++) {
    for (j = high; j > i; j--) {
      if (array[j] < array[j - 1])
        swap(array, j, j - 1);
    }
  }
}

void mix_insertion_merge_sort(int *array, int low, int high, int k) {
  if (high - low + 1 < k) {
    insertion_sort(array, low, high);
  } else {
    int mid = (low + high) / 2;
    printf("%d\n", mid);
    mix_insertion_merge_sort(array, low, mid, k);
    mix_insertion_merge_sort(array, mid + 1, high, k);
    merge(array, low, mid, high);
  }
}

void counting_sort(int *array, int low, int high, int k) {
  int temp[high - low + 1];
  int sum[k + 1];
  int i;
  for (i = 0; i < k + 1; i++)
    sum[i] = 0;
  for (i = low; i <= high; i++)
    sum[array[i]] += 1;
  for (i = 1; i < k + 1; i++)
    sum[i] += sum[i - 1];
  for (i = 1; i < k + 1; i++)
    sum[i] -= 1;
  for (i = high; i >= low; i--) {
    temp[sum[array[i]]] = array[i];
    sum[array[i]] -= 1;
  }
  for (i = low; i <= high; i++)
    array[i] = temp[i];
}

int main() {
  int arr[] = {2, 1, 5, 2, 3, 5, 1, 2, 3, 3};
  // merge_sort(arr, 0, 4);
  // mix_insertion_merge_sort(arr, 0, 4, 3);
  // insertion_sort(arr, 0, 4);
  // selection_sort(arr, 0, 4);
  counting_sort(arr, 0, 9, 5);
  print(arr, 10);
  return 0;
}
