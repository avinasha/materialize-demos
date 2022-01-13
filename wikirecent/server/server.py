#!/usr/bin/env python3

"""Tornado web server for the wikirecent demo."""

from pathlib import Path

import psycopg
import sqlparse
import tornado.ioloop
import tornado.platform.asyncio
import tornado.web
import tornado.websocket

DSN = "postgresql://materialize@materialized:6875/materialize"
PORT = 8875


class StreamHandler(tornado.websocket.WebSocketHandler):
    async def open(self, view):
        """Handle a new websocket connection by tailing the requested view
        and streaming the results back to the client."""

        conn = await psycopg.AsyncConnection.connect(DSN)
        cursor = conn.cursor()

        inserted = []
        deleted = []
        query = f"TAIL {view} WITH (PROGRESS)"
        async for (timestamp, progressed, diff, *columns) in cursor.stream(query):
            # The progressed column serves as a synchronization primitive indicating that all
            # rows for an update have been read. We should publish this update.
            if progressed:
                self.write_message(
                    {
                        "deleted": deleted,
                        "inserted": inserted,
                        "timestamp": int(timestamp),
                    }
                )
                inserted = []
                deleted = []
                continue

            # Simplify our implementation by creating "diff" copies of each row instead
            # of tracking counts per row
            if diff < 0:
                deleted.extend([columns] * abs(diff))
            elif diff > 0:
                inserted.extend([columns] * diff)
            else:
                raise ValueError(
                    f"Bad data in TAIL: {timestamp}, {progressed}, {diff}, {columns}"
                )


def main():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            conn.autocommit = True
            for statement in sqlparse.split(Path("views.sql").read_text()):
                cur.execute(statement)

    app = tornado.web.Application(
        handlers=[
            tornado.web.url(r"/api/stream/(.*)", StreamHandler),
            tornado.web.url(
                r"/(.*)",
                tornado.web.StaticFileHandler,
                {"path": Path(__file__).parent, "default_filename": "index.html"},
            ),
        ],
        debug=True,
    )
    app.listen(PORT)
    print(f"Listening on port {PORT}...")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
