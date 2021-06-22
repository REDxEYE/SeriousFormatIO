from typing import List

from .. import ChunkReader, DataChunk, ByteIO


class InternalObjectType:
    def __init__(self, reader: ByteIO, sam_file):
        from ...sam_file import SamFile
        self.sam_file: SamFile = sam_file
        self.id = reader.read_uint32()
        self.type_id = reader.read_uint32()

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __repr__(self):
        return f'{self.__class__.__name__}()'


@ChunkReader.register_chunk
class Container(DataChunk):
    chunk_name = "DCON"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.size = reader.read_uint32()
        self.unk_0 = reader.read_uint32()
        self.unk_1 = reader.read_uint32()
        self.unk_2 = reader.read_uint32()
        self.unk_3 = reader.read_uint32()
        self.unk_4 = reader.read_uint32()
        self.unk_5 = reader.read_uint32()
        self.unk_6 = reader.read_uint32()
        # self.objects: List[InternalObjectType] = []
        # for _ in range(self.count):
        #     internal_object = InternalObjectType(reader, sam_file)
        #     self.sam_file.add_object(internal_object.id, internal_object)
        #     self.objects.append(internal_object)

    def read(self, reader: ByteIO):
        pass
