/**
 * Compile command: g++ -o test AVLTreeUnitTest.cpp -lboost_unit_test_framework
 */

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Simple testcases 2
#include <boost/test/unit_test.hpp>

#include "AVLTree.hpp"

BOOST_AUTO_TEST_SUITE(suite1)

/**
 * The validity of the test all depends on the correctness of insert_key
 * If the test fails for insert_key, then all tests should be considered
 * failed.
 */

BOOST_AUTO_TEST_CASE(TestAVLInsertKey) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);

  // test double rotation (right heavy)
  BOOST_CHECK_EQUAL(tmp->left_->key_, 15);
  BOOST_CHECK_EQUAL(tmp->right_->key_, 20);
  BOOST_CHECK_EQUAL(tmp->height_, 1);
  BOOST_CHECK_EQUAL(tmp->parent_->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_root()->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_root()->height_, 2);

  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);

  // test single right rotation
  BOOST_CHECK_EQUAL(tmp->parent_->key_, 4);
  BOOST_CHECK_EQUAL(tmp->key_, 0);
  BOOST_CHECK_EQUAL(tmp->is_left_, true);
  BOOST_CHECK_EQUAL(tmp->is_right_, false);
  BOOST_CHECK_EQUAL(tree->get_root()->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_root()->height_, 2);

  tmp = tree->insert_key(1);
  tmp = tree->insert_key(2);

  // test single left rotation
  BOOST_CHECK_EQUAL(tmp->parent_->key_, 1);
  BOOST_CHECK_EQUAL(tmp->key_, 2);
  BOOST_CHECK_EQUAL(tmp->is_left_, false);
  BOOST_CHECK_EQUAL(tmp->is_right_, true);
  BOOST_CHECK_EQUAL(tree->get_root()->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_root()->height_, 3);

  // test double rotation (left heavy)
  tmp = tree->insert_key(3);

  BOOST_CHECK_EQUAL(tmp->parent_->key_, 4);
  BOOST_CHECK_EQUAL(tmp->parent_->parent_->key_, 2);
  BOOST_CHECK_EQUAL(tmp->key_, 3);
  BOOST_CHECK_EQUAL(tmp->is_left_, true);
  BOOST_CHECK_EQUAL(tmp->is_right_, false);
  BOOST_CHECK_EQUAL(tree->get_root()->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_root()->height_, 3);
}

BOOST_AUTO_TEST_CASE(TestAVLGetPredecessor) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tree->insert_key(15);
  tree->insert_key(18);
  tree->insert_key(4);
  tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);

  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 18);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 15);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 10);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 6);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 4);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 2);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 1);
  tmp = tree->get_predecessor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 0);
}

BOOST_AUTO_TEST_CASE(TestAVLGetSuccessor) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);
  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);

  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 1);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 2);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 4);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 6);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 10);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 15);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 18);
  tmp = tree->get_successor(tmp);
  BOOST_CHECK_EQUAL(tmp->key_, 20);
}

BOOST_AUTO_TEST_CASE(TestAVLDeleteKey) {
  AVLTree *tree = new AVLTree(10);

  tree->insert_key(6);
  tree->insert_key(20);
  tree->insert_key(15);
  tree->insert_key(18);
  tree->insert_key(4);
  tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);
  tree->insert_key(3);
  tree->insert_key(9);
  tree->insert_key(8);
  tree->insert_key(7);

  // test simple bst_delete
  tree->delete_key(10);
  AVLTree::node_ptr root = tree->get_root();
  BOOST_CHECK_EQUAL(root->key_, 4);
  BOOST_CHECK_EQUAL(root->right_->key_, 15);
  BOOST_CHECK_EQUAL(root->right_->right_->key_, 18);
  BOOST_CHECK_EQUAL(root->right_->left_->key_, 8);

  // test bst_delete followed by rotation
  tree->delete_key(20);
  BOOST_CHECK_EQUAL(root->key_, 4);
  BOOST_CHECK_EQUAL(root->right_->key_, 8);
  BOOST_CHECK_EQUAL(root->right_->right_->key_, 15);
  BOOST_CHECK_EQUAL(root->right_->left_->key_, 6);

  // test bst_delete root followed by rotation
  tree->delete_key(4);
  BOOST_CHECK_EQUAL(root->key_, 6);
  BOOST_CHECK_EQUAL(root->right_->key_, 8);
  BOOST_CHECK_EQUAL(root->right_->right_->key_, 15);
  BOOST_CHECK_EQUAL(root->right_->left_->key_, 7);
}

