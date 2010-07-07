import qualified Data.Map as Map

import SimpleMemo

type RVal = Int
type RCount = Integer
type Rolls = [(RVal,RCount)]

addrolls :: Rolls -> Rolls -> Rolls
addrolls rolls1 rolls2 = let
    newlist = do
        (k1, v1) <- rolls1
        (k2, v2) <- rolls2
        return (k1+k2, v1*v2)
    in Map.toList $ Map.fromListWith (+) newlist

diedistrib :: RCount -> RVal -> Rolls
diedistrib 1 nsides = zip [1..nsides] (repeat 1)
diedistrib n nsides = let
    base = (diedistrib 1 nsides) 
    lwr = (diedistrib (n-1) nsides)
    in addrolls base lwr

matchoff :: RCount -> RCount -> RVal -> (RCount, RCount, RCount)
matchoff n1 n2 nsides = let
    rolls1 = diedistrib n1 nsides
    rolls2 = diedistrib n2 nsides
    rcompare (r1, c1) (r2, c2)
        | r1 > r2 = ((c1 * c2),0,0)
        | r1 < r2 = (0,0,(c1 * c2))
        | r1 == r2 = (0,(c1 * c2),0)
    (wins, ties, losses) = unzip3 [rcompare x y | x <- rolls1, y<-rolls2]
    -- in (wins, ties, losses)
    in (sum wins, sum ties, sum losses)

matchfrac :: (Fractional n) => RCount -> RCount -> RVal -> (n,n,n)
matchfrac n1 n2 ns = let
    (wi,ti,li) = matchoff n1 n2 ns
    w = fromIntegral wi
    t = fromIntegral ti
    l = fromIntegral li
    total = fromIntegral (wi + ti + li)
    in (w/total,t/total, l/total)
    -- in (w,t,l)

winfrac :: (Fractional n) => RCount -> RCount -> RVal -> n
winfrac n1 n2 ns =
    let (w,t,l) = matchfrac n1 n2 ns
    in w