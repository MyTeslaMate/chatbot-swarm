# config.py
import os
from openai import OpenAI
import qdrant_client
from stripe import StripeClient
from grafana_api.grafana_face import GrafanaFace

# Initialize connections
openai_client = OpenAI()
qdrant = qdrant_client.QdrantClient(host="localhost")

# Constants
EMBEDDING_MODEL = "text-embedding-3-large"
COLLECTION_NAME = "help_center"
