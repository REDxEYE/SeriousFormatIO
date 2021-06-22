from .. import ChunkReader, DataChunk, ByteIO


@ChunkReader.register_chunk
class CTSEMetaChunk(DataChunk):
    chunk_name = "CTSE"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        reader.skip(4)
        self.hash = reader.read_uint32()
        self.unk_0 = reader.read_uint32()
        self.version = reader.read_prefixed_string()
