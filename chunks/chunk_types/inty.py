from typing import List

from .. import ChunkReader, DataChunk, ByteIO
from .dtty import InternalType


@ChunkReader.register_chunk
class InternalTypes(DataChunk):
    chunk_name = "INTY"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.types: List[InternalType] = []
        for _ in range(self.count):
            data_type = sam_file.cr.read_chunk()
            # self.sam_file.register_type(internal_type)
            self.types.append(data_type)
