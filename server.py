import asyncio
import tornado
import json
import os

# 取得データ格納領域
posts = {}
memo_list=[]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", memo_list=memo_list)
    
    def post(self):
        body = self.get_argument('body')
        memo_list.append(body)
        self.render("index.html", memo_list=memo_list)
        

class Get(tornado.web.RequestHandler):
    async def get(self):
        # 複数データ取得
        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch('https://jsonplaceholder.typicode.com/posts/')
            if response.error:
                self.set_status(500)
                self.write({"error": str(response.error)})
            else:
                global posts 
                posts = json.loads(response.body.decode('utf-8'))
                self.write({'ok': response.code})
        finally:
            http_client.close()
    
class Data(tornado.web.RequestHandler):
    def get(self, get_id):
        # 1データ取得
        try:
            get_id = int(get_id)
            found_post = None

            for post in posts:
                if post['id'] == get_id:
                    found_post = post
                    break
            if found_post:
                self.write(found_post)
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid Value"})
        except Exception as e:
            self.write({'error': str(e)})     

class Create(tornado.web.RequestHandler):
    def post(self):
        post_id = max([post['id'] for post in posts ])
        print(post_id)
        posts['id'] = post_id
        self.write({'ok': ""})

class Delete(tornado.web.RequestHandler):
    def delete(self, delete_id):
        delete_id = int(delete_id)
        global posts
        posts = [post for post in posts if post['id'] != delete_id]
        self.write({'post': posts})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/get", Get),
        (r"/data/([0-9]+)", Data),
        (r"/create", Create),
        (r"/delete/([0-9]+)", Delete),
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