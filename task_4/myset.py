from collections import Iterable


class MySet:
    """Class that supports all utility of Python set()

    """
    _items = None

    def __init__(self, values=None):
        items = list()

        if values is not None:
            if isinstance(values, Iterable):
                for i in values:
                    if i not in items:
                        items.append(i)
            else:
                if values not in items:
                    items.append(values)

        self._items = items

    @property
    def items(self):
        return self._items

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        if self._items:
            # tmp = '{' + ' '.join(str(i) for i in self._items) + '}'
            return '{' + ', '.join(str(i) for i in self._items) + '}'
        else:
            return 'My set()'

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        # for cases of iterable argument
        if isinstance(item, Iterable):
            contains = 0
            for i in item:
                if i in self._items:
                    contains += 1
            return contains == len(item)
        # for cases of single value
        return item in self._items

    # --------------------------------------------
    # comparison operations
    # --------------------------------------------

    def __eq__(self, value):
        """Return self==value."""
        if isinstance(value, MySet):
            return sorted(self._items) == sorted(value._items)
            # !!! check with in operator
        else:
            raise TypeError('Cannot compare MySet with other types')

    def __gt__(self, value):
        """Return self>value."""
        if isinstance(value, MySet):
            return all(o in self._items for o in value._items) \
                   and not all(i in value._items for i in self._items)
        else:
            raise TypeError('Cannot compare MySet with other types')

    def __ge__(self, value):
        """Return self>=value."""
        return self > value or self == value

    def __lt__(self, other):
        """Return self<value."""
        return not(self >= other)

    def __le__(self, other):
        """Return self<=value."""
        return not(self > other)

    # --------------------------------------------
    # AND operations
    # --------------------------------------------

    def __and__(self, other):
        """Return self&other."""
        if isinstance(other, MySet):
            intersection = list()
            for i in self._items:
                if i in self._items and i in other._items:
                    intersection.append(i)
            for i in other._items:
                if i in self._items and i in other._items:
                    intersection.append(i)
            return MySet(intersection)
        else:
            raise TypeError('Both must be MySet()')

    def __rand__(self, other):
        """Return other&self."""
        return self & other

    def __iand__(self, other):
        """Return self&=other"""
        self._items = (self & other)._items
        return self

    # --------------------------------------------
    # OR operations
    # --------------------------------------------

    def __or__(self, other):
        """Return self|other."""
        if isinstance(other, MySet):
            union = list()
            for i in self._items:
                if i in self._items or i in other._items:
                    union.append(i)
            for i in other._items:
                if i in self._items or i in other._items:
                    union.append(i)
            return MySet(union)
        else:
            raise TypeError('Both must be MySet()')

    def __ror__(self, other):
        """Return other|self."""
        return self | other

    def __ior__(self, other):
        """Return self|=other."""
        self._items = (self | other)._items
        return self

    # --------------------------------------------
    # XOR operations
    # --------------------------------------------

    def __xor__(self, other):
        """Return self^other."""
        if isinstance(other, MySet):
            symm_difference = list()
            for i in self._items:
                if not (i in self._items and i in other._items):
                    symm_difference.append(i)
            for i in other._items:
                if not (i in other._items and i in self._items):
                    symm_difference.append(i)
            return MySet(symm_difference)
        else:
            raise TypeError('Both must be MySet()')

    def __rxor__(self, other):
        """Return other^self"""
        return self ^ other

    def __ixor__(self, other):
        """Return self^=other"""
        self._items = (self ^ other)._items
        return self

    # --------------------------------------
    # SUB operations
    # --------------------------------------

    def __sub__(self, other):
        """Return self-other."""
        if isinstance(other, MySet):
            difference = list()
            for i in self._items:
                if i in self._items and i not in other._items:
                    difference.append(i)
            return MySet(difference)
        else:
            raise TypeError('Both must be MySet()')

    def __rsub__(self, other):
        """Return other-self"""
        return self - other

    def __isub__(self, other):
        """Return self-=other"""
        self._items = (self - other)._items
        return self

    # --------------------------------------------------
    # public methods
    # --------------------------------------------------

    def copy(self):
        """Return shallow copy of MySet object"""
        new_set = MySet()
        new_set._items = self._items
        return new_set

    def add(self, element):
        """Add an element to a set.

        This has no effect if the element is already present.
        """
        if isinstance(element, Iterable):
            for e in element:
                if e not in self._items:
                    self._items.append(e)
        else:
            if element not in self._items:
                self._items.append(element)

    def clear(self):
        """Remove all elements from this set."""
        self._items.clear()

    def discard(self, element):
        """Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        """
        if element in self._items:
            self._items.remove(element)







    """class set(object)
 |  set() -> new empty set object
 |  set(iterable) -> new set object
 |  
 |  Build an unordered collection of unique elements.
 |  
 |  Methods defined here:
 |
 |  pop(...)
 |      Remove and return an arbitrary set element.
 |      Raises KeyError if the set is empty.
 |
 |  remove(...)
 |      Remove an element from a set; it must be a member.
 |
 |      If the element is not a member, raise a KeyError.
 |
 |  update(...)
 |      Update a set with the union of itself and others.
 |  
 |  difference(...)
 |      Return the difference of two or more sets as a new set.
 |      
 |      (i.e. all elements that are in this set but not the others.)
 |  
 |  difference_update(...)
 |      Remove all elements of another set from this set.
 |  
 |  intersection(...)
 |      Return the intersection of two sets as a new set.
 |      
 |      (i.e. all elements that are in both sets.)
 |  
 |  intersection_update(...)
 |      Update a set with the intersection of itself and another.
 |  
 |  isdisjoint(...)
 |      Return True if two sets have a null intersection.
 |  
 |  issubset(...)
 |      Report whether another set contains this set.
 |  
 |  issuperset(...)
 |      Report whether this set contains another set.
 |  
 |  symmetric_difference(...)
 |      Return the symmetric difference of two sets as a new set.
 |      
 |      (i.e. all elements that are in exactly one of the sets.)
 |  
 |  symmetric_difference_update(...)
 |      Update a set with the symmetric difference of itself and another.
 |  
 |  union(...)
 |      Return the union of sets as a new set.
 |      
 |      (i.e. all elements that are in either set.)"""







