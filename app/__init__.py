# Copyright 2025, OpenRemote Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager

from fastmcp import FastMCP
from openremote_client.schemas import ExternalServiceSchema
from starlette.templating import Jinja2Templates

from services.openremote_service import init_openremote_service
from .config import config
from .health import init_health
from .services import init_services
import json

mcp = FastMCP("OpenRemote Tools")

@mcp.custom_route("/", methods=['GET'])
async def homepage(request):
    return Jinja2Templates(directory="templates").TemplateResponse(
        "index.html",
        {
            "request": request,
            "tools": await mcp.get_tools(),
            "app_homepage_url": config.app_homepage_url,
            "json": json
        }
    )

init_health(mcp)

app = mcp.http_app()


def extend_lifespan(original_lifespan):
    """
    Wraps FastMCP's existing lifespan to add custom background tasks.
    Preserves the session manager lifespan while adding custom logic.
    """
    @asynccontextmanager
    async def combined_lifespan(app):
        # Run FastMCP's original lifespan (manages session manager)
        async with original_lifespan(app):
            # Init OpenRemote service
            await init_openremote_service(
                host=str(config.openremote_url),
                client_id=config.openremote_client_id,
                client_secret=config.openremote_client_secret,
                verify_SSL=config.openremote_verify_ssl,
                service_schema=ExternalServiceSchema(
                    serviceId=config.openremote_service_id,
                    label="MCP-Server",
                    homepageUrl=config.app_homepage_url,
                    status="AVAILABLE",
                )
            )

            await init_services(mcp)

            yield

    return combined_lifespan

app.router.lifespan_context = extend_lifespan(app.router.lifespan_context)