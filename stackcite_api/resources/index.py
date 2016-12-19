from inspect import isclass
from pyramid import location


class IndexResource(object):
    """
    A base traversal resource used to define site indexes for Pyramid's
    traversal system.

    Raises an exception if ``parent`` is neither an instance of
    :class:`.IndexResource` nor ``None`` and if ``name`` is not a string.
    """

    _OFFSPRING = {}

    def __init__(self, parent, name):
        if not (parent is None or isinstance(parent, IndexResource)) \
                or not isinstance(name, str):
            raise TypeError("Invalid class: {}".format(type(parent)))

        self.__parent__ = parent
        self.__name__ = name
        self._items = {}

        for name, child in self._OFFSPRING.items():
            self[name] = child

    def __setitem__(self, key, value):
        """
        Adds a child :class:`IndexResource` to the traversal tree.

        Raises an exception if ``value`` is not a type or instance of
        IndexResource or its children.
        """
        if isclass(value):
            value = value(self, key)
        if not isinstance(value, IndexResource):
            raise TypeError("Invalid class: {}".format(type(value)))
        self._items[key] = value

    def __getitem__(self, key):
        """
        Returns a child resource from the traversal tree.
        """
        return self._items[key]

    @property
    def name(self):
        return self.__name__

    @property
    def lineage(self):
        return [x.name for x in location.lineage(self)]
