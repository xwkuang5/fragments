def dedup(items, key=None):
    """A simple generator function to deduplicate items in an iterable
    
    Usage: for item in dedup(items):
                # do something
    """
    seen = set()

    for item in items:
        key = item if key is None else key(item)
        if key not in seen:
            yield item
            seen.add(key)