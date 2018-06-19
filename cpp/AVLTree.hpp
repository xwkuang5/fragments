#ifndef AVL_TREE_H
#define AVL_TREE_H

#include <cmath>
#include <iostream>
#include <string>

class AVLTreeNode {
public:
  int key_;
  int height_;
  bool is_left_;
  bool is_right_;
  AVLTreeNode *parent_;
  AVLTreeNode *left_;
  AVLTreeNode *right_;

  AVLTreeNode(int key);
  AVLTreeNode(int key, int height, bool is_left, bool is_right, AVLTreeNode *parent, AVLTreeNode *left,
              AVLTreeNode *right);

  void print_node();
};

class AVLTree {
public:
  typedef AVLTreeNode node_type;
  typedef AVLTreeNode *node_ptr;

  node_ptr root_;

  void fix_node(node_ptr z);
  void rotate_right(node_ptr z);
  void rotate_left(node_ptr z);
  void set_height_from_children(node_ptr z);
  node_ptr bst_insert(int key);

public:
  AVLTree();
  AVLTree(int key);
  void insert_key(int key);
  void delete_key(int key);
  bool search_key(int key);
  bool is_empty();
  node_ptr get_root();
  int get_height(node_ptr z);

  void print_tree(node_ptr z);
  void inorder_traversal(node_ptr z);
  void preorder_traversal(node_ptr z);
  void postorder_traversal(node_ptr z);
};

#endif
