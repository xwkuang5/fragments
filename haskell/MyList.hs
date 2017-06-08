module MyList
( myLast
, myButLast
, elementAt
, myLength
, myReverse
, isPalindrome
, flattern
, compress
, pack
, encode
, encodeModified
, decodeModified
) where

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

-- Problem 9
pack :: (Eq a) => [a] -> [[a]]
pack []     = []
pack [x]    = [[x]]
pack (x:xs) = if elem x (head (pack xs))
              then (x:(head (pack xs))):(tail (pack xs))
              else [x]:(pack xs)

-- Problem 10
encode :: (Eq a) => [a] -> [(Int, a)]
encode = encode_help . pack
    where encode_help [[]]   = error "No encoding for empty list!"
          encode_help [x]    = [(sum (map (\_ -> 1) x), head x)]
          encode_help (x:xs) = (sum (map (\_ -> 1) x), head x):(encode_help xs) 

encode' x = (encode_help' . pack) x
    where encode_help' = foldr (\x acc -> (length x, head x):acc) []

-- Problem 11
data ListItem a = Single a | Multiple Int a
    deriving (Show)
encodeModified :: (Eq a) => [a] -> [ListItem a]
encodeModified = encodeModified_help . encode
    where encodeModified_help [(1, a)] = [Single a]
          encodeModified_help [(n, a)] = [Multiple n a]
          encodeModified_help ((1, a):xs) = (Single a):(encodeModified_help xs)
          encodeModified_help ((n, a):xs) = (Multiple n a):(encodeModified_help xs)

-- Problem 12
decodeModified :: [ListItem a] -> [a]
decodeModified [Single a]            = [a]
decodeModified [Multiple n a]        = map (\_ -> a) [1..n]
decodeModified ((Single x):xs)       = x:(decodeModified xs)
decodeModified ((Multiple n x):xs)   = (map (\_ -> x) [1..n]) ++ (decodeModified xs)

-- Problem 13

