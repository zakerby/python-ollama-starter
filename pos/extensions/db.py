from flask_sqlalchemy import SQLAlchemy
import qdrant_client

db = SQLAlchemy()

qdrant_db = qdrant_client.QdrantClient(host='localhost', port=6333)
