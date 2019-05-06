instance Functor ((->) e) where
    fmap = (.)

instance Functor ((,) e) where
    fmap f (e, a) = (e, f a)

data ITree a = Leaf (Int -> a)
             | Node [ITree a]

instance Functor ITree where
    fmap f (Leaf g) = Leaf (f . g)
    fmap f (Node x) = Node (map (\y -> fmap f y) x)

