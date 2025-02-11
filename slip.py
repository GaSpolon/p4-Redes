class CamadaEnlace:
    ignore_checksum = False

    def __init__(self, linhas_seriais):
        self.enlaces = {}
        self.callback = None
        for ip_outra_ponta, linha_serial in linhas_seriais.items():
            enlace = Enlace(linha_serial)
            self.enlaces[ip_outra_ponta] = enlace
            enlace.registrar_recebedor(self._callback)

    def registrar_recebedor(self, callback):
        self.callback = callback

    def enviar(self, datagrama, next_hop):
        self.enlaces[next_hop].enviar(datagrama)

    def _callback(self, datagrama):
        if self.callback:
            self.callback(datagrama)

class Enlace:
    def __init__(self, linha_serial):
        self.linha_serial = linha_serial
        self.buffer = b''
        self.linha_serial.registrar_recebedor(self.__raw_recv)

    def registrar_recebedor(self, callback):
        self.callback = callback

    def enviar(self, datagrama):
        datagrama = datagrama.replace(b'\xDB', b'\xDB\xDD')
        datagrama = datagrama.replace(b'\xC0', b'\xDB\xDC')
        datagrama_res = b'\xC0' + datagrama + b'\xC0'
        self.linha_serial.enviar(datagrama_res)

    def __raw_recv(self, dados):
        split_separador = b'\xC0'
        partes = dados.split(split_separador)

        if not partes:
            return

        self.buffer += partes[0]

        for segmento in partes[1:]:
            if self.buffer:
                datagrama = self.buffer.replace(b'\xdb\xdc', split_separador).replace(b'\xdb\xdd', b'\xdb')
                try:
                    self.callback(datagrama)
                except:
                    import traceback
                    traceback.print_exc()
                finally:
                    self.buffer = b''

            self.buffer = segmento