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

