#ifndef SKIP_LIST_H
#define SKIP_LIST_H

#include <iostream>

#include "SkipListRandGen.hpp"
#include "SkipListSkipNode.hpp"

template <class Key, class Obj>
class SkipList {
  public:
    SkipList(float prob, int height, Key* key);
    ~SkipList();
 
    bool insert(Key* key, Obj* obj);
    bool remove(Key* key);
    Obj* search(Key* key);
    void dump(std::ofstream& ofs);

    class iterator {
      public:
        typedef iterator self_type;

        iterator(SkipNode<Key, Obj>* ptr) : ptr_(ptr) {}
        iterator(const self_type &rhs) : ptr_(rhs.ptr_) {}
        ~iterator() {}

        bool operator==(const self_type &rhs) { return ptr_ == rhs.ptr_; }
        bool operator!=(const self_type &rhs) { return ptr_ != rhs.ptr_; }

        const self_type operator++() {
          const self_type ret = self_type(this->ptr_);
          this->ptr_ = this->ptr_->forward_nodes[1];
          
          return ret;
        }

        self_type& operator++(int dummy) {
          this->ptr_ = this->ptr_->forward_nodes[1];

          return *this;
        }
        
        self_type& operator=(const self_type &rhs) {
          ptr_ = rhs.ptr_;

          return *this;
        }

        SkipNode<Key, Obj>& operator*() { return *ptr_; }
        SkipNode<Key, Obj>* operator->() { return ptr_; }

      private:
      public:
        SkipNode<Key, Obj>* ptr_;
    };

    const iterator begin() { return iterator(head->forward_nodes[1]); }
    const iterator end() { return iterator(tail); }
 
  private:
    SkipNode<Key, Obj>* head;
    SkipNode<Key, Obj>* tail;
    float prob_;
    int max_height;
    int cur_height;
    RandomHeight* rand_gen;
};

template <class Key, class Obj>
SkipList<Key, Obj>::SkipList(float prob, int height, Key* key) {
  cur_height = 1;
  max_height = height;
  rand_gen = new RandomHeight(prob, max_height);

  head = new SkipNode<Key, Obj>(max_height);
  tail = new SkipNode<Key, Obj>(key, nullptr, max_height);

  for (int i = 1; i <= max_height; i++) {
    head->forward_nodes[i] = tail;
  }
}

template <class Key, class Obj>
SkipList<Key, Obj>::~SkipList() {
  SkipNode<Key, Obj>* prev, tmp = head;

  while (tmp != nullptr) {
    prev = tmp;
    tmp = tmp->forward_nodes[1];

    delete prev;
  }

  delete rand_gen;
}

template <class Key, class Obj>
Obj* SkipList<Key, Obj>:: search(Key* key) {
  SkipNode<Key, Obj>* tmp = head;
  for (int level = cur_height; level >= 1; level--) {
    while (*(tmp->forward_nodes[level]->get_key()) < *key) {
      tmp = tmp->forward_nodes[level];
    }
  }

  tmp = tmp->forward_nodes[1];
  if (*(tmp->get_key()) == *key) {
    return tmp->get_obj();
  } else {
    return nullptr;
  }
}

template <class Key, class Obj>
bool SkipList<Key, Obj>::insert(Key* key, Obj* obj) {
  SkipNode<Key, Obj>* tmp = head;
  SkipNode<Key, Obj>** update_vec = new SkipNode<Key, Obj>*[max_height + 1];
  for (int i = 1; i <= max_height; i++) {
    update_vec[i] = nullptr;
  }

  for (int level = cur_height; level >= 1; level--) {
    while (*(tmp->forward_nodes[level]->get_key()) < *key) {
      tmp = tmp->forward_nodes[level];
    }
    update_vec[level] = tmp;
  }

  tmp = tmp->forward_nodes[1];
  if (*(tmp->get_key()) == *key) {
    delete [] update_vec;
    return false; 
  } else {
    int node_level = rand_gen->new_level();
    SkipNode<Key, Obj>* new_node = new SkipNode<Key, Obj>(key, obj, node_level);

    if (node_level > cur_height) {
      for (int i = cur_height + 1; i <= node_level; i++) {
        update_vec[i] = head;
      }
      cur_height = node_level;
    }

    for (int i = 1; i <= node_level; i++) {
      new_node->forward_nodes[i] = update_vec[i]->forward_nodes[i]; 
      update_vec[i]->forward_nodes[i] = new_node;
    }

    delete [] update_vec;
    return true;
  }
}

template <class Key, class Obj>
bool SkipList<Key, Obj>::remove(Key* key) {
  SkipNode<Key, Obj>* tmp = head;
  SkipNode<Key, Obj>** update_vec = new SkipNode<Key, Obj>*[max_height + 1];

  for (int i = cur_height; i >= 1; i--) {
    while (*(tmp->forward_nodes[i]->get_key()) < *key) {
      tmp = tmp->forward_nodes[i];
    }
    update_vec[i] = tmp;
  }

  tmp = tmp->forward_nodes[1];

  if (*(tmp->get_key()) == *key) {
    for (int i = 1; i <= tmp->get_height(); i++) {
      if (update_vec[i]->forward_nodes[i] != tmp) {
        break;
      }
      update_vec[i]->forward_nodes[i] = tmp->forward_nodes[i];
    }

    while (cur_height > 1 && head->forward_nodes[cur_height] == tail) {
      cur_height -= 1;
    }

    delete tmp;
    delete [] update_vec;

    return true;
  } else {
    delete [] update_vec;

    return false;
  }
}

#endif
