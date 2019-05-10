{-# LANGUAGE GeneralizedNewtypeDeriving #-}

module Risk where

import Control.Monad.Random
import Data.List

------------------------------------------------------------
-- Die values

newtype DieValue = DV { unDV :: Int } 
  deriving (Eq, Ord, Show, Num)

first :: (a -> b) -> (a, c) -> (b, c)
first f (a, c) = (f a, c)

instance Random DieValue where
  random           = first DV . randomR (1,6)
  randomR (low,hi) = first DV . randomR (max 1 (unDV low), min 6 (unDV hi))

die :: Rand StdGen DieValue
die = getRandom

------------------------------------------------------------
-- Risk

type Army = Int

data Battlefield = Battlefield { attackers :: Army, defenders :: Army }

-- Excercise 2

type Attackers = Int
type Defenders = Int

attackerUnits :: Battlefield -> Attackers
attackerUnits (Battlefield att _)
  | att >= 3    = 3
  | att <= 1    = 0
  | otherwise   = att

defensiveUnits :: Battlefield -> Defenders
defensiveUnits (Battlefield _ def)
  | def >= 2    = 2
  | otherwise   = def

rollDice :: Int -> Rand StdGen [DieValue]
rollDice n = sequence $ replicate n die

type Casualty = (Int, Int)

casualty :: [Bool] -> Casualty 
casualty = foldr (\b (m,n) -> if b then (m+1,n) else (m,n+1)) (0,0)

fight :: Attackers -> Defenders -> Rand StdGen Casualty
fight attackers defenders = liftM casualty $ liftM2 (zipWith (<)) attDices defDices 
  where
    attDices = liftM (reverse . sort) $ rollDice attackers
    defDices = liftM (reverse . sort) $ rollDice defenders

updateBattlefield :: Casualty -> Battlefield -> Battlefield
updateBattlefield (ac,dc) (Battlefield att def) = Battlefield (att-ac) (def-dc)

battle :: Battlefield -> Rand StdGen Battlefield
battle bf = liftM2 updateBattlefield losses (return bf) where
  losses = fight att def
  att = attackers bf
  def = defenders bf


-- Excercise 3

invade :: Battlefield -> Rand StdGen Battlefield
invade bf@(Battlefield att def)
  | att < 2     = return bf
  | def == 0    = return bf
  | otherwise   = battle bf >>= invade


-- Excercise 4
type Outcome = (Int, Int)
type Simulations = Int

simulate :: Simulations -> Battlefield -> Rand StdGen Outcome
simulate n bf = liftM foldBattlefield $ sequence $ map invade $ replicate n bf
  where
    foldBattlefield = foldr (\bf (wins,losses) -> if (defenders bf == 0) then (wins+1,losses) else (wins,losses+1)) (0,0)

successProb :: Battlefield -> Rand StdGen Double
successProb bf = liftM outcomeToProb $ simulate 1000 bf
  where
    outcomeToProb (x,y) = (fromIntegral x) / (fromIntegral (x+y))