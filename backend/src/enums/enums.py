from enum import Enum


class SessionStatus(Enum):
    UPLOADING="uploading"
    STORING="storing"
    ENQUEUING="enqueuing"
    PARSING="parsing"
    CHUNKING="chunking"
    EMBEDDING="embedding"
    READY="ready"
    FAILED="failed"
    