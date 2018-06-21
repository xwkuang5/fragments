#include <iostream>

template <typename T> class Node {
public:
  T value_;
  Node *next_;

  Node(T value) : value_(value), next_(NULL) {}
  Node(T value, Node *next) : value_(value), next_(next) {}
};

template <typename T> class LinkedList {

private:
  typedef T value_type;
  typedef T &reference;
  typedef T *pointer;
  typedef Node<T> node_type;
  typedef Node<T> *node_ptr;
  node_ptr start_;

public:
  LinkedList() : start_(NULL) {}

  LinkedList(value_type value) { start_ = new node_type(value); }

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

    reference operator*() {
      return *this->_ptr;
    } // member access (./->) has precedence over dereference
    const node_ptr operator->() { return this->_ptr; }

    void operator=(const iterator &rhs) { _ptr = rhs._ptr; }

    bool operator==(const self_type &rhs) { return this->_ptr == rhs._ptr; }
    bool operator!=(const self_type &rhs) { return this->_ptr != rhs._ptr; }

  private:
    node_ptr _ptr;
  };

  iterator begin() { return iterator(this->start_); }

  iterator end() { return iterator(NULL); }

  void add(value_type value) {
    iterator prev, cur;
    cur = this->begin();

    while (cur != this->end()) {
      prev = cur;
      ++cur;
    }

    prev->next_ = new node_type(value);
  }
};

int main() {
  auto list = LinkedList<int>(3);

  list.add(4);
  list.add(5);

  typedef LinkedList<int>::iterator iterator;
  for (iterator iter = list.begin(); iter != list.end(); iter++) {
    std::cout << iter->value_ << std::endl;
  }
}
