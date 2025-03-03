from typing import TypeVar, Generic, Type
from database.connections.connection import DatabaseConnection

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, db: DatabaseConnection, model_class: Type[T]):
        self.db = db
        self.model_class = model_class
        self.table_name = self._get_table_name()
    
    def _get_table_name(self) -> str:
        """Get table name from model class name (pluralized)"""
        model_name = self.model_class.__name__.lower()
        return f"{model_name}s"
    
    def _model_to_dict(self, model: T) -> dict:
        """Convert model to dictionary for DB insertion"""
        return model.__dict__
    
    def _row_to_model(self, row) -> T:
        """Convert DB row to model instance"""
        return self.model_class(**dict(row))