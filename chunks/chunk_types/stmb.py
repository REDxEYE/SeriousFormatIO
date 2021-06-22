from typing import List

from .. import ChunkReader, DataChunk, ByteIO
from .dtty import InternalType


class Member:
    def __init__(self, reader: ByteIO, sam_file):
        from ...sam_file import SamFile
        self.sam_file: SamFile = sam_file
        self.name_id = reader.read_int32()
        self.type_id = reader.read_int32()

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.type.name})'


@ChunkReader.register_chunk
class StructureMembers(DataChunk):
    chunk_name = "STMB"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.count = reader.read_uint32()
        self.members: List[Member] = []
        for _ in range(self.count):
            internal_type = Member(reader, sam_file)
            # self.sam_file.register_type(internal_type)
            self.members.append(internal_type)
