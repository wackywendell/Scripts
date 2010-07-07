import qualified Data.Map as M

data Class = Class {dep :: String, num :: Int, grd :: String}
classFromList [d, n, g] = Class d (read n) g

instance Show Class where
    show c = dep c ++ " " ++ (show $ num c) ++ ":" ++ grd c

grades = ["A","A-","B+","B"]

makeLookup = M.fromList.(zip grades)

getGrade gs c = case M.lookup (grd c) gs of
    Nothing -> error ("error looking up grade for class " ++ show c)
    Just a -> a

getGrades gs = map (getGrade gs)

normGet = getGrades $ makeLookup [4.00,3.67,3.33,3.00]
berkGet = getGrades $ makeLookup [4.00,3.7,3.3,3.00]
average ints = (sum ints) / (fromIntegral $ length ints)

filterMajor = filter (\ c -> elem (dep c) ["PHYS", "ASTR"])

filterUpper = filter (\ c -> (num c) >= 40)

roundTo n = (fromIntegral $ round (n*100)) / 100

showAvg = show . roundTo . average

main = do
    f <- readFile "gpaclasses.txt"
    let cs = map classFromList.map words.lines $ f
    putStrLn $ "GPA:\t\t\t" ++ (showAvg $ normGet cs)
    putStrLn $ "Major GPA:\t\t" ++ (showAvg $ normGet $ filterMajor cs)
    putStrLn $ "Berk GPA:\t\t" ++ (showAvg $ berkGet cs)
    putStrLn $ "Berk Major:\t\t" ++ (showAvg $ berkGet $ filterMajor cs)
    putStrLn $ "Berk Upper:\t\t" ++ (showAvg $ berkGet $ filterUpper cs)
    putStrLn $ "Berk Major Upper:\t" ++ 
                (showAvg $ berkGet $ filterUpper $ filterMajor cs)
    
