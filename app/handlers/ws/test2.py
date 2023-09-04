import asyncio
import os
import json
import aiohttp.web

class ChatRoom():
    def __init__(self):
        self.sockets = {
            "sockets": []
        }



    async def room_chat(self, request):
        ws = aiohttp.web.WebSocketResponse()


        available = ws.can_prepare(request)

        # #todo 如果为准备 做些什么
        # if not available:
        #     pass

        await ws.prepare(request)


        status_task = request.app.loop.create_task(
            self.work(ws)
        )


        try:
            # self.sockets['sockets'].append(ws)
            # for ws in self.sockets['sockets']:
            #     await ws.send_str("someone joined")
            self.sockets['sockets'].append(ws)
            print(self.sockets, "#####")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == "close":
                        await ws.close()
                    else:
                        #todo actual things
                        # await status_task
                        print ("@@@@@")
            print ("end")

            return ws
        except Exception:
            import traceback
            traceback.print_exc()
        finally:
            print ('finally')
            self.sockets['sockets'].remove(ws)
            status_task.cancel()
            await ws.close()
            return ws


    async def work(self, ws):
        while True:
            error_server_list = await self._query_error_servers()
            ws.send_json(error_server_list)
            await asyncio.sleep(2)


    async def _query_error_servers(self):
        #todo 从数据库查询错误服务器列表返回
        error_server_list = []
        return error_server_list
