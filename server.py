import asyncio
import tornado
import json

# 取得データ格納領域
posts = {}

class MainHandler(tornado.web.RequestHandler):
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
    def get(self, post_id):
        # 1データ取得
        try:
            post_id = int(post_id)
            found_post = None

            for post in posts:
                if post['id'] == post_id:
                    found_post = post
                    break
            if found_post:
                self.write(found_post)
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid Value"})
        except Exception as e:
            self.write({'error': str(e)})
        


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/data/([0-9]+)", Data)
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())