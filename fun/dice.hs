#!/usr/bin/ghci

import Data.List

type Side = Int
type Die  = [Side]
type Dice = [Die]

makelast lst dice = dice ++ [foldl (\\) lst dice]

makelsts :: (Num a) => a -> [b] -> [[b]]
makelsts 0 _ = [[]]
makelsts _ [] = []
makelsts n lst@(x:xs) = let
    lsts1 = map (x:) (makelsts (n-1) xs)
    lsts2 = makelsts n xs
    in lsts1 ++ lsts2

-- ~ nxtdie nd ns fstdie 

-- ~ makedielst nd ns lst = do
    -- ~ die1 <- makelsts ns lst
    -- ~ let nextlst = lst \\ die1
    -- ~ restdie <- makedielst (nd-1) ns nextlst
    -- ~ return die1:restdie

splits :: Side -> [Side] -> [(Die, Die)]
splits 0 xs = [([],xs)]
splits _ [] = []
splits n (x:xs) = 
    if length (x:xs) < n
    then []
    else map (joinf x) (splits (n-1) xs) ++ map (joinl x) (splits n xs)
         where joinf x (xs, ys) = (x:xs, ys)
               joinl y (xs, ys) = (xs, y:ys)

getalldice :: Side -> Side -> [Dice]
getalldice ndice nsides = nub $ map sort diewithdupes
    where 
        diewithdupes = helper ndice [1..(ndice * nsides)]
        -- ~ helper :: (Integral a) => a -> [a] -> [[[a]]]
        helper 1 lst = [[lst]]
        helper nd lst =
            do
                (fdie, rest) <- splits nsides lst
                nextdice <- helper (nd-1) rest
                if fdie < (head nextdice)
                    then return (fdie:nextdice)
                    else fail ""



t1 = length $ getalldice 3 3
-- ~ t2 = length $ makedie 3 3

getwin :: (Num a) => Die -> Die -> a
getwin a b = sum $ [ comp x y | x <- a, y<- b ]
    where 
        comp x y | x > y = 1
                 | x < y = -1
                 | True  = 0

getwins :: (Num a) => Dice -> [a]
getwins lst@(x:xs) = zipWith getwin lst (xs ++ [x])

alleq :: (Eq a) => [a] -> Bool
alleq []  = True
alleq [x] = True
alleq (x:xs)  = all (==x) xs

testdice :: Dice -> Bool
testdice lst = alleq $ map signum $ getwins lst

getdice nd ns = filter testdice $ getalldice nd ns

comparewins :: (Num a) => Dice -> Dice -> a
comparewins d1 d2 = let
    dw1 = map abs $ getwins d1
    dw2 = map abs $ getwins d2
    min1 = foldl1 min dw1
    min2 = foldl1 min dw2
    tot1 = sum dw1
    tot2 = sum dw2
    comp | min1 > min2 = 1
         | min1 < min2 = -1
         | tot1 > tot2 = 1
         | tot1 < tot2 = -1
         | otherwise   = 0
    in comp

bestdice :: (Num a) => Side -> Side -> [(Dice, [a])]
bestdice nd ns = let
    dice = getdice nd ns
    acc xs [] = xs
    acc [] (x:xs) = acc [x] xs
    acc (b:bs) (x:xs) = case comparewins x b of
        1  -> acc [x] xs
        0  -> acc (x:b:bs) xs
        -1 -> acc (b:bs) xs
    retform ds = (ds, getwins ds)
    in map retform $ acc [] dice

printlst [] = putStrLn "(Empty)"
printlst [x] = putStrLn (show x)
printlst (x:xs) = do 
    putStr ((show x) ++ " ")
    printlst xs

printres (ds, res) = do
    sequence_ $ map printlst ds
    putStr "   "
    print res
    putStrLn ""

printbest nd ns = do
    let ress = bestdice nd ns
    sequence_ $ map printres ress
