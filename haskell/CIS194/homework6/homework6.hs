-- Excercise 1
fib :: Integer -> Integer
fib 1 = 0
fib 2 = 1
fib n = fib (n-1) + fib (n-2)

fibs1 :: [Integer]
fibs1 = map fib [1..]

-- Excercise 2
fibs2 :: [Integer]
fibs2 = 0 : 1 : [a + b | (a, b) <- zip fibs2 $ tail fibs2]

-- Excercise 3
data Stream a = Cons a (Stream a)

streamToList :: Stream a -> [a]
streamToList (Cons a b) = a : (streamToList b)

instance Show a => Show (Stream a) where
    show = show . take 10 . streamToList

-- Excercise 4
streamRepeat :: a -> Stream a
streamRepeat a = Cons a (streamRepeat a)

streamMap :: (a -> b) -> (Stream a) -> (Stream b)
streamMap f (Cons a b) = Cons (f a) (streamMap f b)

streamFromSeed :: (a -> a) -> a -> Stream a
streamFromSeed f a = Cons b (streamFromSeed f b)
    where b = f a

-- Excercise 5
nats :: Stream Integer
nats = streamFromSeed (+1) (-1)

interleaveStreams :: (Stream a) -> (Stream a) -> (Stream a)
interleaveStreams (Cons a b) c = Cons a (interleaveStreams c b)
-- This declaration won't work with ruler
-- interleaveStreams (Cons a b) (Cons c d) = Cons a (Cons c (interleaveStreams b d))

ruler :: Stream Integer
ruler = startFrom 0 where
    startFrom n = interleaveStreams (streamRepeat n) (startFrom (n + 1))

-- TODO: excercise 6 & 7