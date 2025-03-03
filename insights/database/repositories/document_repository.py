from typing import List, Optional
from datetime import datetime
import sqlite3

from database.connections.connection import DatabaseConnection
from database.repositories.base_repository import BaseRepository
from database.models.document import Document


class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db: DatabaseConnection):
        super().__init__(db, Document)
    
    def create(self, document: Document) -> Document:
        """Create a new document in the database"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                '''
                INSERT INTO documents (id, content, description, timestamp, filetype)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (document.id, document.content, document.description, document.timestamp, document.filetype)
            )
            
            conn.commit()
            return document
    
    def get_by_id(self, document_id: int) -> Optional[Document]:
        """Get a document by its ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT * FROM documents WHERE id = ?',
                (document_id,)
            )
            
            row = cursor.fetchone()
            if row:
                return self._row_to_model(row)
            return None
    
    def get_all(self) -> List[Document]:
        """Get all documents"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM documents ORDER BY timestamp DESC')
            
            return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def update(self, document: Document) -> Document:
        """Update an existing document"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            document.updated_at = datetime.now()
            
            cursor.execute(
                '''
                UPDATE documents
                SET description = ?, content = ?, timestamp = ?, fyletype = ?
                WHERE id = ?
                ''',
                (document.description, document.content, document.timestamp, document.filetype, document.id)
            )
            
            conn.commit()
            
            return document
    
    def delete(self, document_id: int) -> bool:
        """Delete a document by its ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                'DELETE FROM documents WHERE id = ?',
                (document_id,)
            )
            
            conn.commit()
            
            return cursor.rowcount > 0
    
    def search_by_title(self, query: str) -> List[Document]:
        """Search for documents by title"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT * FROM documents WHERE title LIKE ? ORDER BY updated_at DESC',
                (f'%{query}%',)
            )
            
            return [self._row_to_model(row) for row in cursor.fetchall()]
        
    def get_documents_without_description(self) -> List[Document]:
        """Get documents without a description"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT * FROM documents WHERE description IS NULL ORDER BY timestamp DESC'
            )
            
            return [self._row_to_model(row) for row in cursor.fetchall()]
        
    def get_all_document_ids(self) -> List[str]:
        """Get a list of all document IDs"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM documents')
            
            return [row[0] for row in cursor.fetchall()]