from typing import List

from .. import ChunkReader, DataChunk, ByteIO


class BaseType:
    def __init__(self, reader: ByteIO, sam_file):
        from ...sam_file import SamFile
        self.sam_file: SamFile = sam_file

    def read(self, reader: ByteIO):
        raise NotImplementedError(f"Implement me {self.__class__.__name__}")


class DataClass(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.base_id = reader.read_int32()
        from Serious4IO.chunks.chunk_types.stmb import StructureMembers
        self.struct_member: StructureMembers = sam_file.cr.read_chunk()

    @property
    def base(self):
        return self.sam_file.get_type(self.base_id)

    def read(self, reader: ByteIO):
        storage = {}
        for member in self.struct_member.members:
            name_id = member.name_id
            storage[name_id] = member.type.read(reader)
            pass
        return storage


class Bytes(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.bytes = reader.read_int32()
        self.lbe = reader.read_int32()

    def read(self, reader: ByteIO):
        return reader.read(self.bytes)
        pass


class Unk(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.unk_0 = reader.read_int32()

    def read(self, reader: ByteIO):
        return reader.read(self.unk_0)


class BytesCount(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.unk_0 = reader.read_int32()


class ArrayOf(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.type_id = reader.read_int32()

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __str__(self):
        return f"ArrayOf<{self.type.name}>"


class CStaticArray(ArrayOf):
    def __str__(self):
        return f"CStaticArray<{self.type.name}>"


class CStaticStackArray(ArrayOf):
    def __str__(self):
        return f"CStaticStackArray<{self.type.name}>"


class CDynamicContainer(ArrayOf):
    def __str__(self):
        return f"CDynamicContainer<{self.type.name}>"

    def read(self, reader: ByteIO):
        container_chunk = self.sam_file.cr.read_chunk()
        return container_chunk


class TemplateOf(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.name = reader.read_prefixed_string()
        self.type_id = reader.read_int32()

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __str__(self):
        return f"{self.name}<{self.type.name}>"


class Pointer(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.type_id = reader.read_int32()

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __str__(self):
        return f"{self.type.name}*>"


class Ptr(Pointer):

    def __str__(self):
        return f"Ptr<{self.type.name}>"


class FixedArrayOf(BaseType):
    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.type_id = reader.read_int32()
        self.size = sam_file.cr.read_chunk()

    @property
    def type(self):
        return self.sam_file.get_type(self.type_id)

    def __str__(self):
        return f"{self.type.name}"


@ChunkReader.register_chunk
class InternalType(DataChunk):
    chunk_name = "DTTY"

    def __init__(self, reader: ByteIO, sam_file):
        super().__init__(reader, sam_file)
        self.id = reader.read_uint32()
        self.name = reader.read_prefixed_string()
        self.format = reader.read_uint32()
        self.value_type = reader.read_uint32()
        if self.value_type == 0:
            self.data = Bytes(reader, sam_file)
        elif self.value_type == 1:
            self.data = BytesCount(reader, sam_file)
        elif self.value_type == 2:
            self.data = Pointer(reader, sam_file)
        elif self.value_type == 4:
            self.data = FixedArrayOf(reader, sam_file)
        elif self.value_type == 5:
            self.data = DataClass(reader, sam_file)
        elif self.value_type == 6:
            self.data = CStaticArray(reader, sam_file)
        elif self.value_type == 7:
            self.data = CStaticStackArray(reader, sam_file)
        elif self.value_type == 8:
            self.data = CDynamicContainer(reader, sam_file)
        elif self.value_type == 11:
            self.data = Ptr(reader, sam_file)
        elif self.value_type == 13:
            self.data = Unk(reader, sam_file)
        elif self.value_type == 14:
            self.data = TemplateOf(reader, sam_file)
        else:
            raise NotImplementedError(f'Unsupported DTTY type {self.type} at {reader.tell()}')

        self.sam_file.register_type(self.id, self)

    def read(self, reader: ByteIO):
        print(f'Reading {self.name}:', end=' ')
        if self.format == 1 and self.name == 'CString':
            value = reader.read_prefixed_string()
        else:
            value = self.data.read(reader)
        print(value)
        return value

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'
