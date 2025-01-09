import asyncio
import json
from typing import Set, Dict
from fastapi import WebSocket
from .peer import Peer
from .protocols import NetworkProtocol

class Node:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: Dict[str, Peer] = {}
        self.websocket_connections: Set[WebSocket] = set()
        self.protocol = NetworkProtocol()

    async def start(self):
        server = await asyncio.start_server(
            self._handle_connection, self.host, self.port
        )
        await server.serve_forever()

    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = Peer(reader, writer)
        self.peers[peer.id] = peer
        try:
            await self._handle_peer_messages(peer)
        finally:
            await peer.close()
            del self.peers[peer.id]

    async def _handle_peer_messages(self, peer: Peer):
        while True:
            message = await peer.receive_message()
            if message is None:
                break
            
            response = await self.protocol.handle_message(message)
            if response:
                await peer.send_message(response)

    async def broadcast(self, message: dict):
        for peer in self.peers.values():
            await peer.send_message(message)
        
        for websocket in self.websocket_connections:
            await websocket.send_json(message)

    async def connect_to_peer(self, host: str, port: int):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            peer = Peer(reader, writer)
            self.peers[peer.id] = peer
            asyncio.create_task(self._handle_peer_messages(peer))
            return True
        except:
            return False

