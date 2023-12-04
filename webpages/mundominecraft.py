from WebsiteBaseHandler import BaseHandler

# http://mundo-minecraft.com:3000/player/8c5747ed-dfd9-469c-9c1e-a393a75ee92f

class MundoMinecraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        return super().parse_website_html(response_text, url)
