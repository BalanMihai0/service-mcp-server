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

from fastmcp import FastMCP

from .asset import init_asset_service
from .asset_model import asset_model_mcp
from .realm import realm_mcp
#from .rule import rule_mcp


async def init_services(mcp_app: FastMCP):
    await init_asset_service(mcp_app)
    await mcp_app.import_server(asset_model_mcp, prefix="asset_model")
    await mcp_app.import_server(realm_mcp, prefix="realm")
    #await mcp_app.import_server(rule_mcp, prefix="rule")
