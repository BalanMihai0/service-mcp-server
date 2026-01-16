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

from services.openremote_service import get_openremote_service

realm_mcp = FastMCP("Realm Service")


@realm_mcp.tool
async def get_all():
    """Retrieve all realms."""
    openremote_service = get_openremote_service()

    return await openremote_service.client.realm.get_all_realms()


@realm_mcp.tool
async def get_by_name(realm_name: str):
    """Retrieve details about the currently authenticated and active realm."""
    openremote_service = get_openremote_service()

    return await openremote_service.client.realm.get_realm(realm_name)