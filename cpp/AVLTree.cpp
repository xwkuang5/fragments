#include "AVLTree.hpp"

AVLTreeNode ::AVLTreeNode(int key)
    : key_(key), height_(0), num_left_(0), num_right_(0), is_left_(false),
      is_right_(false), parent_(NULL), left_(NULL), right_(NULL) {}
AVLTreeNode ::AVLTreeNode(int key, int height, int num_left, int num_right,
                          bool is_left, bool is_right, AVLTreeNode *parent,
                          AVLTreeNode *left, AVLTreeNode *right)
    : key_(key), height_(height), num_left_(num_left), num_right_(num_right),
      is_left_(is_left), is_right_(is_right), parent_(parent), left_(left),
      right_(right) {}

void AVLTreeNode ::print_node() {
  std::string parent = parent_ == NULL ? "NULL" : std::to_string(parent_->key_);

  std::string heredity_str;

  if (parent_ == NULL) {
    heredity_str = "root node";
  } else {
    if (is_left_) {
      heredity_str = "left child of " + std::to_string(parent_->key_);
    } else {
      heredity_str = "right child of " + std::to_string(parent_->key_);
    }
  }

  std::string left = "left subtree has " + std::to_string(num_left_) + " nodes";
  std::string right =
      "right subtree has " + std::to_string(num_right_) + " nodes";

  std ::cout << "key: " << key_ << ", height: " << height_ << ", " << left
             << ", " << right << ", " << heredity_str << std::endl;
}

AVLTree ::AVLTree() : root_(NULL) {}

AVLTree ::AVLTree(int key) { root_ = new node_type(key); }

bool AVLTree ::is_empty() { return root_ == NULL; }

void AVLTree ::rotate_right(node_ptr z) {
  node_ptr parent = z->parent_;

  node_ptr y = z->left_;
  node_ptr x = y->right_;

  z->left_ = x;
  if (x != NULL) {
    x->parent_ = z;
    x->is_left_ = true;
    x->is_right_ = false;
  }
  y->right_ = z;
  z->parent_ = y;
  y->parent_ = parent;

  if (parent != NULL && z->is_left_) {
    parent->left_ = y;
    y->is_left_ = true;
    y->is_right_ = false;
  } else if (parent != NULL && z->is_right_) {
    parent->right_ = y;
    y->is_left_ = false;
    y->is_right_ = true;
  }
  z->is_left_ = false;
  z->is_right_ = true;

  set_number_from_children(z);
  set_number_from_children(y);
  set_height_from_children(z);
  set_height_from_children(y);
}

void AVLTree ::rotate_left(node_ptr z) {
  node_ptr parent = z->parent_;

  node_ptr y = z->right_;
  node_ptr x = y->left_;
  z->right_ = x;
  if (x != NULL) {
    x->parent_ = z;
    x->is_left_ = false;
    x->is_right_ = true;
  }
  y->left_ = z;
  z->parent_ = y;
  y->parent_ = parent;

  if (parent != NULL && z->is_left_) {
    parent->left_ = y;
    y->is_left_ = true;
    y->is_right_ = false;
  } else if (parent != NULL && z->is_right_) {
    parent->right_ = y;
    y->is_left_ = false;
    y->is_right_ = true;
  }
  z->is_left_ = true;
  z->is_right_ = false;

  set_number_from_children(z);
  set_number_from_children(y);
  set_height_from_children(z);
  set_height_from_children(y);
}

void AVLTree ::set_height_from_children(node_ptr z) {
  int max_height = -1;

  if (z->left_ != NULL) {
    max_height =
        z->left_->height_ > max_height ? z->left_->height_ : max_height;
  }

  if (z->right_ != NULL) {
    max_height =
        z->right_->height_ > max_height ? z->right_->height_ : max_height;
  }

  z->height_ = max_height + 1;
}

