from typing import BinaryIO, Union, Dict

from ..chunks import ChunkReader
from ..chunks.chunk_types.dtty import InternalType
from ..chunks.chunk_types.exob import ExternalObject
from ..chunks.chunk_types.exty import ExternalType
from ..chunks.chunk_types.obty import InternalObjectType
from ..utils.byte_io_sam import ByteIO


class SamFile:

    def __init__(self, file_object: Union[BinaryIO, ByteIO]):
        self.type_registry: Dict[int, Union[ExternalType, InternalType]] = {}
        self.object_registry: Dict[int, Union[InternalObjectType, ExternalObject]] = {}

        if isinstance(file_object, ByteIO):
            self._reader = file_object
        else:
            self._reader = ByteIO(file_object)
        self.chunks = []
        self.cr = ChunkReader(self._reader, self)
        while True:
            chunk = self.cr.read_chunk()
            if chunk is None:
                break
            self.chunks.append(chunk)

    def register_type(self, type_id, chunk: Union[ExternalType, InternalType]):
        self.type_registry[type_id] = chunk

    def get_type(self, type_id):
        return self.type_registry.get(type_id, None)

    def add_object(self, object_id, sam_object):
        self.object_registry[object_id] = sam_object

    def get_object(self, type_id):
        return self.object_registry.get(type_id, None)
