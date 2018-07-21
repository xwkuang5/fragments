#define BOOST_CHECK_DYN_LINK
#define BOOST_CHECK_MODULE Simple testcases 2
#include <boost/test/unit_test.hpp>

#include "DisjointSet.hpp"

BOOST_AUTO_TEST_SUITE(suite1)

BOOST_AUTO_TEST_CASE(TestDisjointSet) {
  DisjointSet *set = new DisjointSet(6);

  for (int i = 0; i < 6; i++) {
    set->make_set(i);
  }

  BOOST_CHECK_EQUAL(set->find(0) == set->find(1), false);
  set->union_by_rank(0, 1);
  BOOST_CHECK_EQUAL(set->find(0) == set->find(1), true);

  BOOST_CHECK_EQUAL(set->find(2) == set->find(3), false);
  set->union_by_rank(2, 3);
  BOOST_CHECK_EQUAL(set->find(2) == set->find(3), true);

  BOOST_CHECK_EQUAL(set->find(0) == set->find(3), false);
  set->union_by_rank(0, 3);
  BOOST_CHECK_EQUAL(set->find(0) == set->find(3), true);
  BOOST_CHECK_EQUAL(set->find(1) == set->find(3), true);
  BOOST_CHECK_EQUAL(set->find(0) == set->find(2), true);
  BOOST_CHECK_EQUAL(set->find(1) == set->find(2), true);
}

BOOST_AUTO_TEST_SUITE_END()
