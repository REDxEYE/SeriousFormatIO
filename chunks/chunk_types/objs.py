from typing import List

from .. import ChunkReader, DataChunk, ByteIO


class InternalObject:
    def __init__(self, reader: ByteIO, sam_file):
        from ...sam_file import SamFile
        self.sam_file: SamFile = sam_file
        self.id = reader.read_uint32()
        self.type_id = reader.read_uint32()
        self.data = {}
        self.read(reader)

    def read(self, reader: ByteIO):
        data = self.type.read(reader)
        print(data)
        self.data = data

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __repr__(self):
        return f'{self.__class__.__name__}()'


@ChunkReader.register_chunk
class InternalObjects(DataChunk):
    chunk_name = "OBJS"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.objects: List[InternalObject] = []
        for _ in range(self.count):
            internal_object = InternalObject(reader, sam_file)
            self.sam_file.add_object(internal_object.id, internal_object)
            self.objects.append(internal_object)
