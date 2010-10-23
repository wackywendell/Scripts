import Data.Set
import Data.List

type HorsePos = (Int, Int)

moveHorse :: HorsePos -> [HorsePos]
moveHorse (c, r) = [(c', r') | c1 <- [1,2]
                   , c2 <- [-1,1]
                   , r2 <- [-1,1]
                   , let c' = c + c1 * c2
                   , let r' = r + (3 - c1) * r2
                   , 1 <= r'
                   , 1 <= c'
                   , 8 >= r'
                   , 8 >= c']

stepn 0 pos = [pos]
stepn n pos = 
    let allsteps = do
            onestep <- moveHorse pos
            newpos <- stepn (n-1) onestep
            return newpos
    in sort $ toList $ fromList allsteps

innsteps n lastpos firstpos =
    let allsteps = stepn n firstpos
    in elem lastpos allsteps

allboard n pos = 
    length (stepn n pos) == 64

numpos n pos = do
    n' <- [1..n]
    return $ length $ stepn n' pos

getboard poslist = 
    let 
        dispval pos = case (elem pos poslist) of
            True -> 1
            False -> 0
        getrow n = 
            do
                m <- [1..8]
                return $ dispval (n,m)
    in do
        n <- [1..8]
        return $ getrow n

rowtochars rlist = do
    let tochar 1 = 'X'
        tochar 0 = ' '
    p <- rlist
    return $ tochar p

btochars poslist = do
    row <- getboard poslist
    let charrow = rowtochars row
    return charrow

printboard :: [HorsePos] -> IO ()
printboard poslist = 
    let
        prows [] = do
            return ()
        prows (row:rows) = do
            putStrLn $ "|" ++ row ++ "|"
            prows rows
    in do
        putStrLn "----------"
        prows $ btochars poslist
        putStrLn "----------"
    

main = do
    printboard $ stepn 1 (1,1)
    printboard $ stepn 2 (1,1)

other2 = do
    print "---"
    printboard $ stepn 2 (1,1)
    print "---"
    printboard $ stepn 3 (1,1)
    print "---"
    printboard $ stepn 4 (1,1)

othermain = do
    print $ numpos 6 (1,1)
    print $ numpos 6 (3,1)
    print $ numpos 6 (4,5)
    print $ getboard $ stepn 1 (1,1)