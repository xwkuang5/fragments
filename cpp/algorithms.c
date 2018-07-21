#include "algorithms.h"

void swap(int *array, int i, int j) {
  if (i != j) {
    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

void print_array(int *array, int size) {
  int i;
  for (i = 0; i < size; i++)
    printf("%d ", array[i]);
  printf("\n");
}

int array_sum(int *array, int low, int high) {
  int i, sum;
  for (i = 0; i < low; i++)
    array++;
  for (i = 0, sum = 0; i < high - low + 1; i++) {
    sum += *(array++);
  }
  return sum;
}

int *maximum_cross_middle_subarray(int *array, int low, int mid, int high) {
  int *result = (int *)malloc(sizeof(int) * 3);
  int left_sum = INT_MIN;
  int sum = 0;
  int i;
  for (i = mid; i >= low; i--) {
    sum += array[i];
    if (sum > left_sum) {
      left_sum = sum;
      result[0] = i;
    }
  }
  int right_sum = INT_MIN;
  sum = 0;
  for (i = mid + 1; i <= high; i++) {
    sum += array[i];
    if (sum > right_sum) {
      right_sum = sum;
      result[1] = i;
    }
  }
  result[2] = left_sum + right_sum;
  return result;
}

int *maximum_subarray(int *array, int low, int high) {
  if (low == high) {
    int *result = (int *)malloc(sizeof(int) * 3);
    result[0] = result[1] = low;
    result[2] = array[low];
    return result;
  } else {
    int *left, *middle, *right;
    int mid = (low + high) / 2;
    left = maximum_subarray(array, low, mid);
    middle = maximum_cross_middle_subarray(array, low, mid, high);
    right = maximum_subarray(array, mid + 1, high);
    if (left[2] >= middle[2]) {
      if (left[2] >= right[2]) {
        free(middle);
        free(right);
        return left;
      } else {
        free(left);
        free(middle);
        return right;
      }
    } else {
      if (middle[2] >= right[2]) {
        free(left);
        free(right);
        return middle;
      } else {
        free(left);
        free(middle);
        return right;
      }
    }
  }
}

int *naive_maximum_subarray(int *array, int low, int high) {
  int *result = (int *)malloc(sizeof(int) * 3);
  int final_sum = INT_MIN;
  int left_index, right_index;
  int i, j;
  for (i = 0; i < high - low + 1; i++) {
    int current_sum = 0;
    for (j = i; j < high - low + 1; j++) {
      current_sum = array_sum(array, i, j);
      if (current_sum > final_sum) {
        final_sum = current_sum;
        left_index = i;
        right_index = j;
      }
    }
  }
  result[0] = left_index;
  result[1] = right_index;
  result[2] = final_sum;
  return result;
}

int randomized_partition(int *array, int low, int high) {
  int pivot = array[high];
  int i, j;
  i = low - 1;
  for (j = low; j < high; j++) {
    if (array[j] <= pivot) {
      i = i + 1;
      swap(array, i, j);
    }
  }
  swap(array, i + 1, high);
  return i + 1;
}

int randomized_select(int *array, int low, int high, int i) {
  if (low == high) {
    return array[low];
  }
  int pivot_index = randomized_partition(array, low, high);
  int size = pivot_index - low + 1;
  if (i == size)
    return array[pivot_index];
  else if (i < size)
    return randomized_select(array, low, pivot_index - 1, i);
  else
    return randomized_select(array, pivot_index + 1, high, i - size);
}

int inversion_n_k(int n, int k) {
  // I(m, n) = \sum_{i = max(0, n - m + 1)}^{n}
  int row = n;
  int column = k + 1;
  int **table = (int **)malloc(sizeof(int *) * row);
  for (int i = 0; i < row; i++) {
    table[i] = (int *)malloc(sizeof(int) * column);
    memset(table[i], 0, sizeof(int) * column);
  }
  // I(1, 0) = 1
  table[0][0] = 1;
  for (int i = 1; i < row; i++) {
    for (int j = 0; j < column; j++) {
      for (int l = MAX(0, j - i); l <= j; l++) {
        table[i][j] += table[i - 1][l];
      }
    }
  }
  int ret = table[row - 1][column - 1];
  for (int i = 0; i < row; i++) {
    free(table[i]);
  }
  free(table);
  return ret;
}

float linear_time_median(int *arr, int low, int high) {
  int size = high - low + 1;

  if (size == 1) {
    return arr[low];
  } else if (size == 2) {
    return (arr[low] + arr[high]) / 2.0;
  } else {
    if (size % 2 == 0) {
      return (randomized_select(arr, low, high, size / 2) + randomized_select(arr, low, high, size / 2 + 1)) / 2.0;
    } else {
      return randomized_select(arr, low, high, size / 2 + 1);
    }
  }
}

int main() { 
  // printf("number of inversion is %d\n", inversion_n_k(1, 1)); 

  int arr[] = {1, 2, 3, 4, 5, 6};
  int low = 0;
  int high = sizeof(arr) / sizeof(int) - 1;

  printf("median is %f\n", linear_time_median(arr, low, high));
}