BOOST_AUTO_TEST_CASE(TestAVLSearchKey) {
  AVLTree *tree = new AVLTree(10);

  tree->insert_key(6);
  tree->insert_key(20);
  tree->insert_key(15);
  tree->insert_key(18);
  tree->insert_key(4);
  tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);
  tree->insert_key(3);
  tree->insert_key(9);
  tree->insert_key(8);
  tree->insert_key(7);

  BOOST_CHECK_EQUAL(tree->search_key(0), true);
  BOOST_CHECK_EQUAL(tree->search_key(1), true);
  BOOST_CHECK_EQUAL(tree->search_key(2), true);
  BOOST_CHECK_EQUAL(tree->search_key(3), true);
  BOOST_CHECK_EQUAL(tree->search_key(4), true);
  BOOST_CHECK_EQUAL(tree->search_key(5), false);
  BOOST_CHECK_EQUAL(tree->search_key(6), true);
  BOOST_CHECK_EQUAL(tree->search_key(7), true);
  BOOST_CHECK_EQUAL(tree->search_key(8), true);
  BOOST_CHECK_EQUAL(tree->search_key(9), true);
  BOOST_CHECK_EQUAL(tree->search_key(10), true);
  BOOST_CHECK_EQUAL(tree->search_key(11), false);
  BOOST_CHECK_EQUAL(tree->search_key(12), false);
  BOOST_CHECK_EQUAL(tree->search_key(13), false);
  BOOST_CHECK_EQUAL(tree->search_key(14), false);
  BOOST_CHECK_EQUAL(tree->search_key(15), true);
  BOOST_CHECK_EQUAL(tree->search_key(16), false);
  BOOST_CHECK_EQUAL(tree->search_key(17), false);
  BOOST_CHECK_EQUAL(tree->search_key(18), true);
  BOOST_CHECK_EQUAL(tree->search_key(19), false);
  BOOST_CHECK_EQUAL(tree->search_key(20), true);
}

BOOST_AUTO_TEST_CASE(TestAVLForwardIterator) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);
  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);

  AVLTree::ForwardIterator iter = tree->begin();
  BOOST_CHECK_EQUAL(iter->key_, 0);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 1);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 2);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 4);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 6);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 10);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 15);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 18);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 20);
  iter++;
  BOOST_CHECK_EQUAL(iter == tree->end(), true);
}

BOOST_AUTO_TEST_CASE(TestAVLReverseIterator) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);
  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);
  AVLTree::ReverseIterator iter = tree->rbegin();
  BOOST_CHECK_EQUAL(iter->key_, 20);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 18);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 15);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 10);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 6);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 4);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 2);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 1);
  iter++;
  BOOST_CHECK_EQUAL(iter->key_, 0);
  iter++;
  BOOST_CHECK_EQUAL(iter == tree->rend(), true);
}

BOOST_AUTO_TEST_CASE(TestAVLNumberNodesInSubtree) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);
  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);

  BOOST_CHECK_EQUAL(tree->root_->num_left_, 5);
  BOOST_CHECK_EQUAL(tree->root_->num_right_, 3);
  BOOST_CHECK_EQUAL(tree->root_->left_->num_left_, 3);
  BOOST_CHECK_EQUAL(tree->root_->left_->num_right_, 1);
  BOOST_CHECK_EQUAL(tree->root_->right_->num_left_, 1);
  BOOST_CHECK_EQUAL(tree->root_->right_->num_right_, 1);
  BOOST_CHECK_EQUAL(tmp->parent_->num_left_, 1);
  BOOST_CHECK_EQUAL(tmp->parent_->num_right_, 1);
  BOOST_CHECK_EQUAL(tmp->num_left_, 0);
  BOOST_CHECK_EQUAL(tmp->num_right_, 0);
}

BOOST_AUTO_TEST_CASE(TestAVLGetIthNode) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);
  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);

  AVLTree::node_ptr root = tree->get_root();

  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 1)->key_, 0);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 2)->key_, 1);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 3)->key_, 2);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 4)->key_, 4);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 5)->key_, 6);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 6)->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 7)->key_, 15);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 8)->key_, 18);
  BOOST_CHECK_EQUAL(tree->get_ith_node(root, 9)->key_, 20);
}

BOOST_AUTO_TEST_CASE(TestAVLGetIthSuccessor) {
  AVLTree *tree = new AVLTree(10);
  AVLTree ::node_ptr tmp;
  tmp = tree->insert_key(6);
  tmp = tree->insert_key(20);
  tmp = tree->insert_key(15);
  tmp = tree->insert_key(18);
  tmp = tree->insert_key(4);
  tmp = tree->insert_key(0);
  tree->insert_key(1);
  tree->insert_key(2);

  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 0)->key_, 0);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 1)->key_, 1);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 2)->key_, 2);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 3)->key_, 4);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 4)->key_, 6);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 5)->key_, 10);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 6)->key_, 15);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 7)->key_, 18);
  BOOST_CHECK_EQUAL(tree->get_ith_successor(tmp, 8)->key_, 20);
}

BOOST_AUTO_TEST_SUITE_END()
