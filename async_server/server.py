import asyncio

import uvloop


def endpoint():
    response = "HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello, World"
    return response


async def handle_client(reader, writer):
    while True:
        request_data = await reader.read(1000)
        if not request_data:
            break


        response = endpoint()
        writer.write(response.encode())
        await writer.drain()
    
        print("Response: 'Hello world'")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8080
    )

    async with server:
        print("server started")
        await server.serve_forever()


if __name__ == '__main__':
    uvloop.run(main())