void AVLTree ::set_number_from_children(node_ptr z) {
  if (z == NULL) {
    return;
  } else {
    z->num_left_ =
        z->left_ == NULL ? 0 : 1 + z->left_->num_left_ + z->left_->num_right_;

    z->num_right_ = z->right_ == NULL
                        ? 0
                        : 1 + z->right_->num_left_ + z->right_->num_right_;
  }
}

void AVLTree ::fix_node(node_ptr z) {
  int left_height = get_height(z->left_);
  int right_height = get_height(z->right_);

  if (left_height > right_height) {
    node_ptr y = z->left_;
    left_height = get_height(y->left_);
    right_height = get_height(y->right_);

    if (left_height >= right_height) {
      // single right rotation on z
      rotate_right(z);
    } else {
      // single left rotation on y + single right rotation on z
      rotate_left(y);
      rotate_right(z);
    }
  } else {
    node_ptr y = z->right_;
    left_height = get_height(y->left_);
    right_height = get_height(y->right_);

    if (left_height >= right_height) {
      // single right rotation on y + single left rotation on z
      rotate_right(y);
      rotate_left(z);
    } else {
      // single left rotation on z
      rotate_left(z);
    }
  }
  if (root_ == z) {
    root_ = z->parent_;
  }
}

AVLTree ::node_ptr AVLTree ::bst_insert(int key) {

  if (root_ == NULL) {
    root_ = new node_type(key);
    return root_;
  }

  node_ptr prev, cur = root_;

  while (cur != NULL) {
    prev = cur;
    if (cur->key_ == key) {
      return NULL;
    } else if (cur->key_ < key) {
      cur = cur->right_;
    } else {
      cur = cur->left_;
    }
  }

  if (prev->key_ < key) {
    prev->right_ = new node_type(key, 0, 0, 0, false, true, prev, NULL, NULL);
    return prev->right_;
  } else {
    prev->left_ = new node_type(key, 0, 0, 0, true, false, prev, NULL, NULL);
    return prev->left_;
  }
}

