from typing import List

from .. import ChunkReader, DataChunk, ByteIO


class ExternalType:
    def __init__(self, reader: ByteIO):
        self.id = reader.read_uint32()
        self.path = reader.read_prefixed_string()

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'


@ChunkReader.register_chunk
class ExternalTypes(DataChunk):
    chunk_name = "EXTY"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.types: List[ExternalType] = []
        for _ in range(self.count):
            external_type = ExternalType(reader)
            self.sam_file.register_type(external_type.id, external_type)
            self.types.append(external_type)
