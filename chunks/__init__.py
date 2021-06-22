import importlib
from pathlib import Path
from typing import Type

from ..utils.byte_io_sam import ByteIO

from .chunk import DataChunk


class MultipleChunkClassDefinition(Exception):
    pass


class ChunkReader:
    _chunk_hanlders = {}

    @classmethod
    def register_chunk(cls, chunk_class: Type[DataChunk]):
        if chunk_class.chunk_name in cls._chunk_hanlders:
            raise MultipleChunkClassDefinition(
                f"Multiple definitions of {chunk_class.__name__}({chunk_class.chunk_name}) class")
        cls._chunk_hanlders[chunk_class.chunk_name] = chunk_class
        return chunk_class

    def __init__(self, reader: ByteIO, sam_file):
        from ..sam_file import SamFile
        self.sam_file: SamFile = sam_file
        self.reader = reader

    def read_chunk(self):
        if not self.reader:
            return None
        key = self.reader.read_ascii_string(4)
        if key in self._chunk_hanlders:
            chunk = self._chunk_hanlders[key](self.reader, self.sam_file)
            return chunk
        raise NotImplementedError(f'Unknown chunk {key} at {self.reader.tell() - 4}')


from .chunk_types import (
    ctsemeta,
    msgs,
    info,
    rfil,
    idnt,
    exty,
    inty,
    dtty,
    stmb,
    adim,
    exob,
    obty,
    edty,
    objs,
    dcon,
)
