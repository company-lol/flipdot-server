from flipdot import sign as flipdot_sign
import numpy as np
import json
import logging
import markdown2
import sys
from os import path

from collections import deque
from concurrent.futures import ThreadPoolExecutor
import configparser

import asyncio

from aiohttp import web
import aiohttp_jinja2
import jinja2

from aiojobs.aiohttp import setup, spawn
from aiojobs.aiohttp import atomic




class FlipdotServer:

    LOG_LEVEL = logging.DEBUG

    def __init__(self, host, port, sign_usb, sign_address, sign_columns, sign_rows, sign_simulator=False):
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.loop = asyncio.get_event_loop()
        self.images_to_display = deque([])

        self.flipdot_sign = flipdot_sign(sign_usb, sign_address,
                          sign_columns, sign_rows, simulator=sign_simulator)

    #Image display helper
    async def display_image(self, image_array):
        image_array = np.asarray(image_array)
        self.flipdot_sign.render_numpy_array(image_array)
        
    # Route Handlers
    async def handle_redirect(self, request):
        raise web.HTTPFound('/documentation')

    async def handle_docs(self, request):
        api_doc = "./README.md"
        documentation = markdown2.markdown(open(api_doc, 'r').read())
        html  = """
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.css" integrity="sha256-jyWGtg7ocpUge8Zt/LotwFtPMWE23n7jgkHHw/Ejh+U=" crossorigin="anonymous" />
                <title>Flipdot API Doc</title>
            </head>
            <body class="markdown-body">""" + documentation + """</body>
        </html>"""
        return web.Response(body=html, content_type="text/html")

    async def handle_dot_array(self, request):
        if request.body_exists:
            array_body = await request.read()
            image_array = json.loads(array_body.decode("utf-8"))
            self.images_to_display.append(image_array)
        
        data = {"response:":"image added", "images":len(self.images_to_display)}
        return web.json_response(data)

    # Background tasks helpers

    async def process_queue(self):
        while True:
            if self.images_to_display:
                image_array = self.images_to_display.popleft()
                self.logger.debug("Dispatching image array to flipdot display")
                await self.display_image(image_array)
            else:
                await asyncio.sleep(0.1)

    async def start_background_tasks(self, app):
        self.logger.info("Starting background tasks")
        app['dispatch'] = app.loop.create_task(self.process_queue())

    async def cleanup_background_tasks(self, app):
        self.logger.info("Stopping background tasks")
        app['dispatch'].cancel()
        await app['dispatch']

    # Create App
    async def create_app(self):
        self.logger.info("Creating web app")
        app = web.Application()
        routes = [
            web.get('/documentation', self.handle_docs),  # documentation
            web.post('/api/dots', self.handle_dot_array),  # dots api endpoint
            web.get('/', self.handle_redirect),
            web.get('/{name}', self.handle_redirect), ]
        
        app.add_routes(routes)
        aiohttp_jinja2.setup(app,
                             loader=jinja2.FileSystemLoader('./templates'))

        return app

    def run_app(self):
        self.logger.info("Instantiating server")
        loop = self.loop
        app = loop.run_until_complete(self.create_app())
        app.on_startup.append(self.start_background_tasks)
        app.on_cleanup.append(self.cleanup_background_tasks)
        web.run_app(app, host=self.host, port=self.port)





#set up sign
sign_usb = "/dev/ttyUSB0"
sign_columns = 96
sign_rows = 16
sign_address = 1

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    if path.exists(config_file):
        config.read(config_file)
    else:
        logging.error("Config file missing: {}".format(config_file))
        sys.exit(1)

    server = FlipdotServer(
        host=config.get('SERVER', 'HOST'),
        port=config.getint('SERVER', 'PORT'),
        sign_usb=config.get('FLIPDOTSIGN', 'USB'),
        sign_address=config.getint('FLIPDOTSIGN', 'ADDRESS'),
        sign_columns=config.getint('FLIPDOTSIGN', 'COLUMNS'),
        sign_rows=config.getint('FLIPDOTSIGN', 'ROWS'),
        sign_simulator=config.getboolean('FLIPDOTSIGN', 'SIMULATOR')
        )
    server.run_app()
