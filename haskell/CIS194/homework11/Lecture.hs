module Lecture11 where

import           Control.Applicative

sequenceA :: Applicative f => [f a] -> f [a]
sequenceA []        = []
sequenceA (x:xs)    = (:) <$> x <*> sequenceA xs

mapA :: Applicative f => (a -> f b) -> ([a] -> f [b])
mapA f = \x -> sequenceA $ map f x

replicateA :: Applicative f => Int -> f a -> f [a]
replicateA n x = sequenceA $ replicate n x