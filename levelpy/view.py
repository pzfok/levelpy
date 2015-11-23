#
# levelpy/view.py
#
"""
Provides a read-only object accessing a database or sublevel
"""

from .db_accessors import LevelReader


class View(LevelReader):
    """
    This is an immutable object providing read-only access to the database
    (or a sublevel)
    """

    def __init__(self, db, prefix='', delim='!', value_encoding='utf-8'):
        super().__init__(prefix, delim, value_encoding)
        self._db = db

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step is not None:
                raise ValueError("Step values are not available for "
                                 "slices in levelpy")
            start, stop = self.subkey(key.start), self.subkey(key.stop)
            return self._db[start:stop]

        elif isinstance(key, (tuple, list, set)):
            t = type(key)
            return self._db[t(self.subkey(k) for k in key)]

        else:
            return self._db[self.subkey(key)]

    def __copy__(self):
        """
        Simple copy of view - same db, prefix, delimeter, and encoding
        """
        enc = self._get_encoding(None)
        return View(self._db, self.prefix, self.delim, enc)

    def view(self, key, delim=None, value_encoding=None):
        """
        Return a subview of this view
        """
        prefix = self.key_transform(key)
        delim = self.delim if (delim is None) else delim
        enc = self._get_encoding(value_encoding)

        return View(self._db,
                    prefix,
                    delim=delim,
                    value_encoding=enc,
                    )
