toDigits :: Integer -> [Integer]
toDigits n
    | n <= 0    = []
    | n <= 9    = [n]
    | otherwise = (toDigits (n `div` 10)) ++ [n `mod` 10]

toDigitsRev :: Integer -> [Integer]
toDigitsRev = reverse . toDigits

doubleEveryOtherFromLeft :: [Integer] -> [Integer]
doubleEveryOtherFromLeft []            = []
doubleEveryOtherFromLeft [x]           = [x]
doubleEveryOtherFromLeft (x:y:rest)    = x : y*2 : doubleEveryOtherFromLeft rest

doubleEveryOther :: [Integer] -> [Integer]
doubleEveryOther = reverse . doubleEveryOtherFromLeft . reverse

sumInteger :: Integer -> Integer
sumInteger n
    | n <= 9    = n
    | otherwise = sumInteger (n `div` 10) + n `mod` 10

sumDigits :: [Integer] -> Integer
sumDigits []        = 0
sumDigits (x:xs)    = sumInteger x + sumDigits xs

validate :: Integer -> Bool
validate n = (sumDigits . doubleEveryOther . toDigits) n `mod` 10  == 0


type Peg = String
type Move = (Peg, Peg)

hanoi :: Integer -> Peg -> Peg -> Peg -> [Move]
hanoi 0 a b c = []
hanoi 1 a b c = [(a, c)]
hanoi n a b c = (hanoi (n-1) a c b) ++ [(a, c)] ++ (hanoi (n-1) b a c)