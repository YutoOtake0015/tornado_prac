import asyncio
import tornado
import json
import os

# データ格納
items=[]
# items=[{"id": 1, "title": "タイトル", "content": "内容"}]

class ItemHandler(tornado.web.RequestHandler):  
    def get(self):
        self.write({"items": items})

    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            new_item = {"id": len(items)+1, **data}
            items.append(new_item)
            self.set_status(201)
            self.write(json.dumps(new_item))
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


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