"""Which replica serves which pack."""

from __future__ import annotations

from chunkforge.refs import PackRef


class Roster:
    def __init__(self, hosts: list[str]) -> None:
        self.hosts = list(hosts)

    def host_for(self, ref: PackRef) -> str:
        """Replica that serves this pack; placement follows the pack, not its contents."""
        total = 0
        for char in ref.pack_id.encode("utf-8"):
            total = (total * 31 + char) % (2**31)
        return self.hosts[total % len(self.hosts)]
