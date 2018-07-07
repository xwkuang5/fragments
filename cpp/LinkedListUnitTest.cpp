#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Simple testcases 2
#include <boost/test/unit_test.hpp>

#include "LinkedList.hpp"

BOOST_AUTO_TEST_SUITE(suite1)

BOOST_AUTO_TEST_CASE(TestLinkedListInsertKey) {
  auto linked_list = new LinkedList<int, int>();

  linked_list->insert_back(new int(3), new int(3));
  linked_list->insert_front(new int(2), new int(2));
  linked_list->insert_back(new int(4), new int(4));
  linked_list->insert_back(new int(5), new int(5));
  linked_list->insert_front(new int(1), new int(1));
  linked_list->insert_back(new int(6), new int(6));
  linked_list->insert_back(new int(7), new int(7));
  linked_list->insert_front(new int(0), new int(0));

  int arr[8] = {0, 1, 2, 3, 4, 5, 6, 7};

  int i = 0;
  for (auto iter = linked_list->begin(); iter != linked_list->end(); iter++) {
    BOOST_CHECK_EQUAL(*(iter->obj_), arr[i++]);
  }
}

BOOST_AUTO_TEST_CASE(TestLinkedListSearchKey) {
  auto linked_list = new LinkedList<int, int>();

  linked_list->insert_back(new int(3), new int(3));
  linked_list->insert_front(new int(2), new int(2));
  linked_list->insert_back(new int(4), new int(4));

  BOOST_CHECK_EQUAL(linked_list->search(3), true);
  BOOST_CHECK_EQUAL(linked_list->search(4), true);
  BOOST_CHECK_EQUAL(linked_list->search(2), true);
  BOOST_CHECK_EQUAL(linked_list->search(1), false);
  BOOST_CHECK_EQUAL(linked_list->search(5), false);
}

BOOST_AUTO_TEST_CASE(TestLinkedListRemoveKey) {
  auto linked_list = new LinkedList<int, int>();

  linked_list->insert_back(new int(3), new int(3));
  linked_list->insert_front(new int(2), new int(2));
  linked_list->insert_back(new int(4), new int(4));

  BOOST_CHECK_EQUAL(linked_list->search(3), true);
  linked_list->remove(3);
  BOOST_CHECK_EQUAL(linked_list->search(3), false);
  BOOST_CHECK_EQUAL(linked_list->search(2), true);
  linked_list->remove(2);
  BOOST_CHECK_EQUAL(linked_list->search(2), false);
  BOOST_CHECK_EQUAL(linked_list->search(4), true);
  linked_list->remove(4);
  BOOST_CHECK_EQUAL(linked_list->search(4), false);
  BOOST_CHECK_EQUAL(linked_list->is_empty(), true);
}

BOOST_AUTO_TEST_SUITE_END()
