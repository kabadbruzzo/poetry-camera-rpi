from escpos import printer

## initialize printer
p = printer.Serial("/dev/ttyS0", baud_rate=9600) ## todo: change serial code
#print("printer initialized")
p.text("Hola skurki \n")
#p.qr("Te amo mucho, como dos a la 300esima")
p.text("\n \n \n")
#print("text printed")
p.image()
