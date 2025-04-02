import asyncio
import websockets
import os
import ssl

connected_clients = []

async def handle_client(websocket, path):
    # Agregar nuevo cliente
    connected_clients.append(websocket)
    print(f"Nuevo cliente conectado. Total: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"Mensaje recibido: {message}")
            
            # Reenviar el mensaje a todos los clientes conectados
            for client in connected_clients:
                await client.send(f"Usuario dice: {message}")
                    
    finally:
        # Eliminar cliente cuando se desconecta
        connected_clients.remove(websocket)
        print(f"Cliente desconectado. Total: {len(connected_clients)}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("cert.pem", "key.pem")

async def main():
    async with websockets.serve(handle_client, "localhost", 8002, ssl=ssl_context):
        print("Servidor WebSocket iniciado en wss://localhost:8002")
        await asyncio.Future()

# clients = []

# async def handle_message(websocket, path):
#     global clients
#     global fastest_time
#     message = await websocket.recv()

#     if message == 'buzz':
#         response_time = asyncio.get_event_loop().time()
#         clients.append([websocket, response_time])

#         if len(clients) == 1:
#             await websocket.send('first place!')
#             fastest_time = response_time
#         else:
#             time = round(response_time -fastest_time, 2)
#             await websocket.send(f'Response time {time} sec slower')


# async def main():
#     async with websockets.serve(handle_message, 'localhost', 8002):
#         print("Servidor WebSocket iniciado en ws://localhost:8002")
#         print(os.environ.get('HTTP_PROXY'))
#         await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())