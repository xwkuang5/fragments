#include "AVLTree.hpp"

AVLTreeNode ::AVLTreeNode(int key)
    : key_(key), height_(0), is_left_(false), is_right_(false), parent_(NULL), left_(NULL), right_(NULL) {}
AVLTreeNode ::AVLTreeNode(int key, int height, bool is_left, bool is_right, AVLTreeNode *parent,
                          AVLTreeNode *left, AVLTreeNode *right)
    : key_(key), height_(height), is_left_(is_left), is_right_(is_right), parent_(parent), left_(left), right_(right) {}

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
  std :: cout << "key: " << key_ << ", height: " << height_ << ", left child: " << left << ", right child: " << right << ", " << heredity_str << std::endl;
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

  if (prev->key_ < key) {
    prev->right_ = new node_type(key, 0, false, true, prev, NULL, NULL);
    return prev->right_;
  } else {
    prev->left_ = new node_type(key, 0, true, false, prev, NULL, NULL);
    return prev->left_;
  }
}

AVLTree ::node_ptr AVLTree ::get_root() { return root_; }

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
      break;
    } else {
      parent = parent->parent_;
    }
  }
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

void AVLTree ::print_tree(node_ptr z) { ; }


int main() {
    AVLTree *tree = new AVLTree();
    
    // // Test rotate right
    // AVLTree ::node_ptr root = new AVLTree ::node_type(100, 2, false, false, NULL, NULL, NULL);
    // AVLTree ::node_ptr z = new AVLTree ::node_type(3, 1, true, false, root, NULL, NULL);
    // AVLTree ::node_ptr y = new AVLTree ::node_type(2, 0, true, false, z, NULL, NULL);
    // AVLTree ::node_ptr x = new AVLTree ::node_type(1, 0, true, false, y, NULL, NULL);
    // root->left_ = z;
    // z->left_ = y;
    // y->left_ = x;
    // tree->rotate_right(z);
    // tree->inorder_traversal(root);

    // // Test rotate left
    // AVLTree ::node_ptr root = new AVLTree ::node_type(1, 2, false, false, NULL, NULL, NULL);
    // AVLTree ::node_ptr z = new AVLTree ::node_type(2, 1, false, true, root, NULL, NULL);
    // AVLTree ::node_ptr y = new AVLTree ::node_type(3, 0, false, true, z, NULL, NULL);
    // AVLTree ::node_ptr x = new AVLTree ::node_type(4, 0, false, true, y, NULL, NULL);
    // root->right_ = z;
    // z->right_ = y;
    // y->right_ = x;
    // tree->rotate_left(z);
    // tree->inorder_traversal(root);

    // // Test double rotation (left heavy)
    // AVLTree ::node_ptr root = new AVLTree ::node_type(100, 2, false, false, NULL, NULL, NULL);
    // AVLTree ::node_ptr z = new AVLTree ::node_type(3, 1, true, false, root, NULL, NULL);
    // AVLTree ::node_ptr y = new AVLTree ::node_type(1, 0, true, false, z, NULL, NULL);
    // AVLTree ::node_ptr x = new AVLTree ::node_type(2, 0, false, true, y, NULL, NULL);
    // root->left_ = z;
    // z->left_ = y;
    // y->right_ = x;
    // tree->rotate_left(y);
    // tree->rotate_right(z);
    // tree->inorder_traversal(root);

    // // Test double rotation (right heavy)
    AVLTree ::node_ptr root = new AVLTree ::node_type(0, 2, false, false, NULL, NULL, NULL);
    AVLTree ::node_ptr z = new AVLTree ::node_type(1, 1, false, true, root, NULL, NULL);
    AVLTree ::node_ptr y = new AVLTree ::node_type(3, 0, false, true, z, NULL, NULL);
    AVLTree ::node_ptr x = new AVLTree ::node_type(2, 0, true, false, y, NULL, NULL);
    root->right_ = z;
    z->right_ = y;
    y->left_ = x;
    tree->rotate_right(y);
    tree->rotate_left(z);
    tree->inorder_traversal(root);

    return 0;
}