AVLTree::node_ptr AVLTree ::bst_delete(int key) {
  if (root_ == NULL) {
    return NULL;
  }

  node_ptr cur = root_;
  while (cur != NULL) {
    if (cur->key_ < key) {
      cur = cur->right_;
    } else if (cur->key_ > key) {
      cur = cur->left_;
    } else {
      break;
    }
  }

  if (cur == NULL) {
    // key does not exist
    return NULL;
  } else if (root_ == cur) {
    // delete root node
    if (root_->left_ == NULL && root_->right_ == NULL) {
      // if root node is a leaf
      delete root_;
      root_ = NULL;
      return NULL;
    } else if (root_->left_ == NULL && root_->right_ != NULL) {
      // if root node only has right child
      node_ptr tmp = root_;
      root_ = root_->right_;
      delete tmp;
      return root_;
    } else if (root_->left_ != NULL && root_->right_ == NULL) {
      // if root node only has left child
      node_ptr tmp = root_;
      root_ = root_->left_;
      delete tmp;
      return root_;
    } else {
      // if root node has two children => swap with successor
      node_ptr successor, successor_parent;
      successor = get_successor(root_);
      successor_parent = successor->parent_;
      if (successor_parent == root_) {
        // right child of the root node is a leaf
        root_->right_ = NULL;
      } else {
        if (successor->right_ != NULL) {
          // successor has a right child => connect it to sucessor's
          // parent
          successor_parent->left_ = successor->right_;
          successor->right_->parent_ = successor_parent;
          successor->right_->is_left_ = successor->is_left_;
          successor->right_->is_right_ = successor->is_right_;
        } else {
          // successor is a leaf
          successor_parent->left_ = NULL;
        }
      }
      // swap with successor
      root_->key_ = successor->key_;
      // delete successor
      delete successor;
      // return the parent of the deleted node
      return successor_parent;
    }
  } else {
    // cur is not root => must have parent
    node_ptr parent = cur->parent_;
    if (cur->left_ == NULL && cur->right_ == NULL) {
      // cur is a leaf => update cur's parent
      if (cur->is_left_) {
        parent->left_ = NULL;
      } else {
        parent->right_ = NULL;
      }
      // delete cur
      delete cur;
      // return the parent of the delete node
      return parent;
    } else if (cur->left_ != NULL && cur->right_ == NULL) {
      // cur has only a left child => swap predecessor up
      node_ptr predecessor, predecessor_parent;
      predecessor = get_predecessor(cur);
      predecessor_parent = predecessor->parent_;
      if (predecessor_parent == cur) {
        // left child of cur is a straight branch
        if (predecessor->left_ != NULL) {
          // left child of cur has a left child
          predecessor_parent->left_ = predecessor->left_;
          predecessor->left_->parent_ = predecessor->parent_;
        } else {
          // left child of cur is a leaf
          predecessor_parent->left_ = NULL;
        }
      } else {
        // left child of cur is a subtree (with right children)
        if (predecessor->right_ != NULL) {
          // predecessor has a right child => connect it to predecessor's
          // parent
          predecessor_parent->left_ = predecessor->right_;
          predecessor->right_->parent_ = predecessor_parent;
          // predecessor->right_->is_left_ = predecessor->is_left_;
          predecessor->right_->is_left_ = false;
          // predecessor->right_->is_right_ = predecessor->is_right_;
          predecessor->right_->is_right_ = true;
        } else {
          // predecessor is a leaf
          predecessor_parent->left_ = NULL;
        }
      }
      // swap with predecessor
      cur->key_ = predecessor->key_;
      // delete predecessor
      delete predecessor;
      // return the parent of the deleted node
      return predecessor_parent;
    } else {
      // swap successor up
      node_ptr successor = get_successor(cur);
      node_ptr successor_parent = successor->parent_;
      if (successor_parent == cur) {
        // right child of cur is a straight branch
        if (successor->right_ != NULL) {
          // right child of cur has a right child
          successor_parent->right_ = successor->right_;
          successor->right_->parent_ = successor_parent;
        } else {
          // right child of cur is a leaf
          successor_parent->right_ = NULL;
        }
      } else {
        // right child of cur is a subtree (with left children)
        if (successor->right_ != NULL) {
          // successor has a left child => connect it to successor's
          // parent
          successor_parent->left_ = successor->right_;
          successor->right_->parent_ = successor_parent;
          // successor->right_->is_left_ = successor->is_left_;
          successor->right_->is_left_ = true; // equivalent to the line above
          // successor->right_->is_right_ = successor->is_right_;
          successor->right_->is_right_ = false; // equivalent to the line above
        } else {
          // successor is a leaf
          successor_parent->left_ = NULL;
        }
      }
      // swap with successor
      cur->key_ = successor->key_;
      // delete successor
      delete successor;
      // return the parent of the deleted node
      return successor_parent;
    }
  }
}

AVLTree ::node_ptr AVLTree ::get_root() { return root_; }

AVLTree ::node_ptr AVLTree ::get_left_most() {
  node_ptr tmp = root_;

  while (tmp->left_ != NULL) {
    tmp = tmp->left_;
  }

  return tmp;
}

AVLTree ::node_ptr AVLTree ::get_right_most() {
  node_ptr tmp = root_;

  while (tmp->right_ != NULL) {
    tmp = tmp->right_;
  }

  return tmp;
}

AVLTree ::node_ptr AVLTree ::get_predecessor(AVLTree ::node_ptr z) {
  if (z == NULL) {
    return NULL;
  }

  node_ptr prev, tmp = z;

  if (tmp->left_ != NULL) {
    prev = tmp;
    tmp = tmp->left_;
    while (tmp != NULL) {
      prev = tmp;
      tmp = tmp->right_;
    }

    return prev;
  } else {
    while (tmp != NULL && tmp->is_left_) {
      tmp = tmp->parent_;
    }

    if (tmp == NULL || root_ == tmp) {
      // z is the first node in the tree
      return NULL;
    } else {
      return tmp->parent_;
    }
  }
}

