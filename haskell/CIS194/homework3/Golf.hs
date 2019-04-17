module Golf where

-- The output of skips is a list of lists. The first list in the output should
-- be the same as the input list. The second list in the output should
-- contain every second element from the input list. . . and the nth list in
-- the output should contain every nth element from the input list.
-- For example:
-- skips "ABCD" == ["ABCD", "BD", "C", "D"]
-- skips "hello!" == ["hello!", "el!", "l!", "l", "o", "!"]
-- skips [1] == [[1]]
-- skips [True,False] == [[True,False], [False]]
-- skips [] == []
-- Note that the output should be the same length as the input.
takeEveryN :: Int -> [t] -> [t]
takeEveryN _ []         = []
takeEveryN n l@(x:xs)   = x:(takeEveryN n (drop n l))

everyOther :: Int -> [t] -> [t]
everyOther n l = takeEveryN n (drop (n-1) l)

skips :: [t] -> [[t]]
skips l = map (\(x, y) -> everyOther x y) $ zip [1..n] $ replicate n l
    where n = length l

-- A local maximum of a list is an element of the list which is strictly
-- greater than both the elements immediately before and after it. For
-- example, in the list [2,3,4,1,5], the only local maximum is 4, since
-- it is greater than the elements immediately before and after it (3 and
-- 1). 5 is not a local maximum since there is no element that comes
-- after it.
-- Write a function
-- localMaxima :: [Integer] -> [Integer]
-- which finds all the local maxima in the input list and returns them in
-- order. For example:
-- localMaxima [2,9,5,6,1] == [9,6]
-- localMaxima [2,3,4,1,5] == [4]
-- localMaxima [1,2,3,4,5] == []
localMaxima :: [Integer] -> [Integer]
localMaxima []              = []
localMaxima [_]             = []
localMaxima [_, _]          = []
localMaxima (x:y:z:rest)
    | x <= y && y >= z      = y:(localMaxima (y:z:rest))
    | otherwise             = localMaxima (y:z:rest)

-- Exercise 3 Histogram
-- For this task, write a function
-- histogram :: [Integer] -> String
-- which takes as input a list of Integers between 0 and 9 (inclusive),
-- and outputs a vertical histogram showing how many of each number
-- were in the input list. You may assume that the input list does not
-- contain any numbers less than zero or greater than 9 (that is, it does
-- not matter what your function does if the input does contain such
-- numbers). Your output must exactly match the output shown in the
-- examples below.
-- cis 194: homework 3 4
-- histogram [1,1,1,5] ==
-- *
-- *
-- * *
-- ==========
-- 0123456789
-- histogram [1,4,5,4,6,6,3,4,2,4,9] ==
-- *
-- *
-- * *
-- ****** *
-- ==========
-- 0123456789
-- Important note: If you type something like histogram [3,5] at
-- the ghci prompt, you should see something like this:
-- " * * \n==========\n0123456789\n"
-- This is a textual representation of the String output, including \n
-- escape sequences to indicate newline characters. To actually visualize
-- the histogram as in the examples above, use putStr, for example,
-- putStr (histogram [3,5]).
-- histogram :: [Integer] -> String
countHelper :: Integer -> [Integer] -> [Integer]
countHelper x l = (take xint l) ++ [l !! xint + 1] ++ (drop (xint+1) l)
    where xint = fromIntegral x

count :: [Integer] -> [Integer]
count = foldr countHelper $ replicate 10 0

mapFuncLargerThanN :: Integer -> Integer -> Char
mapFuncLargerThanN frequencyBound elemInArray
    | elemInArray >= frequencyBound     = '*'
    | otherwise                         = ' '

mapMapFuncLargerThanN :: Integer -> [Integer] -> [Char]
mapMapFuncLargerThanN n l = map (mapFuncLargerThanN n) l

histogramMatrix :: [Integer] -> [[Char]]
histogramMatrix l = [mapMapFuncLargerThanN number list | (list, number) <- zip (replicate (fromIntegral max) statistic) (reverse [1..max])]
    where   max         = maximum statistic
            statistic   = count l

joinWithSeparator :: [String] -> String -> String
joinWithSeparator [] _          = ""
joinWithSeparator [x] _         = x
joinWithSeparator (x:xs) sep    = x ++ sep ++ (joinWithSeparator xs sep)

histogram :: [Integer] -> String
histogram l = joinWithSeparator ((histogramMatrix l) ++ ["========="] ++ ["0123456789\n"]) "\n"