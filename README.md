
# Algorithmic Operation Research

* [Homework 1](Homework_1/homework.pdf)
* [Homework 2](Homework_2/homework.pdf)
* [Homework 3](Homework_3/homework.pdf)

## Contributors

* Σιώρος Βασίλειος       - 1115201500144
* Ανδρινοπούλου Χριστίνα - 1115201500006

# LaTeX Project Base Generation

```bash
usage: generate.py [-h] [-l LOAD] -s SAVE [-d] [-o]

LaTeX Project Base Generation

optional arguments:
  -h, --help            show this help message and exit
  -l LOAD, --load LOAD  specify the input file
  -s SAVE, --save SAVE  specify the output file
  -d, --directory       make parent directories as needed
  -o, --overwrite       enable overwriting
```

## Example

```bash
python generate.py -s ".\Homework_3\homework.tex" -l "..\Algorithmic Operation Research_hw_3.pdf" -d -o
```

