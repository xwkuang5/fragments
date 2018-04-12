import Data.Char
import Data.List
import System.IO 

sizeOfBoard = 3

data Player = O | B | X deriving (Eq, Show, Ord)

type Board = [[Player]]

nextPlayer :: Player -> Player
nextPlayer O = X
nextPlayer X = O
nextPlayer B = B

interleave :: a -> [a] -> [a]
interleave x []         = []
interleave x [y]        = [y]
interleave x (y:ys)     = y:x:interleave x ys

showPlayer :: Player -> [String]
showPlayer O = ["   ", " O ", "   "]
showPlayer X = ["   ", " X ", "   "]
showPlayer B = ["   ", "   ", "   "]

showRow :: [Player] -> String
showRow = concat . concat . interleave ["|"] . map showPlayer

showBoard :: Board -> IO ()
showBoard = putStrLn . unlines . interleave dash . map showRow
    where dash = replicate (sizeOfBoard*sizeOfBoard*3) '-'