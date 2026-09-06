# Windows + WSL local networking

Start FastAPI in WSL with `uvicorn app.main:app --host 0.0.0.0 --port 8000`. Windows should reach [health](http://localhost:8000/health) through WSL forwarding. Phones need a reachable LAN address; their localhost is not your computer.

1. Put the phone and Windows host on the same trusted private network.
2. Run `ipconfig` in PowerShell. Find the IPv4 address of the active Wi-Fi/Ethernet adapter, not Docker, VPN or WSL virtual adapters.
3. Set `EXPO_PUBLIC_API_URL=http://<windows-lan-ip>:8000` in `mobile/.env`. Replace the placeholder; do not commit the actual address.
4. Ensure the network can reach the WSL service using one of the modes below.
5. Open `http://<windows-lan-ip>:8000/health` in the phone browser before debugging Expo.
6. Run `npm.cmd start` from Windows and scan the LAN QR code. Restart Metro after changing environment configuration. Allow the Expo development server's port (normally 8081) only on the trusted private network if Windows prompts.

## WSL2 NAT mode

Windows-localhost forwarding does not automatically expose WSL to phones. Obtain the WSL address using `wsl -d Ubuntu hostname -I`; identify its IPv4 address. If LAN forwarding is required, these are optional **Administrator PowerShell** commands with placeholders to replace:

```powershell
netsh interface portproxy add v4tov4 listenaddress=<windows-lan-ip> listenport=8000 connectaddress=<wsl-ip> connectport=8000
New-NetFirewallRule -DisplayName 'Coach Luna local API' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000 -Profile Private -RemoteAddress LocalSubnet
```

The WSL address may change after restart, requiring the proxy to be updated. Remove this development exposure when no longer needed:

```powershell
netsh interface portproxy delete v4tov4 listenaddress=<windows-lan-ip> listenport=8000
Remove-NetFirewallRule -DisplayName 'Coach Luna local API'
```

## Mirrored networking

Windows 11 22H2+ can use `[wsl2] networkingMode=mirrored` in the user's `.wslconfig`. This changes all WSL networking and requires a WSL restart; it is not changed automatically by this project. In mirrored mode, use the Windows LAN address and, if necessary, a port-specific Hyper-V firewall rule for WSL TCP 8000. Consult Microsoft's [WSL networking guide](https://learn.microsoft.com/en-us/windows/wsl/networking) for your installed WSL version. Do not disable the firewall or allow all inbound WSL traffic.

## Troubleshooting

- Verify `/health` in WSL, then Windows, then the phone to isolate the blocked hop.
- This host already has a Windows HTTP service on port 8000 (it responds with Microsoft-HTTPAPI 400). The verified local slice therefore uses `uvicorn app.main:app --host 0.0.0.0 --port 8001` and the ignored `mobile/.env` points to `http://localhost:8001`. Use 8001 in LAN/proxy examples on this machine; the project defaults remain 8000. No existing Windows service was changed.
- VPNs, guest Wi-Fi client isolation and public-network firewall profiles can prevent LAN access.
- Android emulators commonly reach the Windows host at `10.0.2.2`; physical phones use the LAN address.
- For web previews opened via a LAN hostname, add that exact origin to `COACH_LUNA_CORS_ORIGINS` (JSON array) before starting FastAPI. Native apps do not need browser CORS.
- An Expo tunnel only tunnels Metro; it does not expose the FastAPI server.
- Use a compatible Expo Go client. Native development builds can have platform-specific HTTP restrictions; validate local HTTP on target devices before changing transport settings.

No router forwarding, public tunnel, cloud exposure, firewall edits or WSL configuration changes are performed by the bootstrap. Phase 0 has no authentication and belongs on a trusted development network.
