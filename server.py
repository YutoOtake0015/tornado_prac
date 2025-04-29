import asyncio
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
    
class Sample(tornado.web.RequestHandler):
    def get(self):
        self.write("Sample")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/sample", Sample)
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())