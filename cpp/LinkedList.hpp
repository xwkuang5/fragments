#ifndef LINKED_LIST_H
#define LINKED_LIST_H

/**
 * Assume no duplicate key
 */

#include <iostream>

template <class Key, class Obj> class Node {
public:
  Key *key_;
  Obj *obj_;
  Node *next_;

  Node() : key_(NULL), obj_(NULL) {}
  Node(Key *key, Obj *obj) : key_(key), obj_(obj), next_(NULL) {}
  Node(Key *key, Obj *obj, Node *next) : key_(key), obj_(obj), next_(next) {}

  ~Node() {
    delete key_;
    delete obj_;
  }
};

template <class Key, class Obj> class LinkedList {

public:
  typedef Node<Key, Obj> node_type;
  typedef Node<Key, Obj> &node_reference;
  typedef Node<Key, Obj> *node_ptr;

private:
  node_ptr start_;

public:
  LinkedList() : start_(NULL) {}

  LinkedList(Key *key, Obj *obj) { start_ = new node_type(key, obj); }

  ~LinkedList() {
    node_ptr prev, cur = start_;

    while (cur != NULL) {
      prev = cur;
      cur = cur->next_;
      delete prev;
    }
  }

  class iterator {
  public:
    typedef iterator self_type;
    typedef std::forward_iterator_tag iterator_category;

    iterator() : _ptr(NULL) {}
    ~iterator(){};

    iterator(node_ptr ptr) : _ptr(ptr) {}

    iterator(const self_type &rhs) : _ptr(rhs._ptr) {}

    // postfix
    self_type operator++() {
      self_type current = iterator(*this);
      this->_ptr = this->_ptr->next_;
      return current;
    }

    // prefix
    self_type &operator++(int dummy) {
      this->_ptr = this->_ptr->next_;
      return *this;
    }

    node_reference operator*() {
      return *this->_ptr;
    } // member access (./->) has precedence over dekey_reference
    const node_ptr operator->() { return this->_ptr; }

    void operator=(const iterator &rhs) { _ptr = rhs._ptr; }

    bool operator==(const self_type &rhs) { return this->_ptr == rhs._ptr; }
    bool operator!=(const self_type &rhs) { return this->_ptr != rhs._ptr; }

  private:
    node_ptr _ptr;
  };

  iterator begin() { return iterator(this->start_); }

  iterator end() { return iterator(NULL); }

  void insert_front(Key *key, Obj *obj) {
    node_ptr new_head = new node_type(key, obj);
    new_head->next_ = start_;
    start_ = new_head;
  }

  void insert_back(Key *key, Obj *obj) {
    if (start_ == NULL) {
      start_ = new node_type(key, obj);
      return;
    }

    node_ptr prev, cur = start_;
    while (cur != NULL) {
      prev = cur;
      cur = cur->next_;
    }

    prev->next_ = new node_type(key, obj);
  }

  bool search(Key key) {
    for (auto iter = begin(); iter != end(); iter++) {
      if (*(iter->key_) == key) {
        return true;
      }
    }

    return false;
  }

  bool remove(Key key) {
    if (*(start_->key_) == key) {
      node_ptr new_start = start_->next_;
      delete start_;
      start_ = new_start;

      return true;
    }
    node_ptr prev, cur = start_;

    while (cur != NULL && *(cur->key_) != key) {
      prev = cur;
      cur = cur->next_;
    }

    if (cur == NULL) {
      return false;
    } else {
      prev->next_ = cur->next_;
      delete cur;

      return true;
    }
  }

  bool is_empty() { return start_ == NULL; }
};

#endif
