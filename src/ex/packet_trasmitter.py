from hashlib import md5
from json import dumps, loads
import socket as sk

class Packet:
    '''
    This class model a packet of data sendable with socket
    is possible to read data as bytes or string
    '''
    def __init__(self, data : bytes | str) -> None:
        
        if type(data) == str:
            data = data.encode()
        
        self.data = data.hex()
        self.hash = self.hash_fun(data)

    def to_json(self) -> str:
        '''
        Return an json rappresentation
        '''
        return dumps({"data" : self.data, "hash" : self.hash})
    
    def to_byte(self) -> bytes:
        '''
        Convert to a json rappresentation then into bytes
        '''
        return self.to_json().encode()
    
    def __str__(self):
        '''
        Convert data to str
        '''
        return bytes.fromhex(self.data).decode()
    
    @classmethod
    def by_json(cls, json : str):
        '''
        Checks if data and hash on that is the same, next build a packet on that data
        '''
        hextdigest = json["hash"]
        rtr = cls(bytes.fromhex(json['data']))

        if rtr.hash != hextdigest:
            raise TypeError("Data is corrupted")
        
        return rtr
    
    @staticmethod
    def hash_fun(data : str):
        '''
        Function used to hash data (md5)
        '''
        return md5(data).hexdigest()


class PacketTransmitter:
    '''
    This class model a calss that is able to send and recive Packet
    '''
    def __init__(self, buffer_size : int=1024, bind : bool=False, bind_addr : tuple[str, int]=None) -> None:
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        
        if bind:
            if bind_addr is None:
                raise TypeError("Address can't be None if you need to bind the addres")

            self.socket.bind(bind_addr)
        
        self.buffer_size = buffer_size
    
    def send_data(self, data : str | bytes, address : tuple[str, int]) -> int:
        '''
        Send a string or bytes
        '''
        return self.socket.sendto(Packet(data).to_byte(), address)

    def _get_packet(self) -> tuple[Packet, tuple[str, int]]:
        '''
        Recive a generic Packet
        '''
        data, addr = self.socket.recvfrom(self.buffer_size)
        
        data = loads(data.decode())

        return Packet.by_json(data), addr
    
    def get_data(self, timeout_error : str="Timeout reaced", timeout_end="\n", time_out_max=3, type_error_fun=print, to_str : bool=True) -> tuple[str | bytes | None, tuple[str, int] | None]:
        '''
        Recive a generic Packet, but it doesn't stop after a timeout,
        it simply print the message. If a data corruption is present
        a functtion passed as parameter will be executed. There's the
        possibility to not convert recived data into string
        '''
        cnt = 0
        while cnt < time_out_max:
            try:
                package, addr = self._get_packet()
                break
            
            except sk.timeout:
                print(timeout_error, end=timeout_end)
                cnt += 1
            
            except TypeError as e:
                type_error_fun(e)

        if cnt == time_out_max:
            return None, None

        if to_str:
            return str(package), addr
        
        else:
            return bytes.fromhex(package.data), addr
    
    def wait_for_command(self) -> dict:
        data = ''
        addr = ''
        while data is not None and addr is not None:
            data, addr = self._get_packet()
        d = loads(data)
        d.update({"address" : addr})
        return d

    def close(self):
        '''
        close the conncetion
        '''
        self.socket.close()