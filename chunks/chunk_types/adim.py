from .. import ChunkReader, DataChunk, ByteIO


@ChunkReader.register_chunk
class DimensionsInfo(DataChunk):
    chunk_name = "ADIM"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.sizes = [reader.read_uint32() for _ in range(self.count)]
