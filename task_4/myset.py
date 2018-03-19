from collections import Iterable


class MySet:
    """Class that supports all utility of Python set()

    """
    _items = None

    def __init__(self, iterable):
        items = list()

        for i in iterable:
            if i not in items:
                items.append(i)

        self._items = items

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        if self._items:
            # tmp = '{' + ' '.join(str(i) for i in self._items) + '}'
            return '{' + ', '.join(str(i) for i in self._items) + '}'
        else:
            return 'set()'

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

    def __eq__(self, other):
        if isinstance(other, MySet):
            return self._items == other._items
        else:
            raise TypeError('Cannot compare MySet with other types')




    """class set(object)
 |  set() -> new empty set object
 |  set(iterable) -> new set object
 |  
 |  Build an unordered collection of unique elements.
 |  
 |  Methods defined here:
 |  
 |  __eq__(self, value, /)
 |      Return self==value.
 |  
 |  __ge__(self, value, /)
 |      Return self>=value.
 |  
 |  __gt__(self, value, /)
 |      Return self>value.
 |  
 |  __le__(self, value, /)
 |      Return self<=value.
 |  
 |  __ne__(self, value, /)
 |      Return self!=value.
 |  
 |  __lt__(self, value, /)
 |      Return self<value.
 |
 |  
 |  __and__(self, value, /)
 |      Return self&value.
 |  
 |  __iand__(self, value, /)
 |      Return self&=value.
 |  
 |  __ior__(self, value, /)
 |      Return self|=value.
 |  
 |  __isub__(self, value, /)
 |      Return self-=value.
 |  
 |  __ixor__(self, value, /)
 |      Return self^=value.
 |  
 |  __or__(self, value, /)
 |      Return self|value.
 |  
 |  __rand__(self, value, /)
 |      Return value&self.
 |  
 |  __reduce__(...)
 |      Return state information for pickling.
 |  
 |  __ror__(self, value, /)
 |      Return value|self.
 |  
 |  __rsub__(self, value, /)
 |      Return value-self.
 |  
 |  __rxor__(self, value, /)
 |      Return value^self.
 |  
 |  __sub__(self, value, /)
 |      Return self-value.
 |  
 |  __xor__(self, value, /)
 |      Return self^value.
 |  
 |  add(...)
 |      Add an element to a set.
 |      
 |      This has no effect if the element is already present.
 |  
 |  clear(...)
 |      Remove all elements from this set.
 |  
 |  copy(...)
 |      Return a shallow copy of a set.
 |  
 |  difference(...)
 |      Return the difference of two or more sets as a new set.
 |      
 |      (i.e. all elements that are in this set but not the others.)
 |  
 |  difference_update(...)
 |      Remove all elements of another set from this set.
 |  
 |  discard(...)
 |      Remove an element from a set if it is a member.
 |      
 |      If the element is not a member, do nothing.
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
 |  pop(...)
 |      Remove and return an arbitrary set element.
 |      Raises KeyError if the set is empty.
 |  
 |  remove(...)
 |      Remove an element from a set; it must be a member.
 |      
 |      If the element is not a member, raise a KeyError.
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
 |      (i.e. all elements that are in either set.)
 |  
 |  update(...)
 |      Update a set with the union of itself and others."""







