import asyncio
import logging
from datetime import datetime
from aiowebsocket.converses import AioWebSocket


async def startup(uri):
    async with AioWebSocket(uri) as aws:
        # 初始化 aiowebsocket库的链接类
        converse = aws.manipulator
        # 设定需要传送的信息
        message = b'WTF'
        while True:
            # 不断地向服务器发送信息，并打印输出信息时间和信息内容
            await converse.send(message)
            mes = await converse.receive()
            print(mes)


if __name__ == '__main__':
    remote = 'wss://echo.websocket.org'
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))

    except KeyboardInterrupt as exc:
        logging.info('Quit')
