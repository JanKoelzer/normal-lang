from collections import deque
from mpmath import mp
import sys
import re
import os

class FileIterator:
    CHUNK_SIZE = 100
    def __init__(self, filename: str):
        self._filename = filename
        self._file = None
        self._next_chars = deque()

    def __iter__(self):
        return self

    def __next__(self):
        # Try to open the file, if this has not happened yet.
        # Stop the iteration, if the file cannot be opened/found.
        if self._file == None:
            try:
                self._file = open(self._filename, "r")
            except:
                raise StopIteration
                
        if not self._next_chars:
            chunk = self._file.read(self.CHUNK_SIZE)
            if not chunk:   
                self._file.close()
                raise StopIteration
            self._next_chars.extend(chunk)

        char = self._next_chars.popleft()
        if char == "\n":
            self._file.close()
            raise StopIteration
        return char


class SkipIterator:
    def __init__(self, source, n):
        self.source = iter(source)
        self.n = n
        self._skipped = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self._skipped:
            for _ in range(self.n):
                try:
                    next(self.source)
                except StopIteration:
                    break
            self._skipped = True
        return next(self.source)


class MpMathChunkFallback:
    def __init__(self, start_offset=0, chunk_size=20):
        self.start_offset = start_offset
        self.chunk_size = chunk_size

        self._buffer = deque()
        self._digits = ""

        self._index = start_offset

    def _init_digits(self):
        self._digits = str(mp.pi)[2:]


    def _refill(self):
        mp.dps = self._index + self.chunk_size + 2       
        self._init_digits()
        chunk = self._digits[self._index:self._index+self.chunk_size]
        self._buffer.extend(chunk)


    def __iter__(self):
        return self


    def __next__(self):
        if len(self._buffer) == 0:
            self._refill()
        self._index += 1
        result = self._buffer.popleft()
        return result


class FileThenFallback:
    def __init__(self, file_stream, fallback_stream):
        self.file = iter(file_stream)
        self.fallback = iter(fallback_stream)
        self._file_alive = True

    def __iter__(self):
        return self

    def __next__(self):
        if self._file_alive:
            try:
                return next(self.file)
            except StopIteration:
                self._file_alive = False

        return next(self.fallback)

class Pi:
    @staticmethod
    def findFile():
        pattern = re.compile(r"^(\d+)\.txt$")

        max_num = None
        max_file = None

        for filename in os.listdir("."):
            match = pattern.match(filename)
            if match:
                num = int(match.group(1))
                if max_num is None or num > max_num:
                    max_num = num
                    max_file = filename

        return max_file, max_num # might be none

        

    @staticmethod
    def stream():
        max_file, max_num = Pi.findFile()
        if max_file is None:
            return MpMathChunkFallback(start_offset=0)

        else:
            stream = FileIterator(max_file)
            stream = SkipIterator(stream, 2)

            fallback = MpMathChunkFallback(start_offset=max_num)

            stream = FileThenFallback(stream, fallback)
            return stream

if __name__ == "__main__":
    stream = Pi.stream()
    
    print("3."+"".join([str(next(stream)) for _ in range(int(sys.argv[1])) ]))



