from escpos import printer

## initialize printer
p = printer.Serial("/dev/tty0") ## todo: change serial code
p.test("Hello World \n")