AVLTree ::node_ptr AVLTree ::get_successor(AVLTree ::node_ptr z) {
  if (z == NULL) {
    return NULL;
  }

  node_ptr prev, tmp = z;

  if (tmp->right_ != NULL) {
    prev = tmp;
    tmp = tmp->right_;
    while (tmp != NULL) {
      prev = tmp;
      tmp = tmp->left_;
    }
    return prev;
  } else {
    while (tmp != NULL && tmp->is_right_) {
      tmp = tmp->parent_;
    }
    if (tmp == NULL || root_ == tmp) {
      // node z is the last node in the tree
      return NULL;
    } else {
      return tmp->parent_;
    }
  }
}

AVLTree::node_ptr AVLTree::get_ith_node(AVLTree::node_ptr z, int i) {
  // assume i is 1-based
  if (i == z->num_left_ + 1) {
    return z;
  } else if (i <= 0) {
    return NULL;
  } else {
    if (i <= z->num_left_) {
      return get_ith_node(z->left_, i);
    } else {
      return get_ith_node(z->right_, i - z->num_left_ - 1);
    }
  }
}

AVLTree::node_ptr AVLTree::get_ith_successor(AVLTree::node_ptr z, int i) {
  if (i == 0) {
    return z;
  } else {
    if (i <= z->num_right_) {
      return get_ith_node(z->right_, i);
    } else {
      if (z->is_left_) {
        return get_ith_successor(z->parent_, i - z->num_right_ - 1);
      } else if (z->is_right_) {
        return get_ith_successor(z->parent_, i + z->num_left_ + 1);
      } else {
        // z is the node and i > z->num_right
        return NULL;
      }
    }
  }
}

int AVLTree ::get_height(node_ptr z) {
  if (z == NULL) {
    return -1;
  } else {
    return z->height_;
  }
}

AVLTree ::node_ptr AVLTree ::insert_key(int key) {
  node_ptr new_node = bst_insert(key);

  node_ptr parent = new_node->parent_;

  while (parent != NULL) {
    set_number_from_children(parent);
    set_height_from_children(parent);
    if (std::abs(get_height(parent->left_) - get_height(parent->right_)) >= 2) {
      fix_node(parent);
      // break;
      // go all the way up to the root to correct the number of children
    } else {
      parent = parent->parent_;
    }
  }

  return new_node;
}

void AVLTree ::delete_key(int key) {
  node_ptr z = bst_delete(key);

  while (z != NULL) {
    set_number_from_children(z);
    set_height_from_children(z);

    if (std::abs(get_height(z->left_) - get_height(z->right_)) >= 2) {
      fix_node(z);
    }
    z = z->parent_;
  }
}

bool AVLTree ::search_key(int key) {
  node_ptr tmp = root_;

  while (tmp != NULL) {
    if (tmp->key_ == key) {
      return true;
    } else if (tmp->key_ < key) {
      tmp = tmp->right_;
    } else {
      tmp = tmp->left_;
    }
  }
  return false;
}

void AVLTree ::inorder_traversal(node_ptr z) {
  if (z != NULL) {
    inorder_traversal(z->left_);
    z->print_node();
    inorder_traversal(z->right_);
  }
}

void AVLTree ::preorder_traversal(node_ptr z) {
  if (z != NULL) {
    std::cout << z->key_ << " ";
    preorder_traversal(z->left_);
    preorder_traversal(z->right_);
  }
}

void AVLTree ::postorder_traversal(node_ptr z) {
  if (z != NULL) {
    postorder_traversal(z->left_);
    postorder_traversal(z->right_);
    std::cout << z->key_ << " ";
  }
}

AVLTree::ForwardIterator AVLTree::begin() {
  return ForwardIterator(this, get_left_most());
}

AVLTree::ForwardIterator AVLTree::end() { return ForwardIterator(this, NULL); }

AVLTree::ForwardIterator::ForwardIterator()
    : _tree_ptr(NULL), _node_ptr(NULL) {}

