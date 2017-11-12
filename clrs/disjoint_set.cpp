#include "disjoint_set.hpp"

data_structure::disjoint_set::disjoint_set(int size) {
    this->size = size;

    this->parent = new int[this->size];
    this->rank = new int[this->size];

    std::fill(&this->parent[0], &this->parent[0] + this->size, -1);
}

void data_structure::disjoint_set::make_set(int i) {
    this->parent[i] = i;
    this->rank[i] = 1;
}

int data_structure::disjoint_set::find(int i) {
    if (this->parent[i] == i) {
        return i;
    } else {
        int parent = this->find(this->parent[i]);
        // path compression
        this->parent[i] = parent;

        return parent;
    }
}

void data_structure::disjoint_set::union_by_rank(int i, int j) {
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

data_structure::disjoint_set::~disjoint_set() {
    delete [] this->parent;
    delete [] this->rank;
}

int main(void) {
    data_structure::disjoint_set tmp = data_structure::disjoint_set(5);
    tmp.make_set(0);
    tmp.make_set(1);
    tmp.make_set(2);
    tmp.make_set(3);
    tmp.make_set(4);
    tmp.union_by_rank(1, 2);
    std::cout << tmp.find(1) << std::endl;
}