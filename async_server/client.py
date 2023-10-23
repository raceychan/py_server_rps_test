import asyncio
from time import perf_counter

import uvloop


async def send_requests(total_requests):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
    
    for _ in range(total_requests):
        request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n"
        writer.write(request.encode())
        await writer.drain()
        response = await reader.read(1000)
        
        if not response:
            break
    
    writer.close()
    await writer.wait_closed()

async def send_request(conn_num: int, req_per_conn: int):
    requests= {asyncio.create_task(send_requests(req_per_conn)) for _ in range(conn_num)}
    await asyncio.gather(*requests)



async def main():
    conn_num = 10
    req_per_conn = 10000
    
    start_time = perf_counter()
    await send_request(conn_num, req_per_conn)
    end_time = perf_counter()
    
    total_time = end_time - start_time
    total_requests = conn_num * req_per_conn
    rps = round(total_requests / total_time)

    print(f"Send {total_requests} requests using {conn_num} sessions in a single core,  spent {total_time:.2f} seconds, which converts to {rps} rps")
    


if __name__ == '__main__':
    uvloop.run(main())
