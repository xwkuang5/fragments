import Data.Char

-- The Caesar cipher
shift :: Char -> Int -> Char
shift x n
    | isLetter x = intToChar $ (charToInt (Data.Char.toLower x) + n) `mod` 26
    | otherwise  = x
        where intToChar n = chr $ ord 'a' + n
              charToInt c = ord c - ord 'a'  

caesarEncode :: [Char] -> Int -> [Char]
caesarEncode xs n = [shift x n | x <- xs]

table :: [Float]
table = [8.1, 1.5, 2.8, 4.2, 12.7, 2.2, 2.0, 6.1, 7.0,
         0.2, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0,
         6.3, 9.0, 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]

chiSquareStatistic :: [Float] -> [Float] -> Float
chiSquareStatistic observed expected = sum [((o-e)^2)/e | (o, e) <- zip observed expected]

rotate xs n = drop n xs ++ take n xs

pairReducer :: (Float, Int) -> (Float, Int) -> (Float, Int)
pairReducer a b
    | fst a < fst b = a
    | otherwise     = b

argmin :: [Float] -> Int
argmin xs = snd $ foldl pairReducer (1000000, -1) [tuple | tuple <- zip xs [0..(length xs - 1)]]

percentage :: Int -> Int -> Float
percentage a b = fromIntegral a / fromIntegral b * 100

count :: Char -> [Char] -> Int
count x xs = length $ filter (== x) xs

frequencyTable :: [Char] -> [Float]
frequencyTable xs = [percentage (count x xs) total | x <- ['a'..'z']]
    where total = length $ filter isLetter xs

caesarDecode :: [Char] -> [Char]
caesarDecode xs = [shift x (-n) | x <- xs]
    where 
        n = argmin [chiSquareStatistic (rotate freq_table x) table| x <- [0..25]]
        freq_table = frequencyTable $ map Data.Char.toLower xs