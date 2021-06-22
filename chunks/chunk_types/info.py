from .. import ChunkReader, DataChunk, ByteIO

@ChunkReader.register_chunk
class InfoChunk(DataChunk):
    chunk_name = "INFO"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.edit_data_stripped = reader.read_uint32()
        self.resource_files_count = reader.read_uint32()
        self.ident_count = reader.read_uint32()
        self.types_count = reader.read_uint32()
        self.object_count = reader.read_uint32()
