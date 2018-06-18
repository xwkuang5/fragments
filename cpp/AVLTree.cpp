#include <AVLTree.hpp>

AVLTreeNode ::AVLTreeNode(int key)
    : key_(key), height_(0), parent_(NULL), left_(NULL), right_(NULL) {}
AVLTreeNode ::AVLTreeNode(int key, int height, AVLTreeNode *parent,
                          AVLTreeNode *left, AVLTreeNode *right)
    : key_(key), height_(height), parent_(parent), left_(left), right_(right) {}

AVLTree ::AVLTree() : root_(NULL) {}

AVLTree ::AVLTree(int key) { root_ = new node_type(key); }

bool AVLTree ::is_empty() { return root_ == NULL; }

void AVLTree ::rotate_right(node_ptr z) {
  node_ptr y = z->left_;

  z->left_ = y->right_;
  y->right_ = z;

  // make y the new root
  node_ptr tmp = z;
  z = y;
  y = tmp;

  set_height_from_children(z);
  set_height_from_children(y);
}

void AVLTree ::rotate_left(node_ptr z) {
  node_ptr y = z->right_;

  z->right_ = y->left_;
  y->left_ = z;

  node_ptr tmp = z;
  z = y;
  y = tmp;

  set_height_from_children(z);
  set_height_from_children(y);
}

void AVLTree ::set_height_from_children(node_ptr z) {
  int max_height = 0;

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
}

AVLTree ::node_ptr AVLTree ::bst_insert(int key) {
  node_ptr prev, cur = root_;

  while (cur != NULL) {
    prev = cur;
    if (cur->key_ == key) {
      // assume no duplicate key for now
      return NULL;
    } else if (cur->key_ < key) {
      cur = cur->right_;
    } else {
      cur = cur->left_;
    }
  }

  node_ptr ptr = new node_type(key, 0, prev, NULL, NULL);

  if (prev->key_ < key) {
    prev->right_ = ptr;
  } else {
    prev->left_ = ptr;
  }

  return ptr;
}

int AVLTree ::get_height(node_ptr z) {
  if (z == NULL) {
    return -1;
  } else {
    return z->height_;
  }
}

void AVLTree ::insert_key(int key) {
  node_ptr new_node = bst_insert(key);

  node_ptr parent = new_node->parent_;

  while (parent != NULL) {
    set_height_from_children(parent);
    if (std::abs(get_height(parent->left_) - get_height(parent->right_)) >= 2) {
      AVLFix(parent);
      break;
    } else {
      parent = parent->parent_;
    }
  }
}

void AVLTree ::inorder_traversal(node_ptr z) {
  if (z != NULL) {
    inorder_traversal(z->left_);
    std::cout << z->key_ << " ";
    inorder_traversal(z->right_);
  }
  std::cout << std::endl;
}

void AVLTree ::preorder_traversal(node_ptr z) {
  if (z != NULL) {
    std::cout << z->key_ << " ";
    preorder_traversal(z->left_);
    preorder_traversal(z->right_);
  }
  std::cout << std::endl;
}

void AVLTree ::postorder_traversal(node_ptr z) {
  if (z != NULL) {
    postorder_traversal(z->left_);
    postorder_traversal(z->right_);
    std::cout << z->key_ << " ";
  }
  std::cout << std::endl;
}

void AVLTree ::print_tree(node_ptr z) { ; }