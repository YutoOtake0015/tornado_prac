import asyncio
import tornado
import json
import os
import db

# データ格納
items=[]
# items=[{"id": 1, "title": "タイトル", "content": "内容"}]

class Mainhandler(tornado.web.RequestHandler):  
    def get(self):
        items = db.get_items()
        self.render("index.html", items=items)

    def post(self):
        try:
            title = self.get_argument("title")
            content = self.get_argument("content")
            db.insert_item(title,content)
            items = db.get_items()
            self.set_status(201)
            self.render("index.html", items=items)
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))

class ItemHandler(tornado.web.RequestHandler):
    def get(self, item_id):
        try:
            item_id = int(item_id)
            item = db.get_item(item_id)
            print("item", item)

            # for i in items:
            #     if i['id'] == int(item_id):
            #         item = i
            #         break
            self.render("edit.html", item=item)
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))

    def post(self, item_id):
        try:
            item_id = int(item_id)
            if "/delete" in self.request.path:
                db.delete_item(item_id)
                items = db.get_items()
                # global items
                # items = [i for i in items if i['id'] != item_id]
            else:
                item_id = int(item_id)
                title = self.get_argument("title")
                content = self.get_argument("content")
                
                # for i in items:
                #     if i["id"] == item_id:
                #         item = i
                #         break

                # item["title"] = title
                # item["content"] = content
                db.update_item(item_id,title,content)

            self.set_status(200)
            self.redirect("/") 
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))

def make_app():
    return tornado.web.Application([
        (r"/", Mainhandler),
        (r"/items/([0-9]+)", ItemHandler),
        (r"/items/([0-9]+)/delete", ItemHandler),
    ],
        template_path=os.path.join(os.getcwd(),"templates"),
        static_path=os.path.join(os.getcwd(),"static"),
    )

async def main():
    db.init_db()
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())