### 1. Hacer puertos accesible a usuario que no sea root

Una única vez:

```
sudo usermod -a -G dialout $USER
```

y luego desloguearse y volver a loguearse

Alternativamente (a hacer cada vez):
```
chmod a+rw /dev/ttyUSB3
chmod a+rw /dev/ttyUSB4
```

### 2. Instalar dependencias de python

Una única vez (pip3 o pip):
```
pip3 install argparse readchar serial
```

### 3. Hacer el fichero ejecutable

Una única vez:
```
cd ttyfsoc
chmod +x fsoc.py
```

4. Ejecutar tx y rx
```
./fsoc.py -p /dev/ttyUSB3 -t rx
```

y en otro terminal (u ordenador)
```
./fsoc.py -p /dev/ttyUSB4 -t tx -d 100 -n 10000
```

### Parametros:
```
  -h, --help                        show this help message and exit
  -t TYPE, --type TYPE              rx or tx (default: tx)
  -p PORT, --port PORT              Serial port name (default: /dev/ttyUSB0)
  -b BAUDRATE, --baudrate BAUDRATE  Baud rate (default: 9600)
  -n FRAMES, --frames FRAMES        Number of frames (default: no limit)
  -d DELAY, --delay DELAY           Delay ms (default: 100)
  -i, --interactive                 Interactive mode
```
Por defecto hay infinitos frames.

En modo interactivo se puede escribir en el tx y se recibe lo que se escribe en el rx.



