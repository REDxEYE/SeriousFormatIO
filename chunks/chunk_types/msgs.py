from .. import ChunkReader, DataChunk, ByteIO


@ChunkReader.register_chunk
class MessageChunk(DataChunk):
    chunk_name = "MSGS"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.size = reader.read_uint32()
        self.data = reader.read(self.size)
