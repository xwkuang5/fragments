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
    | a `mod` 2 == 0    True
    | otherwise         True

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


