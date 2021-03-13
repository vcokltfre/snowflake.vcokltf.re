from starlette.responses import HTMLResponse

class ResponseBuilder:
    def __init__(self):
        self.items = []

    def addtag(self, name: str, value: str):
        self.items.append((name, value))

    def build(self):
        og_tags = ""
        for item in self.items:
            og_tags += f"\n<meta property=\"og:{item[0]}\" content=\"{item[1]}\">"

        return HTMLResponse(f"""
            <html>
                <head>
                    {og_tags}
                </head>
            </html>
        """)
