import asyncio
import tornado
import json
import os

# データ格納
items=[]
# items=[{"id": 1, "title": "タイトル", "content": "内容"}]

class Mainhandler(tornado.web.RequestHandler):  
    def get(self):
        self.render("index.html", items=items)

    def post(self):
        try:
            title = self.get_argument("title")
            content = self.get_argument("content")
            new_item = {"id": len(items)+1, "title": title, "content": content}
            items.append(new_item)
            self.set_status(201)
            self.render("index.html", items=items)
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))


def make_app():
    return tornado.web.Application([
        (r"/", Mainhandler),
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