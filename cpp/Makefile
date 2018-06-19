BOOST_TEST = -lboost_unit_test_framework

NAME = "AVLTree"
TEST_NAME = "AVLTreeUnitTest"

test:
	@echo "Compiling..."
	g++ -o $(TEST_NAME) $(TEST_NAME).cpp $(NAME).cpp $(BOOST_TEST)

run: test
	@echo "Running..."
	./$(TEST_NAME)

clean:
	@echo "Cleaning..."
	-rm $(TEST_NAME)
