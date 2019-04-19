-- Excercise 1
fun1 :: [Integer] -> Integer
fun1 = foldr (*) 1 . map (*2) . filter even

helper :: Integer -> Integer
helper 1 = 0
helper n | even n       = n `div` 2
         | otherwise    = 3 * n + 1

fun2 :: Integer -> Integer
fun2 = sum . filter even . takeWhile (/=1) . iterate helper


-- Excercise 1
data Tree a = Leaf
            | Node Integer (Tree a) a (Tree a)
    deriving (Show, Eq)

height :: Tree a -> Integer
height Leaf             = -1
height (Node n _ _ _)   = n

insert :: a -> Tree a -> Tree a
insert x Leaf = Node 0 Leaf x Leaf
insert x (Node _ left root right) = Node newHeight newLeft root newRight
    where
        leftHeight = height left
        rightHeight = height right
        newLeft
            | leftHeight <= rightHeight = insert x left
            | otherwise                 = left
        newRight
            | leftHeight <= rightHeight = right
            | otherwise                 = insert x right
        newHeight = 1 + (max (height newLeft) (height newRight))

foldTree :: [a] -> Tree a
foldTree = foldr insert Leaf


-- Excercise 3
xor :: [Bool] -> Bool
xor = odd . foldr (\x y -> if x then (y+1) else y) 0

map' :: (a -> b) -> [a] -> [b]
map' f = foldr (\x y -> (f x):y) []

myFoldl :: (a -> b -> a) -> a -> [b] -> a
myFoldl f init l = foldr (\a b -> f b a) init $ reverse l

-- Excercise 4
-- This implementation is very very very inefficient
filterFunc :: Integer -> Integer -> Bool
filterFunc n t = foldr (\(x,y) z -> z && (t /= x+y+2*x*y)) True [(x,y) | x <- [1..n], y <- [1..n]]

sieveSundaram :: Integer -> [Integer]
sieveSundaram n = map (+1) . map (*2) . filter (filterFunc n) $ [1..n]