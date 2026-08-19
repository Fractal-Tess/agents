---
name: ft-netbird-share
description: Use whenever netbird, NetBird, VPN mesh, or sharing a locally hosted service with the user's other devices is mentioned. Explains the NetBird mesh: host on all interfaces, address is <hostname>.netbird.cloud, ports are preserved.
---

# NetBird share

This machine is part of a NetBird mesh VPN. Anything hosted here is reachable from the user's other devices over the mesh, no extra tunnel, no port forwarding.

## Address

The hostname is the subdomain: `<hostname>.netbird.cloud`.

- `vd` → `vd.netbird.cloud`
- `kiwi` → `kiwi.netbird.cloud` (this machine)

Ports are preserved. A service on port 3000 is reachable at:

```
kiwi.netbird.cloud:3000
```

No mapping, no rewrite. Whatever port the process listens on is the port the user dials.

## Hosting rules

1. **Bind all interfaces.** Always `0.0.0.0`, never `127.0.0.1` or `localhost`. The mesh reaches the host by IP; a localhost bind is unreachable from other devices.
2. **Watch dev-server defaults.** Vite, Next.js dev, `bun run dev`, and most dev servers bind localhost by default. Force the host flag: `--host`, `--host 0.0.0.0`, or `host: "0.0.0.0"` in config.
3. **Firewall.** If the OS firewall blocks the port, allow it on the chosen interface before claiming the service is up.
4. **Verify.** After starting, confirm reachability from the mesh: `curl http://<hostname>.netbird.cloud:<port>` from the host, or tell the user to try from the other device.
5. **State the URL.** When the user asks to access something being hosted, give the concrete address `kiwi.netbird.cloud:<port>` and the exact command used to start the service, so they can hit it immediately.
