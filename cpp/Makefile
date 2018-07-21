BOOST_TEST = -lboost_unit_test_framework
CPP_VERSION = -std=c++14

LINKED_LIST_TEST_NAME = "LinkedListUnitTest"

DISJOINT_SET_TEST_NAME = "DisjointSetUnitTest"

AVL_NAME = "AVLTree"
AVL_TEST_NAME = "AVLTreeUnitTest"

SKIP_LIST_TEST_NAME = "SkipListUnitTest"

LinkedListTest:
	@echo "Compiling..."
	g++ -o $(LINKED_LIST_TEST_NAME) $(LINKED_LIST_TEST_NAME).cpp $(BOOST_TEST) $(CPP_VERSION)
	@echo "Running..."
	./$(LINKED_LIST_TEST_NAME)

DisjointSetTest:
	@echo "Compiling..."
	g++ -o $(DISJOINT_SET_TEST_NAME) $(DISJOINT_SET_TEST_NAME).cpp $(BOOST_TEST) $(CPP_VERSION)
	@echo "Running..."
	./$(DISJOINT_SET_TEST_NAME)

AVLTest:
	@echo "Compiling..."
	g++ -o $(AVL_TEST_NAME) $(AVL_TEST_NAME).cpp $(AVL_NAME).cpp $(BOOST_TEST) $(CPP_VERSION)
	@echo "Running..."
	./$(AVL_TEST_NAME)

SkipListTest:
	@echo "Compiling"
	g++ -o $(SKIP_LIST_TEST_NAME) $(SKIP_LIST_TEST_NAME).cpp $(BOOST_TEST) $(CPP_VERSION)
	@echo "Running..."
	./$(SKIP_LIST_TEST_NAME)

clean:
	@echo "Cleaning..." 
	-rm $(LINKED_LIST_TEST_NAME)
	-rm $(DISJOINT_SET_TEST_NAME)
	-rm $(AVL_TEST_NAME)
	-rm $(SKIP_LIST_TEST_NAME)
