import asyncio
import json
import logging
from collections import deque
from pathlib import Path
from typing import Deque, List, Any

import aiohttp_jinja2
import jinja2
import markdown2
import numpy as np
from aiohttp import web
from configparser import ConfigParser

# Assuming flipdot library is still used and compatible
from flipdot import sign as flipdot_sign

class FlipdotServer:
    LOG_LEVEL = logging.DEBUG

    def __init__(self, host: str, port: int, sign_usb: str, sign_address: int,
                 sign_columns: int, sign_rows: int, sign_simulator: bool = False):
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.images_to_display: Deque[List[Any]] = deque()

        self.flipdot_sign = flipdot_sign(sign_usb, sign_address,
                                         sign_columns, sign_rows, simulator=sign_simulator)

    async def display_image(self, image_array: np.ndarray):
        self.flipdot_sign.render_numpy_array(np.asarray(image_array))

    async def handle_redirect(self, request: web.Request) -> web.Response:
        raise web.HTTPFound('/documentation')

    async def handle_docs(self, request: web.Request) -> web.Response:
        api_doc = Path("./README.md")
        documentation = markdown2.markdown(api_doc.read_text())
        return aiohttp_jinja2.render_template('documentation.html', request, {'content': documentation})

    async def handle_dot_array(self, request: web.Request) -> web.Response:
        if request.body_exists:
            array_body = await request.json()
            self.images_to_display.append(array_body)

        return web.json_response({"response": "image added", "images": len(self.images_to_display)})

    async def process_queue(self):
        while True:
            if self.images_to_display:
                image_array = self.images_to_display.popleft()
                self.logger.debug("Dispatching image array to flipdot display")
                await self.display_image(image_array)
            else:
                await asyncio.sleep(0.1)

    async def start_background_tasks(self, app: web.Application):
        self.logger.info("Starting background tasks")
        app['dispatch'] = asyncio.create_task(self.process_queue())

    async def cleanup_background_tasks(self, app: web.Application):
        self.logger.info("Stopping background tasks")
        app['dispatch'].cancel()
        await app['dispatch']

    async def create_app(self) -> web.Application:
        self.logger.info("Creating web app")
        app = web.Application()
        app.add_routes([
            web.get('/documentation', self.handle_docs),
            web.post('/api/dots', self.handle_dot_array),
            web.get('/', self.handle_redirect),
            web.get('/{name}', self.handle_redirect),
        ])

        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))

        app.on_startup.append(self.start_background_tasks)
        app.on_cleanup.append(self.cleanup_background_tasks)

        return app

    def run_app(self):
        self.logger.info("Instantiating server")
        web.run_app(self.create_app(), host=self.host, port=self.port)

def main():
    config = ConfigParser()
    config_file = Path('config.ini')
    if not config_file.exists():
        logging.error(f"Config file missing: {config_file}")
        return

    config.read(config_file)

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

if __name__ == '__main__':
    main()
