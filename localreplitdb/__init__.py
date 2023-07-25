"""Replit DB-style API with a local file backing it"""
__name__ = "localreplitdb"
from .realreplitdb import Database as ReplitDatabase
from .localreplitdb import LocalDatabase as Database, db, db_path
