"""Replit DB-style API with a local file backing it"""
__name__ = "localreplitdb"
from .replitdb import Database as ReplitDatabase
from .localreplitdb import LocalDatabase, db, db_path
