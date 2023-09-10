-- Problem 1
multipleOfThreeAndFive :: (Integral a) => a -> Bool
multipleOfThreeAndFive a 
    | a `mod` 3 == 0    = True 
    | a `mod` 5 == 0    = True
    | otherwise         = False

-- result = sum [x | x <- [1..1000], multipleOfThreeAndFive x]
-- result = sum $ filter multipleOfThreeAndFive [1..999]

-- Problem 2
even :: (Integral a) => a -> Bool
even a  
    | a `mod` 2 == 0    = True
    | otherwise         = False

-- the use of thunk
-- fibs                         = 0 : 1 : <thunk1>
-- tail fibs                    = 1 : <thunk1>
-- zipWith (+) fibs (tail fibs) = <thunk1>

-- fibs                         = 0 : 1 : 1 : <thunk2>
-- tail fibs                    = 1 : 1 : <thunk2>
-- zipWith (+) fibs (tail fibs) = 1 : <thunk2>

-- fibs                         = 0 : 1 : 1 : 2 : <thunk3>
-- tail fibs                    = 1 : 1 : 2 : <thunk3>
-- zipWith (+) fibs (tail fibs) = 1 : 2 : <thunk3>
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- result = sum $ takeWhile (<4000000) $ filter even fibs

-- Problem 3
leastPrime :: (Integral a) => a -> [a]
-- Only need to check until sqrt a, but using round does not work for type checking
-- Use take 1 because take 1 [] = []
leastPrime a = take 1 $ filter (\x -> (a `mod` x) == 0) [2..a-1]

findPrimeFactors :: (Integral a) => a -> [a]
findPrimeFactors 1  = []
findPrimeFactors n
    | factors == [] = [n]
    | otherwise     = factors ++ findPrimeFactors (n `div` (head factors))
    where factors = leastPrime n

findLargestPrimeFactors :: (Integral a) => a -> a
findLargestPrimeFactors a = (last . findPrimeFactors) a

-- Problem 4
reverseNumber :: (Integral a) => a -> a -> a
reverseNumber 0 y = y
reverseNumber x y = reverseNumber q (r + y * 10)
    where (q, r) = x `quotRem` 10

isPalindrome :: (Integral a) => a -> Bool
isPalindrome x = reverseNumber x 0 == x

cartesianProduct :: (Integral a) => [a] -> [a] -> [(a, a)]
cartesianProduct xs ys = [(x, y) | x <- xs, y <- ys]

tupleProduct :: (Integral a) => (a, a) -> a
tupleProduct (x, y) = x * y

largestPalindromProduct :: (Integral a) => a -> a
largestPalindromProduct n = foldl1 max $ filter isPalindrome $ map tupleProduct $ cartesianProduct list list
    where list = [1..((^) 10 n - 1)]
