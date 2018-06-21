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
  AVLTreeNode(int key, int height, bool is_left, bool is_right,
              AVLTreeNode *parent, AVLTreeNode *left, AVLTreeNode *right);

  void print_node();
};

class AVLTree {
public:
  typedef AVLTreeNode node_type;
  typedef AVLTreeNode *node_ptr;
  typedef AVLTree tree_type;
  typedef AVLTree *tree_ptr;

  node_ptr root_;

  void fix_node(node_ptr z);
  void rotate_right(node_ptr z);
  void rotate_left(node_ptr z);
  void set_height_from_children(node_ptr z);
  node_ptr bst_insert(int key);
  node_ptr bst_delete(int key);

  AVLTree();
  AVLTree(int key);
  node_ptr insert_key(int key);
  void delete_key(int key);
  bool search_key(int key);
  bool is_empty();
  int get_height(node_ptr z);
  node_ptr get_root();
  node_ptr get_left_most();
  node_ptr get_right_most();
  node_ptr get_successor(node_ptr z);
  node_ptr get_predecessor(node_ptr z);

  void inorder_traversal(node_ptr z);
  void preorder_traversal(node_ptr z);
  void postorder_traversal(node_ptr z);

  class ForwardIterator {
  public:
    typedef ForwardIterator self_type;
    typedef std::forward_iterator_tag ForwardIterator_category;

    ForwardIterator();
    ForwardIterator(tree_ptr tptr, node_ptr nptr);
    ForwardIterator(const self_type &rhs);
    ~ForwardIterator();

    self_type operator++();
    self_type &operator++(int dummy);

    node_ptr operator->();
    node_type operator*();

    bool operator==(const self_type &rhs);
    bool operator!=(const self_type &rhs);
    void operator=(const self_type &rhs);

  private:
    tree_ptr _tree_ptr;
    node_ptr _node_ptr;
  };

  class ReverseIterator {
  public:
    typedef ReverseIterator self_type;

    ReverseIterator();
    ReverseIterator(tree_ptr _tptr, node_ptr _nptr);
    ReverseIterator(const self_type &rhs);
    ~ReverseIterator();

    self_type operator++();
    self_type &operator++(int dymmy);

    node_ptr operator->();
    node_type operator*();

    bool operator==(const ReverseIterator &rhs);
    bool operator!=(const ReverseIterator &rhs);
    void operator=(const ReverseIterator &rhs);

  private:
    tree_ptr _tree_ptr;
    node_ptr _node_ptr;
  };

  ForwardIterator begin();
  ForwardIterator end();

  ReverseIterator rbegin();
  ReverseIterator rend();
};

#endif
