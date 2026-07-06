# normal-lang

Interpreter for the NORMAL programming language.

Code your program by selecting a number, for example `836`, then run the resulting code with an argument like so
```
python3 Interpreter.py 836 3
```
This example computes the square of your argument, so the result is 9.

See [http://normal-lang.kölzer.eu/](http://normal-lang.kölzer.eu/) for specs and documentation.

## Installation and Dependencies

The NORMAL interpreter makes use of Python 3, which is pre-installed on a lot of machines. Check [Python 3](https://www.python.org/), if the following fails.

1. Install MpMath (≥ 1.4). You may want to use `apt install python3-mpmath` or `pip install mpmath`.  MpMath is BSD licensed, see [https://mpmath.org/](https://mpmath.org/).
2. Download NORMAL. You can download the [zip file](https://github.com/JanKoelzer/normal-lang/archive/refs/heads/main.zip) or clone the repository: `git clone https://github.com/JanKoelzer/normal-lang.git`.
3. Start coding with NORMAL: `python3 Interpreter.py 26030 6`

## Performance

If your code uses large numbers (for example > 5), then NORMAL computes digits of of Pi on-demand. This can become slow. You can use pre-calculated digits like the ones you can find on [https://pilookup.com/de/download.html](https://pilookup.com/de/download.html). Download any of the files and copy it to the NORMAL directory. Name it to N.txt, where N is the number of digits ("3." not counted). NORMAL will detect the file and use those digits. (See 5.txt for format and naming convention.)
