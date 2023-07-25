DB_TABLE_NAME = "replit_db"
DB_DOCUMENT_ID = 629

from . import ReplitDatabase
from tinydb import TinyDB
from tinydb.table import Document
from tinydb.operations import delete

class LocalDatabase(ReplitDatabase):
    """Dictionary-like interface for Repl.it Database, backed by TinyDB.

    This interface will coerce all values everything to and from JSON.
    """

    __slots__ = ("db_path", "table", "db")

    def __init__(self, db_path: str) -> None:
        """Initialize database. You shouldn't have to do this manually.

        Args:
            db_path (str): Database file path to use.
        """
        self.db_path = db_path
        self.db = TinyDB(db_path)
        self.table = self.db.table(DB_TABLE_NAME, cache_size=None) # Infinite cache!!!!

        if not self.table.contains(doc_id=DB_DOCUMENT_ID):
            self.table.insert(Document({}, doc_id=DB_DOCUMENT_ID))

    def update_db_url(self, db_url: str) -> None:
        """Stubbed"""
        pass

    def get_raw(self, key: str) -> str:
        """Look up the given key in the database and return the corresponding value.
        Args:
            key (str): Key to get value for.
        Raises:
            KeyError: The key is not in the database.
        Returns:
            str: Raw value from database.
        """
        return self.table.get(doc_id=DB_DOCUMENT_ID)[key]

    def set_bulk_raw(self, values: dict[str, str]) -> None:
        """Set multiple values in the database.

        Args:
            values (dict[str, str]): The key-value pairs to set.
        """
        self.table.update(Document(values, doc_id=DB_DOCUMENT_ID))

    def __delitem__(self, key: str) -> None:
        """Delete a key from the database.

        Args:
            key (str): The key to delete

        Raises:
            KeyError: Key is not set
        """
        self.table.update(delete(key), doc_ids=[DB_DOCUMENT_ID])

    def prefix(self, prefix: str) -> tuple[str, ...]:
        """Return all of the keys in the database that begin with the prefix.
        Args:
            prefix (str): The prefix the keys must start with, blank means anything.
        Returns:
            Tuple[str]: The keys found.
        """
        return tuple(filter(lambda key: key.startswith(prefix),self.table.get(doc_id=DB_DOCUMENT_ID).keys()))

    def __repr__(self) -> str:
        """A representation of the database.

        Returns:
            A string representation of the database object.
        """
        return f"<{self.__class__.__name__}(db_path={self.db_path!r})>"

    def close(self) -> None:
        """Close the database file handle."""
        self.db.close()


db_path = "local_replit_db.db"
db: LocalDatabase | None = LocalDatabase(db_path)

if not db:
    # The user will see errors if they try to use the database.
    print('Warning: error initializing database. Replit DB is not configured.')
