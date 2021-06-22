from typing import List

from .. import ChunkReader, DataChunk, ByteIO


class Identifier:
    def __init__(self, reader: ByteIO):
        self.id = reader.read_uint32()
        self.path = reader.read_prefixed_string()

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'


@ChunkReader.register_chunk
class Idents(DataChunk):
    chunk_name = "IDNT"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.identifiers: List[Identifier] = []
        for _ in range(self.count):
            link = Identifier(reader)
            self.identifiers.append(link)
