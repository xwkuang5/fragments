module Party where
import Data.Monoid
import Data.Tree
import Employee
import Data.List

-- Excercise 1

glCons :: Employee -> GuestList -> GuestList
glCons e@(Emp { empName=x, empFun=y }) (GL l f) = GL (e:l) (y+f)

instance Monoid GuestList where
    mempty = GL [] 0
    mappend (GL a b) (GL c d) = GL (a ++ c) (b + d)

moreFun :: GuestList -> GuestList -> GuestList
moreFun gl1@(GL _ fun1) gl2@(GL _ fun2)
    | fun1 <= fun2  = gl2
    | otherwise     = gl1 

-- Excercise 2

treeFold :: (a -> b -> b) -> b -> Tree a -> b
treeFold f acc (Node { rootLabel=x, subForest=xs }) = f x $ foldr (flip $ treeFold f) acc xs

-- Excercise 3

nextLevel :: Employee -> [(GuestList, GuestList)] -> (GuestList, GuestList)
nextLevel emp list = (with, without) where
    with    = foldr (<>) (glCons emp mempty) $ map snd list
    without = foldr (<>) mempty $ map (\(w,wo) -> moreFun w wo) list

-- Excercise 4

maxFun :: Tree Employee -> GuestList
maxFun = uncurry moreFun . maxFunHelper where
    maxFunHelper (Node emp [])      = ((glCons emp mempty), mempty)
    maxFunHelper (Node root forest) = nextLevel root $ map maxFunHelper forest

-- Excercise 5

getFun :: GuestList -> Fun
getFun (GL _ fun) = fun

getNames :: GuestList -> [Name]
getNames (GL employees _) = sort $ map empName employees

retrieveGuests :: Tree Employee -> [String]
retrieveGuests empTree = header : guestNames where
    guests = maxFun empTree
    header = "Total fun: " ++ (show $ getFun guests)
    guestNames = getNames guests

main :: IO ()
main = readFile "company.txt" >>=
    mapM putStrLn . retrieveGuests . read