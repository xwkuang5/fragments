/**
 * Compile command: g++ -o test AVLTreeUnitTest.cpp -lboost_unit_test_framework
 */


#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Simple testcases 2
#include <boost/test/unit_test.hpp>

#include "AVLTree.hpp"

BOOST_AUTO_TEST_SUITE(suite1)

BOOST_AUTO_TEST_CASE(testAVLInsertKey) {
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
}

BOOST_AUTO_TEST_SUITE_END()
