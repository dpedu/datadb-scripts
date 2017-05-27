import os
from datetime import datetime
from os.path import join as pathjoin
from os.path import exists


DATADB_ROOT = "/nexus/datadb/backups/"
DATADB_TMP = "/nexus/datadb/tmp/"

DATADB_DIR_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"  # Same as isoformat(), but we need to parse it back


class NoBackupException(Exception):
    pass


def get_backup_dir(backup_name):
    """
    Returns path to this profile's backup base dir. The base dir contains the 'data' directory
    """
    return pathjoin(DATADB_ROOT, backup_name)


def get_latest_backup(backup_name):
    """
    Get the absolute local path to a backup or raise an exception if none exists. When getting a backup, sort folder
    names (they're timestamps) and return newest.
    :returns: str absolute path to backup seq /0/
    """
    backups_dir = pathjoin(get_backup_dir(backup_name), 'data')

    if not exists(backups_dir):
        raise NoBackupException("Backup {} does not exist".format(backup_name))

    dirs = os.listdir(backups_dir)

    if not dirs:
        raise NoBackupException("No backups exist for {}".format(backup_name))

    dirs = sorted([datetime.strptime(d, DATADB_DIR_TIMESTAMP_FORMAT) for d in dirs])

    return pathjoin(backups_dir, dirs[-1].strftime(DATADB_DIR_TIMESTAMP_FORMAT), 'data')
