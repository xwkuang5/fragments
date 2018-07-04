#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Simple testcases 2
#include <boost/test/unit_test.hpp>

#include "SkipList.hpp"

BOOST_AUTO_TEST_SUITE(suite1)


BOOST_AUTO_TEST_CASE(TestSkipListInsertKey) {
  int* max = new int(100);
  SkipList<int, int>* skip_list = new SkipList<int, int>(0.5, 16, max);

  auto key1 = new int(1);
  auto obj1 = new int(1);
  auto key2 = new int(2);
  auto obj2 = new int(2);
  auto key3 = new int(3);
  auto obj3 = new int(3);
  auto key4 = new int(4);
  auto obj4 = new int(4);
  auto key5 = new int(5);
  auto obj5 = new int(5);
  auto key6 = new int(6);
  auto obj6 = new int(6);
  auto key7 = new int(7);
  auto obj7 = new int(7);
  auto key8 = new int(8);
  auto obj8 = new int(8);

  BOOST_CHECK_EQUAL(skip_list->insert(key6, obj6), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key1, obj1), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key2, obj2), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key4, obj4), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key8, obj8), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key5, obj5), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key3, obj3), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key7, obj7), true);

  int arr[8] = {1, 2, 3, 4, 5, 6, 7, 8};

  int i = 0;
  for (SkipList<int, int>::iterator iter = skip_list->begin(); iter != skip_list->end(); ++iter) {
    BOOST_CHECK_EQUAL(*(iter->get_obj()), arr[i]);
    i += 1;
  }
}

BOOST_AUTO_TEST_CASE(TestSkipListSearchKey) {
  int* max = new int(100);
  SkipList<int, int>* skip_list = new SkipList<int, int>(0.5, 16, max);

  auto key1 = new int(1);
  auto obj1 = new int(1);
  auto key2 = new int(2);
  auto obj2 = new int(2);
  auto key3 = new int(3);
  auto obj3 = new int(3);
  auto key4 = new int(4);
  auto obj4 = new int(4);
  auto key5 = new int(5);
  auto obj5 = new int(5);
  auto key6 = new int(6);
  auto obj6 = new int(6);
  auto key7 = new int(7);
  auto obj7 = new int(7);
  auto key8 = new int(8);
  auto obj8 = new int(8);

  BOOST_CHECK_EQUAL(skip_list->insert(key6, obj6), true);
  BOOST_CHECK_EQUAL(skip_list->search(key6), obj6);
  BOOST_CHECK_EQUAL(skip_list->insert(key1, obj1), true);
  BOOST_CHECK_EQUAL(skip_list->search(key1), obj1);
  BOOST_CHECK_EQUAL(skip_list->insert(key2, obj2), true);
  BOOST_CHECK_EQUAL(skip_list->search(key2), obj2);
  BOOST_CHECK_EQUAL(skip_list->insert(key4, obj4), true);
  BOOST_CHECK_EQUAL(skip_list->search(key4), obj4);
  BOOST_CHECK_EQUAL(skip_list->insert(key8, obj8), true);
  BOOST_CHECK_EQUAL(skip_list->search(key8), obj8);
  BOOST_CHECK_EQUAL(skip_list->insert(key5, obj5), true);
  BOOST_CHECK_EQUAL(skip_list->search(key5), obj5);
  BOOST_CHECK_EQUAL(skip_list->insert(key3, obj3), true);
  BOOST_CHECK_EQUAL(skip_list->search(key3), obj3);
  BOOST_CHECK_EQUAL(skip_list->insert(key7, obj7), true);
  BOOST_CHECK_EQUAL(skip_list->search(key7), obj7);
}

BOOST_AUTO_TEST_CASE(TestSkipListRemoveKey) {
  int* max = new int(100);
  SkipList<int, int>* skip_list = new SkipList<int, int>(0.5, 16, max);

  auto key1 = new int(1);
  auto obj1 = new int(1);
  auto key2 = new int(2);
  auto obj2 = new int(2);
  auto key3 = new int(3);
  auto obj3 = new int(3);
  auto key4 = new int(4);
  auto obj4 = new int(4);
  auto key5 = new int(5);
  auto obj5 = new int(5);
  auto key6 = new int(6);
  auto obj6 = new int(6);
  auto key7 = new int(7);
  auto obj7 = new int(7);
  auto key8 = new int(8);
  auto obj8 = new int(8);

  auto test_key = new int(20);

  BOOST_CHECK_EQUAL(skip_list->insert(key6, obj6), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key1, obj1), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key2, obj2), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key4, obj4), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key8, obj8), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key5, obj5), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key3, obj3), true);
  BOOST_CHECK_EQUAL(skip_list->insert(key7, obj7), true);

  BOOST_CHECK_EQUAL(skip_list->remove(test_key), false);
  BOOST_CHECK_EQUAL(skip_list->remove(key1), true);
  BOOST_CHECK_EQUAL(skip_list->remove(key3), true);

  int arr[6] = {2, 4, 5, 6, 7, 8};
  int i = 0;
  for (SkipList<int, int>::iterator iter = skip_list->begin(); iter != skip_list->end(); ++iter) {
    BOOST_CHECK_EQUAL(*(iter->get_obj()), arr[i]);
    i += 1;
  }
}

BOOST_AUTO_TEST_SUITE_END()
