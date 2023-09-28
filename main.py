import threading
import socket
import sys 
import json 
import time
import udp as udp_util 

class Node:
    seed_adress = ("127.0.0.1", 10001)
    peers = {}
    node_id = ""
    udp_socket = {}

    def inicializa_peer(self):
        udp_util.enviarMensajeJson(self.udp_socket, self.seed_adress,{
            "type":"nuevo_peer",
            "data":self.node_id
        })

    def recibir(self):
        while 1:
            data, addr = udp_util.recibirMensajeSocket(self.udp_socket)
            action = json.loads(data)
            if action['type'] == 'nuevo_peer':
                print("Nuevo peer registrado en la red con id: " + action['data'])
                self.peers[action['data']]= addr
                udp_util.enviarMensajeJson(self.udp_socket, addr, {
                "type":'notifica_peers',
                "data":self.peers
                })         

            if action['type'] == 'notifica_peers':
                
                self.peers.update(action['data'])
                udp_util.multicastMensajeJson(self.udp_socket, {
                    "type":"registra_peer",
                    "data": self.node_id
                },self.peers) 

            if action['type'] == 'registra_peer':

                print("Se registro nuevo peer en la red con id: " + action['data'])
                self.peers[action['data']]= addr   

            if action['type'] == 'input':
                print(action['data'])  

            if action['type'] == 'salir':
                if(self.node_id == action['data']):
                    time.sleep(0.5) 
                    break;
                value, key = self.peers.pop(action['data'])
                print( action['data'] + " ha abandonado la red.")          

    def enviar(self):
        while 1: 
            msg_input = input(">:")
            if msg_input == "salir":
                udp_util.multicastMensajeJson(self.udp_socket, {
                    "type":"salir",
                    "data":self.node_id
                },self.peers)
                break     
            if msg_input == "imprime_nodos":
                print(self.peers) 
                continue      
            l = msg_input.split()
            if l[-1] in self.peers.keys():
                nodo_destino = self.peers[l[-1]]
                msg_input_sin_destino = ' '.join(l[:-1])
                udp_util.enviarMensajeJson(self.udp_socket, nodo_destino,{
                    "type":"input",
                    "data":msg_input_sin_destino
                })      
            else :
                udp_util.multicastMensajeJson(self.udp_socket, {
                    "type":"input",
                    "data":msg_input
                },self.peers)
                continue 

def main():
    localhost = "127.0.0.1"
    port = int(sys.argv[1])
    node_adress = (localhost ,port)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(node_adress)
    peer = Node()
    peer.node_id = sys.argv[2]
    peer.udp_socket = udp_socket
    peer.inicializa_peer()
    thread_recepcion = threading.Thread(target=peer.recibir, args=())
    thread_envio = threading.Thread(target=peer.enviar, args=())

    thread_recepcion.start()
    thread_envio.start()


if __name__ == '__main__':
    main()           
