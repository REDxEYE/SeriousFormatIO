from typing import List

from .. import ChunkReader, DataChunk, ByteIO


class ResourceFileLink:
    def __init__(self, reader: ByteIO):
        self.id = reader.read_uint32()
        self.flags = reader.read_uint32()
        self.path = reader.read_prefixed_string()


@ChunkReader.register_chunk
class ResourceFileChunk(DataChunk):
    chunk_name = "RFIL"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.links: List[ResourceFileLink] = []
        for _ in range(self.count):
            link = ResourceFileLink(reader)
            self.links.append(link)
