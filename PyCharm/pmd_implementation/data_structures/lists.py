from .basics import ListNode
from collections import UserList


class LinkedListIterator:
    """Iterator used to traverse the lists defined in this module,
    can handle both null-terminated and dummy terminated lists"""

    def __init__(self, parent_list, start: int = 0):
        self.pending = None

        if start > 0 and len(parent_list) > 0:
            self.cursor = parent_list[start]
        elif len(parent_list) > 0:
            self.cursor = parent_list.head.child
        else:
            self.cursor = None

        self.parent = parent_list

        # Corresponds to the index of the cursor
        self.index = 0

    def __iter__(self):
        """Required for this iterator to be an iterable, it doesn't do anything other than return itself."""
        return self

    def __next__(self):
        self.pending = self.cursor

        if self.cursor is not None and not self.cursor.is_dummy:
            self.cursor = self.cursor.child
            self.index += 1
            return self.pending.data
        else:
            raise StopIteration

    def next(self):
        return self.__next__()

    def insert(self, other: ListNode):
        """Appends other as a ListNode after pending, but before cursor, updates the index accordingly"""
        self.cursor.parent.link(other)
        other.link(self.cursor)
        self.index += 1

    def remove(self):
        """Removes pending from the linked list if it's not None"""
        if self.pending is not None:
            self.parent.unlink(self.pending)
            temp = self.pending.data
            self.pending = None
            self.index -= 1
            return temp


class LinkedList(UserList):
    """Represents a doubly linked list with two dummy nodes at the start and end."""

    def __init__(self, data: iter = None, is_sorted: bool = False):
        """Creates an empty linked list and sets up the defaults

        data: [optional] if supplied, will automatically insert the items into the linked list upon creation.

        is_sorted: [optional] when True uses comparisons to determine if an item should go after,
            or before a given node, default is false."""

        super().__init__()

        self.is_sorted = is_sorted

        # Represents the head of the list
        self.head = ListNode()

        # Represents the tail of the list
        self.tail = ListNode()

        # Represents the number of elements in the list
        self.size = 0

        self.clear()

        # Appends the supplied data to the list if it was supplied.
        if data is not None:
            self.extend(data)

    # region built-in methods

    def __str__(self) -> str:
        """Returns a string in the format [a0, a1, a2,..., an] where n is the number of elements in the list"""
        result = "["

        first = True

        current = self.head.child

        while not current.is_dummy:
            if first:
                first = False
            else:
                result += ", "

            result += str(current)
            current = current.child

        result += "]"

        return result

    def __len__(self) -> int:
        """Returns the number of elements in the list"""
        return self.size

    def __contains__(self, item) -> bool:
        """Returns true if the item is contained within this list."""
        current = self.head.child

        while not current.is_dummy:
            if item == current:
                return True
            current = current.child

        return False

    def __iter__(self, start: int = 0):
        return LinkedListIterator(self, start)

    def __setitem__(self, key, value):
        self.insert(value, key)

    def __getitem__(self, item):
        """Inserts the given item at the given index"""
        it = self.__iter__()
        while True:
            try:
                c = it.__next__()
                if item == it.index:
                    return c.data
            except StopIteration:
                raise IndexError("Supplied index is out of bounds")

    # endregion

    # region Node operations

    def unlink(self, target: ListNode):
        """Removes the target from the list by
        setting its parent.child to target.child and child.parent to target.parent."""
        # There shouldn't be any instances of leaves or roots in this list, just dummies
        # __contains__ won't return true if target is head, or tail
        if target in self:
            target.parent.child = target.child
            target.child.parent = target.parent
            self.size -= 1

    # endregion

    # region list operations

    # TODO add a _traverse_list method that can find items based on a lambda expression
    #  and do an action whenever somehting is found
    #  This way it can traverse both backwards and forwards.

    def clear(self):
        """Resets the list size to zero and removes all elements."""
        self.head.link(self.tail)
        self.size = 0

    def extend(self, iterable: iter):
        for d in iterable:
            self.append(d)

    def append(self, item):
        """Adds an item to the list.
        If is_sorted is True, then traverses the list and inserts into the appropriate spot,
        otherwise, it appends the item directly to the end of the list."""

        if self.is_sorted and not (len(self) > 0 and item > self.tail.parent):
            # TODO traverse the list and determine where the item should go
            temp = ListNode(item)
            if len(self) == 0:
                self.head.link(temp)
                temp.link(self.tail)
            else:
                # TODO
                pass
        else:
            # Appends the item to the end of the list and increments the size by 1
            temp = ListNode(item)
            self.tail.parent.link(temp)
            temp.link(self.tail)
            self.size += 1

    def insert(self, item, index: int):
        """Inserts the given item at the given index"""
        it = self.__iter__()
        while True:
            try:
                c = it.__next__()
                if index == it.index:
                    it.insert(ListNode(item))
                    break
            except StopIteration:
                raise IndexError("Supplied index is out of bounds")

    def remove(self, item):
        """Removes an item from the list, if it was in the list"""
        it = self.__iter__()
        while True:
            try:
                c = it.__next__()
                if item == c:
                    it.remove()
                    break
            except StopIteration:
                break

    def pop(self, index: int = None):
        if index is None and len(self) > 0:
            temp = self.tail.parent.data
            self.unlink(self.tail.parent)
            return temp
        else:
            it = self.__iter__()
            while True:
                try:
                    it.__next__()
                    if index == it.index - 1:
                        return it.remove()
                except StopIteration:
                    raise IndexError("Supplied index is out of bounds")

    def index(self, item, start: int = 0, end: int = None) -> int:
        if end is None:
            end = len(self)

        it = self.__iter__(start)
        while True:
            try:
                c = it.__next__()
                if item == c:
                    return it.index - 1

                if end == it.index:
                    break
            except StopIteration:
                break
        raise ValueError("Item does not exist")

    # endregion
