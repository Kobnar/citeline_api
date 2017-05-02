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

    def __init__(self, parent=None, name=None):
        if not (parent is None or isinstance(parent, IndexResource)):
            raise TypeError('Invalid traversal resource: {}'.format(type(parent)))
        if not (isinstance(name, str) or name is None):
            raise TypeError('Invalid name: {}'.format(name))

        self.__parent__ = parent
        self.__name__ = name
        self._items = {}

        for name, child in self._OFFSPRING.items():
            self[name] = child

    def __setitem__(self, key, value):
        """
        Adds a child :class:`IndexResource` to the traversal tree.

        Raises an exception if ``value`` is not a type or instance of
        IndexResource or its children, or cannot be called as one to
        create an instance of IndexResource.
        """
        if not isinstance(value, IndexResource):
            try:
                value = value(self, key)
            except TypeError as err:
                msg = 'Invalid traversal resource: {}: {}'
                raise TypeError(msg.format(value, err))
        self._items[key] = value

    def __getitem__(self, key):
        """
        Returns a child resource from the traversal tree.
        """
        return self._items[key]

    def __iter__(self):
        return self._items.__iter__()

    @property
    def name(self):
        return self.__name__

    @property
    def lineage(self):
        return [x.name for x in location.lineage(self)]
