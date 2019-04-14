module LogAnalysis where

import Log

joinWithSeparator :: [String] -> String -> String
joinWithSeparator [] _          = ""
joinWithSeparator [x] _         = x
joinWithSeparator (x:xs) sep    = x ++ sep ++ (joinWithSeparator xs sep)

parseMessageHelper :: [String] -> LogMessage
parseMessageHelper ("I":timeStamp:message)                      = LogMessage Info (read timeStamp :: Int) (joinWithSeparator message " ")
parseMessageHelper ("W":timeStamp:message)                      = LogMessage Warning (read timeStamp :: Int) (joinWithSeparator message " ")
parseMessageHelper ("E":errorCode:timeStamp:message)            = LogMessage (Error (read errorCode :: Int)) (read timeStamp :: Int) (joinWithSeparator message " ")
parseMessageHelper unknownMessage                               = Unknown (joinWithSeparator unknownMessage " ")

parseMessage :: String -> LogMessage
parseMessage = parseMessageHelper . words

parse :: String -> [LogMessage]
parse = (map parseMessage) . lines

insert :: LogMessage -> MessageTree -> MessageTree
insert (Unknown _) tree = tree
insert newMessage Leaf  = Node Leaf newMessage Leaf
insert newMessage@(LogMessage _ timeStamp1 _) (Node leftNode root@(LogMessage _ timeStamp2 _) rightNode)
    | timeStamp1 <= timeStamp2  = Node (insert newMessage leftNode) root rightNode
    | otherwise                 = Node leftNode root (insert newMessage rightNode)
insert _ (Node _ (Unknown _) _) = error "Unknown messages are not allowed in MessageTree"

build :: [LogMessage] -> MessageTree
build = foldr insert Leaf

inOrder :: MessageTree -> [LogMessage]
inOrder Leaf                                    = []
inOrder (Node leftNode rootMessage rightNode)   = (inOrder leftNode) ++ [rootMessage] ++ (inOrder rightNode)

-- errors with a severity of at least 50
isRelevant :: LogMessage -> Bool
isRelevant (LogMessage (Error errorCode) _ _)   = errorCode >= 50
isRelevant _                                    = False

filterRelevant :: [LogMessage] -> [LogMessage]
filterRelevant = filter isRelevant

retrieveMessage :: LogMessage -> String
retrieveMessage (LogMessage _ _ message)    = message
retrieveMessage (Unknown _)                 = error "Can not retrieve message from unknown log message"

whatWentWrong :: [LogMessage] -> [String]
whatWentWrong = (map retrieveMessage) . (inOrder . build) . filterRelevant

-- test with `testWhatWentWrong parse whatWentWrong "error.log"`