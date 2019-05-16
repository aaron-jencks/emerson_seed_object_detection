
class Node:
    """Represents a node that can be used to store data and links to other nodes."""

    def __init__(self, data=None):
        self.data = data
        self.parents = []
        self.children = []

    # region built-ins

    def __str__(self):
        return str(self.data) if not self.is_dummy else '[dummy]'

    # region operator overloads

    def __eq__(self, other) -> bool:
        """Returns true if self == other"""
        if other is None or self.is_dummy:
            return False
        elif isinstance(other, self.__class__):
            if self is other:
                return True
            elif self.data == other.data:
                return True
            else:
                return False

    def __gt__(self, other) -> bool:
        """Returns true if self > other"""
        if other is None or self.is_dummy:
            return False
        elif isinstance(other, self.__class__):
            return not other.is_dummy and self.data > other.data
        else:
            # Assume other is some sort of data
            return self.data > other

    def __lt__(self, other) -> bool:
        """Returns true if self < other"""
        if other is None or self.is_dummy:
            return False
        elif isinstance(other, self.__class__):
            return not other.is_dummy and self.data < other.data
        else:
            # Assume other is some sort of data
            return self.data < other

    def __ge__(self, other) -> bool:
        """Returns true if self >= other"""
        return self > other or self == other

    def __le__(self, other) -> bool:
        """Returns true if self <= other"""
        return self < other or self == other

    # endregion

    def __contains__(self, other):
        """Returns true if there is a path from this node to the other, or if this node contains the data other"""
        if isinstance(other, self.__class__):
            if other in self.children:
                return True
            elif other == self.data:
                return True
            else:
                return False
        else:
            return self.data == other

    # endregion

    @property
    def is_leaf(self) -> bool:
        """Returns true if this node has no children."""
        return len(self.children) == 0

    @property
    def is_root(self) -> bool:
        """Returns true if this node has no parents."""
        return len(self.parents) == 0

    @property
    def is_dummy(self) -> bool:
        """Returns true if this node's data is None"""
        return self.data is None

    def link(self, other):
        """Links other after this node (makes it a child)."""
        if other is not None and isinstance(other, self.__class__):
            self.children.append(other)
            other.parents.append(self)

    def unlink(self, other):
        """Unlinks other from this node, assuming it's a child, if it's not, then nothing happens."""
        if other is not None and isinstance(other, self.__class__):
            self.children.remove(other)
            other.parents.remove(self)


class ListNode(Node):
    """Represents a node that can be used similar to a node, except that it can only have one child, and one parent."""

    def __init__(self, data=None):
        super().__init__(data)
        self.parent = None
        self.child = None

    @property
    def is_leaf(self) -> bool:
        return self.child is None

    @property
    def is_root(self):
        return self.parent is None

    def link(self, other):
        if isinstance(other, self.__class__):
            # WARNING, this will break any existing links, you need to handle that yourself
            self.child = other
            other.parent = self

    def unlink(self, other):
        if isinstance(other, self.__class__):
            self.child = None
            other.parent = None


# TODO Add BinaryNode
