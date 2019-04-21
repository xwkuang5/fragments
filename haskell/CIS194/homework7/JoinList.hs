{-# LANGUAGE FlexibleInstances, TypeSynonymInstances #-}
{-# OPTIONS_GHC -Wall #-}

module JoinList where

import Data.Monoid
import Sized
import Scrabble
import Buffer

data JoinList m a = Empty
                  | Single m a
                  | Append m (JoinList m a) (JoinList m a)
    deriving (Eq, Show)


-- Excercise 1

(+++) :: Monoid m => JoinList m a -> JoinList m a -> JoinList m a
(+++) jl1 Empty     = jl1
(+++) Empty jl2     = jl2
(+++) jl1 jl2 = Append (tag jl1 <> tag jl2) jl1 jl2

tag :: Monoid m => JoinList m a -> m
tag Empty           = error "Empty JoinList"  
tag (Single m _)    = m
tag (Append m _ _)  = m

-- Excercise 2

tagSize :: (Sized b, Monoid b) =>
            JoinList b a -> Int
tagSize = getSize . size . tag

indexJ :: (Sized b, Monoid b) => 
            Int -> JoinList b a -> Maybe a
indexJ _ Empty                  = Nothing
indexJ 0 (Single _ a)           = Just a
indexJ _ (Single _ _)           = Nothing
indexJ i m@(Append _ a b)
    | i < 0 || i > msize        = Nothing
    | i < asize                 = indexJ i a
    | otherwise                 = indexJ (i-asize) b
    where
        msize = tagSize m
        asize = tagSize a

dropJ :: (Sized b, Monoid b) =>
            Int -> JoinList b a -> JoinList b a
dropJ _ Empty           = Empty
dropJ n jl
    | n <= 0            = jl
    | n >= tagSize jl   = Empty
dropJ n (Append _ a b)
    | n <= tagSize a    = (dropJ n a) +++ b
    | otherwise         = dropJ (n - tagSize a) b

takeJ :: (Sized b, Monoid b) =>
            Int -> JoinList b a -> JoinList b a
takeJ _ Empty           = Empty
takeJ n jl
    | n <= 0            = Empty
    | n >= tagSize jl   = jl
takeJ n (Append _ a b)
    | n <= tagSize a    = takeJ n a
    | otherwise         = a +++ (takeJ (n - tagSize a) b)

-- Excercise 3
scoreLine :: String -> JoinList Score String
scoreLine str = Single (scoreString str) str

-- Excercise 4
-- instance (Monoid a, Monoid b) => Monoid (a, b) where
--     mempty = (mempty, mempty)
--     mappend (a,b) (c,d) = (mappend a c, mappend b d)

jlToList :: (Monoid m) => JoinList m a -> [a]
jlToList Empty          = []
jlToList (Single _ a)   = [a]
jlToList (Append _ a b) = (jlToList a) ++ (jlToList b)

fromSingleLine :: String -> (JoinList (Score, Size) String)
fromSingleLine str = Single (scoreString str, Size 1) str

tagScore :: (JoinList (Score, Size) String) -> Int
tagScore = getScore . fst . tag

instance Buffer (JoinList (Score, Size) String) where
    -- | Convert a buffer to a String.
    toString = unlines . jlToList

    -- | Create a buffer from a String.
    fromString = fromLines . lines where
        fromLines []    = Empty
        fromLines [x]   = fromSingleLine x
        fromLines ls    = fromLines (take half ls) +++
                            fromLines (drop half ls) where
                                half = length ls `div` 2
        -- Note the following gives rise to a skewed JoinList
        -- fromLines x:xs  = fromSingleLine x +++ fromLines xs

    -- | Extract the nth line (0-indexed) from a buffer.  Return Nothing
    -- for out-of-bounds indices.
    line = indexJ

    -- | @replaceLine n ln buf@ returns a modified version of @buf@,
    --   with the @n@th line replaced by @ln@.  If the index is
    --   out-of-bounds, the buffer should be returned unmodified.
    replaceLine n str jl = (takeJ (n-1) jl) +++ (fromSingleLine str) +++ (dropJ n jl)

    -- -- | Compute the number of lines in the buffer.
    numLines = length . jlToList

    -- -- | Compute the value of the buffer, i.e. the amount someone would
    -- --   be paid for publishing the contents of the buffer.
    value = tagScore