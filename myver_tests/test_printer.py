from escpos import printer
import usb

# find your printer vendor id and product id, needed to initialize printer via usb

busses = usb.busses()
for bus in busses:
    devices = bus.devices
    for dev in devices:
        print("Device:", dev.filename)
        print("    idVendor: %d (0x%04x)" %(dev.idVendor, dev.idVendor))
        print("    idProduct: %d (0x%04x)" %(dev.idProduct, dev.idProduct))


## initialize printer
p = printer.Usb(0x28e9, 0x0289, in_ep=0, out_ep=0x03) ## todo: change serial code
p.text("Hello World \n")
