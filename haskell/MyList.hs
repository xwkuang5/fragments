-- Problem 1
myLast :: [a] -> a
myLast [] = error "No end for empty lists!"
myLast [x] = x
myLast (_:xs) = myLast xs

myLast' = last
myLast'' = head . reverse

-- Problem 2
myButLast :: [a] -> a
myButLast [] = error "No last but one element for empty lists!"
myButLast [x] = error "No last but one element for singleton lists!"
myButLast [x,_] = x
myButLast (_:xs) = myButLast xs

myButLast' = last . init 

myButLast'' = take 1 . reverse

-- Problem 3
elementAt :: [a] -> Int -> a
elementAt list i = list !! (i - 1)

elementAt' (x:_) 1 = x
elementAt' [] _ = error "Index out of bound!"
elementAt' (_:xs) i
    | i < 1     = error "Index out of bound!"
    | otherwise = elementAt' xs (i - 1)

-- Problem 4
myLength :: [a] -> Int
myLength []     = 0
myLength [_]    = 1
myLength (_:xs) = myLength xs + 1 

myLength' list = myLengthAcc list 0
    where
        myLengthAcc [] i     = i
        myLengthAcc [_] i    = i + 1
        myLengthAcc (_:xs) i = myLengthAcc xs 1

myLength''  :: [a] -> Int
myLength''  = foldl (\n _ -> n + 1) 0
myLength''' :: [a] -> Int
myLength''' = foldr (\_ n -> n + 1) 0

myLength'''' :: [a] -> Int
myLength'''' = sum . map (\_ -> 1)

myLength''''' list = sum [1 | _ <- list]

-- Problem 5
myReverse :: [a] -> [a]
myReverse []     = []
myReverse [x]    = [x]
myReverse (x:xs) = myReverse xs ++ [x]

-- Problem 6
isPalindrome :: (Eq a) => [a] -> Bool
isPalindrome []     = True
isPalindrome [_]    = True
isPalindrome (x:xs) = (x == (last xs)) && (isPalindrome $ init xs)

-- Problem 7
data NestedList a   = Elem a | List [NestedList a]
flattern :: NestedList a -> [a]
flattern (Elem x)   = [x]
flattern (List xs)  = foldr (++) [] $ map flattern xs

flattern' :: NestedList a -> [a]
flattern' (Elem x)  = [x]
flattern' (List xs) = foldl (++) [] $ map flattern xs

-- Problem 8
compress :: (Eq a) => [a] -> [a]
compress []     = []
compress [x]    = [x]
compress (x:xs) = [x] ++ compress (filter (/=x) xs)

compress' :: (Eq a) => [a] -> [a]
compress' list  = foldl accFunc [] list
    where
        accFunc :: (Eq a) => [a] -> a -> [a]
        accFunc [] x            = [x]
        accFunc list x
            | (last list) == x  = list 
            | (last list) /= x  = list ++ [x]

-- Problem 9
pack :: (Eq a) => [a] -> [[a]]
pack []     = []
pack [x]    = [[x]]
pack (x:xs) = if elem x (head (pack xs))
              then (x:(head (pack xs))):(tail (pack xs))
              else [x]:(pack xs)

-- Problem 10
encode :: (Eq a) => [a] -> [(Int, a)]
encode = encodeHelper . pack
    where encodeHelper [[]]   = error "No encoding for empty list!"
          encodeHelper [x]    = [(sum (map (\_ -> 1) x), head x)]
          encodeHelper (x:xs) = (sum (map (\_ -> 1) x), head x):(encodeHelper xs) 

encode' x = (encodeHelper' . pack) x
    where encodeHelper' = foldr (\x acc -> (length x, head x):acc) []

-- Problem 11
data ListItem a = Single a | Multiple Int a deriving (Show)
encodeModified :: (Eq a) => [a] -> [ListItem a]
encodeModified = encodeModifiedHelper . encode
    where encodeModifiedHelper [(1, a)] = [Single a]
          encodeModifiedHelper [(n, a)] = [Multiple n a]
          encodeModifiedHelper ((1, a):xs) = (Single a):(encodeModifiedHelper xs)
          encodeModifiedHelper ((n, a):xs) = (Multiple n a):(encodeModifiedHelper xs)

-- Problem 12
decodeModified :: [ListItem a] -> [a]
decodeModified [Single a]            = [a]
decodeModified [Multiple n a]        = map (\_ -> a) [1..n]
decodeModified ((Single x):xs)       = x:(decodeModified xs)
decodeModified ((Multiple n x):xs)   = (map (\_ -> x) [1..n]) ++ (decodeModified xs)

-- Problem 13
encodeDirect :: (Eq a) => [a] -> [ListItem a]
encodeDirect = map encodeDirectHelper . encode'
    where
        encode' :: (Eq a) => [a] -> [(Int, a)]
        encode' = foldr encodeHelper []
            where
                encodeHelper :: (Eq a) => a -> [(Int,a)] -> [(Int,a)]
                encodeHelper x [] = [(1,x)]
                encodeHelper x ((a,b):ys)
                    | x == b = (a+1,b):ys
                    | x /= b = (1,x):(a,b):ys
        encodeDirectHelper :: (Eq a) => (Int,a) -> ListItem a
        encodeDirectHelper (1, a) = Single a
        encodeDirectHelper (n, a) = Multiple n a

--Problem 14
dupli :: [a] -> [a]
dupli = foldr dupliHelper [] 
    where
        dupliHelper :: a -> [a] -> [a]
        dupliHelper a [] = [a, a]
        dupliHelper a x = a:a:x

dupli' :: [a] -> [a]
dupli' [] = []
dupli' (x:xs) = x:x:(dupli' xs)

--Problem 15
repli :: [a] -> Int -> [a]
repli list n = foldr (repliHelper n) [] list
    where
        repliHelper :: (Eq n, Num n) => n -> a -> [a] -> [a]
        repliHelper 0 _ list = list
        repliHelper n a list = a:(repliHelper (n-1) a list)

--Problem 16
dropEvery :: [a] -> Int -> [a]
dropEvery list n = dropEveryHelper list n n
    where
        dropEveryHelper :: [a] -> Int -> Int -> [a]
        dropEveryHelper [] _ _ = []
        dropEveryHelper (x:xs) n 0 = dropEveryHelper xs n n
        dropEveryHelper (x:xs) n m = x:(dropEveryHelper xs n (m-1))

--Problem 17
split :: [a] -> Int -> ([a], [a])
split xs n = (take n xs, drop n xs)

--Problem 18
slice :: [a] -> Int -> Int -> [a]
slice list i j = take (j-i+1) . drop (i-1) $ list

--Problem 19
--If n < 0, convert the problem to the equivalent problem for n > 0 by adding the list's length to n.
rotate :: [a] -> Int -> [a]
rotate [] _ = []
rotate xs 0 = xs
rotate (y@x:xs) n
    | n > 0 = rotate (xs ++ [x]) (n-1)
    | n < 0 = rotate (x:xs) (length (x:xs) + n)

--Problem 20
removeAt :: Int -> [a] -> [a]
removeAt _ [] = []
removeAt 1 (x:xs) = xs
removeAt n (x:xs)
    | n > 0 = x:(removeAt (n-1) xs)
    | n < 0 = removeAt (length (x:xs) + n + 1) (x:xs)
