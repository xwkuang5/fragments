#include <iostream>

template <typename T> void print(T *array, size_t size) {
  for (size_t i = 0; i < size; i++) {
    std::cout << array[i] << " ";
  }
  std::cout << std::endl;
}

template <typename T> void swap(T *array, size_t i, size_t j) {
  T tmp = array[i];
  array[i] = array[j];
  array[j] = tmp;
}

template <typename T> void permute(T *array, size_t index, size_t size) {
  if (index == (size - 1)) {
    print(array, size);
  } else {
    for (size_t i = index; i < size; i++) {
      swap(array, index, i);
      permute(array, index + 1, size);
      swap(array, index, i);
    }
  }
}

int main() {
  int *array = new int[3];
  array[0] = 1;
  array[1] = 2;
  array[2] = 3;

  permute(array, 0, 3);
}
