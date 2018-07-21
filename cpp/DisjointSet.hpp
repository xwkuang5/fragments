#ifndef DisjointSet_H
#define DisjointSet_H

#include <iostream>

class DisjointSet {
private:
  int size;
  int *parent;
  int *rank;

public:
  DisjointSet(int size);

  void make_set(int i);

  int find(int i);

  void union_by_rank(int i, int j);

  ~DisjointSet();
};

DisjointSet::DisjointSet(int size) {
  this->size = size;

  this->parent = new int[this->size];
  this->rank = new int[this->size];

  std::fill(&this->parent[0], &this->parent[0] + this->size, -1);
}

void DisjointSet::make_set(int i) {
  this->parent[i] = i;
  this->rank[i] = 1;
}

int DisjointSet::find(int i) {
  if (this->parent[i] == i) {
    return i;
  } else {
    int parent = this->find(this->parent[i]);
    // path compression
    this->parent[i] = parent;

    return parent;
  }
}

void DisjointSet::union_by_rank(int i, int j) {
  int parent_i = this->find(i);
  int parent_j = this->find(j);
  if (parent_i != parent_j) {
    int rank_i = this->rank[parent_i];
    int rank_j = this->rank[parent_j];

    if (rank_i < rank_j) {
      this->parent[parent_i] = parent_j;
    } else if (rank_i > rank_j) {
      this->parent[parent_j] = parent_i;
    } else {
      this->parent[parent_j] = parent_i;
      this->rank[parent_i] += 1;
    }
  }
}

DisjointSet::~DisjointSet() {
  delete[] this->parent;
  delete[] this->rank;
}

#endif
