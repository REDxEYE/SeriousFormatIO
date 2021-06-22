from . import ByteIO


class DataChunk:
    chunk_name = "ERROR"

    def __init__(self, reader: ByteIO, sam_file):
        from ..sam_file import SamFile
        self.sam_file: SamFile = sam_file
        pass
