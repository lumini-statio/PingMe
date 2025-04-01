import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket, path):
    # Agregar nuevo cliente
    connected_clients.add(websocket)
    print(f"Nuevo cliente conectado. Total: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"Mensaje recibido: {message}")
            
            # Reenviar el mensaje a todos los clientes conectados
            for client in connected_clients:
                if client != websocket:  # Opcional: no reenviar al remitente
                    await client.send(f"Usuario dice: {message}")
                    
    finally:
        # Eliminar cliente cuando se desconecta
        connected_clients.remove(websocket)
        print(f"Cliente desconectado. Total: {len(connected_clients)}")

async def main():
    async with websockets.serve(handle_client, "localhost", 8000):
        print("Servidor WebSocket iniciado en ws://localhost:8002")
        await asyncio.Future()  # Ejecutar indefinidamente

if __name__ == "__main__":
    asyncio.run(main())