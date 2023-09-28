import socket
import json

def enviarMensajeSocket(udp_socket, node_adress, message ):
    udp_socket.sendto(message.encode(),(node_adress[0],node_adress[1]))

def recibirMensajeSocket(udp_socket):
    data, addr = udp_socket.recvfrom(1024)
    return data.decode(), addr 

def enviarMensajeJson(udp_socket, node_adress, message):
    enviarMensajeSocket(udp_socket, node_adress, json.dumps(message))

def multicastMensajeJson(udp_socket, message, peers):
    for a_peer in peers.values():
        enviarMensajeJson(udp_socket, a_peer, message)