import humanize
from fastapi import FastAPI
from collections import namedtuple
from datetime import datetime, timedelta

from src.response import ResponseBuilder


Snowflake = namedtuple('Snowflake', ("timestamp", "worker", "process", "increment"))

app = FastAPI(docs_url=None)

def deconstruct(snowflake: int) -> Snowflake:
    timestamp = (snowflake >> 22) + 1420070400000
    worker = (snowflake & 0x3E0000) >> 17
    process = (snowflake & 0x1F000) >> 12
    increment = snowflake & 0xFFF

    return Snowflake(timestamp, worker, process, increment)

def getsfdata(sf: Snowflake) -> str:
    data = f"Timestamp: {sf.timestamp}\n"
    data += f"Worker: {sf.worker}\n"
    data += f"Process: {sf.process}\n"
    data += f"increment: {sf.increment}"

    return data

@app.get("/{snowflake}")
async def get_sf(snowflake: int):
    sf = deconstruct(snowflake)

    date = datetime.fromtimestamp(sf.timestamp // 1000)

    rb = ResponseBuilder()
    rb.addtag("title", f"Snowflake: {snowflake}")
    desc = "**__Raw Data:__**\n"
    desc += f"{getsfdata(sf)}\n\n"
    desc += f"**__ISO 8601 Format:__**\n"
    desc += f"{date.isoformat()}\n\n"
    desc += f"**__Human Time:__**\n"
    desc += f"{humanize.naturaldate(date.date())}"
    rb.addtag("description", desc)

    return rb.build()

@app.get("/compare/{snowflake_1}/{snowflake_2}")
async def get_sf(snowflake_1: int, snowflake_2: int):
    sf1 = deconstruct(snowflake_1)
    sf2 = deconstruct(snowflake_2)

    rb = ResponseBuilder()
    rb.addtag("title", f"Compare: {snowflake_1} | {snowflake_2}")
    desc = f"**__Data for {snowflake_1}:__**\n"
    desc += f"{getsfdata(sf1)}\n\n"
    desc += f"**__Data for {snowflake_2}:__**\n"
    desc += f"{getsfdata(sf2)}\n\n"
    desc += f"**__Difference:__**\n"
    desc += f"{humanize.naturaldelta((max(sf1.timestamp, sf2.timestamp) // 1000) - (min(sf1.timestamp, sf2.timestamp) // 1000))}"
    rb.addtag("description", desc)

    return rb.build()