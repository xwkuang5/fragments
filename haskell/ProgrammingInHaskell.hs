-- 4.8.1
halve :: [a] -> ([a], [a])
halve xs = (take n xs, drop n xs)
  where n = length xs `div` 2

-- 4.8.2
third   xs              = head (tail (tail xs))
third'  xs              = xs !! 2
third'' (_:_:x:xs)      = x

-- 4.8.3
safetail    xs          = if null xs then [] else tail xs
safetail'   xs 
  | null xs             = []
  | otherwise           = tail xs
safetail''  []          = []
safetail''  (_:xs)      = xs

-- 9.11.1
-- Use the idea of swapping, but instead of swapping, we use inserting
-- Is there a more efficient way of doing this in Haskell?
insertAt :: (Num t1, Eq t1) => t -> t1 -> [t] -> [t]
insertAt e _ []     = [e]
insertAt e 0 xs     = e:xs
insertAt e n (x:xs) = x:(insertAt e (n-1) xs)

permsHelper :: (Num n, Enum n, Eq n) => [a] -> n -> [[a]]
permsHelper [x] 1    = [[x]]
permsHelper (x:xs) n = [insertAt x l permuted | l <- [0..(n-1)],
                                                permuted <- permsHelper xs (n-1)]
                                    
perms :: [a] -> [[a]]
perms [] = [[]]
perms xs = permsHelper xs $ length xs