AVLTree::ForwardIterator::ForwardIterator(AVLTree::tree_ptr tptr,
                                          AVLTree::node_ptr nptr)
    : _tree_ptr(tptr), _node_ptr(nptr) {}

AVLTree::ForwardIterator::ForwardIterator(
    const AVLTree::ForwardIterator::self_type &rhs)
    : _tree_ptr(rhs._tree_ptr), _node_ptr(rhs._node_ptr) {}

AVLTree::ForwardIterator::~ForwardIterator() {
  _tree_ptr = NULL;
  _node_ptr = NULL;
}

AVLTree::ForwardIterator::self_type AVLTree::ForwardIterator::operator++() {
  self_type current = self_type(*this);
  _node_ptr = _tree_ptr->get_successor(_node_ptr);

  return current;
}

AVLTree::ForwardIterator::self_type &AVLTree::ForwardIterator::
operator++(int dummy) {
  _node_ptr = _tree_ptr->get_successor(_node_ptr);

  return *this;
}

AVLTree::node_ptr AVLTree::ForwardIterator::operator->() { return _node_ptr; }

AVLTree::node_type AVLTree::ForwardIterator::operator*() { return *_node_ptr; }

bool AVLTree::ForwardIterator::
operator==(const AVLTree::ForwardIterator::self_type &rhs) {
  return _tree_ptr == rhs._tree_ptr && _node_ptr == rhs._node_ptr;
}

bool AVLTree::ForwardIterator::
operator!=(const AVLTree::ForwardIterator::self_type &rhs) {
  return !(*this == rhs);
}

void AVLTree::ForwardIterator::
operator=(const AVLTree::ForwardIterator::self_type &rhs) {
  _tree_ptr = rhs._tree_ptr;
  _node_ptr = rhs._node_ptr;
}

AVLTree::ReverseIterator AVLTree::rbegin() {
  return ReverseIterator(this, get_right_most());
}

AVLTree::ReverseIterator AVLTree::rend() { return ReverseIterator(this, NULL); }

AVLTree::ReverseIterator::ReverseIterator()
    : _tree_ptr(NULL), _node_ptr(NULL) {}

AVLTree::ReverseIterator::ReverseIterator(AVLTree::tree_ptr tptr,
                                          AVLTree::node_ptr nptr)
    : _tree_ptr(tptr), _node_ptr(nptr) {}

AVLTree::ReverseIterator::ReverseIterator(
    const AVLTree::ReverseIterator::self_type &rhs)
    : _tree_ptr(rhs._tree_ptr), _node_ptr(rhs._node_ptr) {}

AVLTree::ReverseIterator::~ReverseIterator() {
  _tree_ptr = NULL;
  _node_ptr = NULL;
}

AVLTree::ReverseIterator::self_type AVLTree::ReverseIterator::operator++() {
  self_type current = self_type(*this);
  _node_ptr = _tree_ptr->get_predecessor(_node_ptr);

  return current;
}

AVLTree::ReverseIterator::self_type &AVLTree::ReverseIterator::
operator++(int dummy) {
  _node_ptr = _tree_ptr->get_predecessor(_node_ptr);

  return *this;
}

AVLTree::node_ptr AVLTree::ReverseIterator::operator->() { return _node_ptr; }

AVLTree::node_type AVLTree::ReverseIterator::operator*() { return *_node_ptr; }

bool AVLTree::ReverseIterator::
operator==(const AVLTree::ReverseIterator::self_type &rhs) {
  return _tree_ptr == rhs._tree_ptr && _node_ptr == rhs._node_ptr;
}

bool AVLTree::ReverseIterator::
operator!=(const AVLTree::ReverseIterator::self_type &rhs) {
  return !(*this == rhs);
}

void AVLTree::ReverseIterator::
operator=(const AVLTree::ReverseIterator::self_type &rhs) {
  _tree_ptr = rhs._tree_ptr;
  _node_ptr = rhs._node_ptr;
}
