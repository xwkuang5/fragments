#include "AVLTree.hpp"

AVLTreeNode ::AVLTreeNode(int key)
    : key_(key), height_(0), is_left_(false), is_right_(false), parent_(NULL),
      left_(NULL), right_(NULL) {}
AVLTreeNode ::AVLTreeNode(int key, int height, bool is_left, bool is_right,
                          AVLTreeNode *parent, AVLTreeNode *left,
                          AVLTreeNode *right)
    : key_(key), height_(height), is_left_(is_left), is_right_(is_right),
      parent_(parent), left_(left), right_(right) {}

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

  std::string left = left_ == NULL ? "NULL" : std::to_string(left_->key_);
  std::string right = right_ == NULL ? "NULL" : std::to_string(right_->key_);
  std ::cout << "key: " << key_ << ", height: " << height_
             << ", left child: " << left << ", right child: " << right << ", "
             << heredity_str << std::endl;
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
  if (root_ == z)
    root_ = z->parent_;
}

AVLTree ::node_ptr AVLTree ::bst_insert(int key) {

  if (root_ == NULL) {
    root_ = new node_type(key, 0, false, false, NULL, NULL, NULL);
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
    prev->right_ = new node_type(key, 0, false, true, prev, NULL, NULL);
    return prev->right_;
  } else {
    prev->left_ = new node_type(key, 0, true, false, prev, NULL, NULL);
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
    set_height_from_children(parent);
    if (std::abs(get_height(parent->left_) - get_height(parent->right_)) >= 2) {
      fix_node(parent);
      break;
    } else {
      parent = parent->parent_;
    }
  }

  return new_node;
}

void AVLTree ::delete_key(int key) {
  node_ptr z = bst_delete(key);

  while (z != NULL) {
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
