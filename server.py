import asyncio
import tornado
import json
import os

# データ格納
items=[]

class ItemHandler(tornado.web.RequestHandler):  
    def get(self):
        self.write(json.dumps({"items": list(items)}))

def make_app():
    return tornado.web.Application([
        (r"/items", ItemHandler),
    ],
        template_path=os.path.join(os.getcwd(),"templates"),
        static_path=os.path.join(os.getcwd(),"static"),
    )

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())