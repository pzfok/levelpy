#
# levelpy/leveldb_module_shims.py
#
"""
Shims for normalizing modules.
"""

import logging

log = logging.getLogger(__name__)


def NormalizeBackend(wrapper, db):
    full_classname = "%s.%s" % (db.__class__.__module__, db.__class__.__name__)

    log.debug('NormalizeBackend: %s' % (full_classname))

    # get the function to normalize
    normalizer = {
        'plyvel._plyvel.DB': plyvel_database,
        'leveldb.LevelDB': py_leveldb,
    }.get(full_classname, lambda wrap_, db_: None)

    log.debug('NormalizeBackend: Found normalizer %s' % (normalizer))

    # normalize the database object
    normalizer(wrapper, db)


def py_leveldb(wrapper, db):

    import leveldb

    if hasattr(db, 'WriteBatch'):
        wrapper.WriteBatch = db.WriteBatch
    else:
        wrapper.WriteBatch = leveldb.WriteBatch

    wrapper.DestroyDB = leveldb.DestroyDB
    wrapper.RepairDB = leveldb.RepairDB
    wrapper.Snapshot = leveldb.Snapshot


def plyvel_database(wrapper, db):
    log.debug('plyvel_database: %s' % (db))

    import plyvel

    wrapper.DestroyDB = plyvel.destroy_db
