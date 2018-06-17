#ifndef DISJOINT_SET_H
#define DISJOINT_SET_H

#include <iostream>

namespace data_structure {

class disjoint_set {
private:
  int size;
  int *parent;
  int *rank;

public:
  disjoint_set(int size);

  void make_set(int i);

  int find(int i);

  void union_by_rank(int i, int j);

  ~disjoint_set();
};
} // namespace data_structure
#endif