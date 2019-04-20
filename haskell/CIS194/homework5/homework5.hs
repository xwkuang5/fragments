{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}

import ExprT
import Parser
import StackVM
import qualified Data.Map as M

-- Excercise 1
eval :: ExprT -> Integer
eval (ExprT.Lit n)          = n
eval (ExprT.Add op1 op2)    = (eval op1) + (eval op2)
eval (ExprT.Mul op1 op2)    = (eval op1) * (eval op2)

-- Excercise 2
evalStrHelper :: Maybe ExprT -> Maybe Integer
evalStrHelper (Nothing)     = Nothing
evalStrHelper (Just expr)   = Just $ eval expr

evalStr :: String -> Maybe Integer
evalStr = evalStrHelper . (parseExp ExprT.Lit ExprT.Add ExprT.Mul)

-- Excercise 3

class Expr a where
    lit :: Integer -> a
    add :: a -> a -> a
    mul :: a -> a -> a

instance Expr ExprT where
    lit a   = ExprT.Lit a
    add a b = ExprT.Add a b
    mul a b = ExprT.Mul a b

reify :: ExprT -> ExprT
reify = id

-- Excercise 4

instance Expr Integer where
    lit a   = a
    add a b = a + b
    mul a b = a * b

instance Expr Bool where
    lit a   = a > 0
    add a b = a || b
    mul a b = a && b

newtype MinMax  = MinMax Integer deriving (Eq, Show)
newtype Mod7    = Mod7 Integer deriving (Eq, Show)

instance Expr MinMax where
    lit a                           = MinMax a
    add a@(MinMax b) c@(MinMax d)   = MinMax (max b d)
    mul a@(MinMax b) c@(MinMax d)   = MinMax (min b d) 

instance Expr Mod7 where
    lit a                       = Mod7 (a `mod` 7)
    add a@(Mod7 b) c@(Mod7 d)   = Mod7 $ (b + d) `mod` 7
    mul a@(Mod7 b) c@(Mod7 d)   = Mod7 $ (b * d) `mod` 7

testExp :: Expr a => Maybe a
testExp = parseExp lit add mul "(3 * -4) + 5"

testInteger = testExp :: Maybe Integer

-- Excercise 5
instance Expr Program where
    lit a       = [PushI a]
    add a b     = a ++ b ++ [StackVM.Add]
    mul a b     = a ++ b ++ [StackVM.Mul]

compile :: String -> Maybe Program
compile = parseExp lit add mul


-- Excercise 6

class HasVars a where
    var :: String -> a

data VarExpT = VarExpTLit Integer
             | VarExpTAdd VarExpT VarExpT
             | VarExpTMul VarExpT VarExpT
             | VarExpTVar String

instance HasVars VarExpT where
    var str = VarExpTVar str

instance Expr VarExpT where
    lit a       = VarExpTLit a
    add a b     = VarExpTAdd a b
    mul a b     = VarExpTMul a b

-- TODO: implement a HasVars and Expr instance for evaluation