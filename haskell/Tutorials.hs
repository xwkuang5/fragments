quicksort :: (Ord a) => [a] -> [a]
quicksort [] = []
quicksort (x:xs) = 
    let smallersorted = quicksort [a | a <- xs, a <= x]
        biggersorted = quicksort [a | a <- xs, a > x]
    in  smallersorted ++ [x] ++ biggersorted

data BinarySearchTree a = EmptyBinarySearchTree | Node a (BinarySearchTree a) (BinarySearchTree a) deriving (Show, Read, Eq)

binarySearchTreeInsert :: (Ord a) => a -> BinarySearchTree a -> BinarySearchTree a
binarySearchTreeInsert a EmptyBinarySearchTree = Node a EmptyBinarySearchTree EmptyBinarySearchTree
binarySearchTreeInsert a (Node root left right)
    | a == root = Node a left right
    | a < root  = Node root (binarySearchTreeInsert a left) right
    | a > root  = Node root left (binarySearchTreeInsert a right)

binarySearchTreeElem :: (Ord a) => a -> BinarySearchTree a -> Bool
binarySearchTreeElem a EmptyBinarySearchTree = False
binarySearchTreeElem a (Node root left right)
    | a == root = True
    | a < root  = binarySearchTreeElem a left
    | a > root  = binarySearchTreeElem a right

buildBinarySearchTreeFromList :: (Ord a) => [a] -> BinarySearchTree a
buildBinarySearchTreeFromList []    = EmptyBinarySearchTree
buildBinarySearchTreeFromList list  = foldr binarySearchTreeInsert EmptyBinarySearchTree list  
