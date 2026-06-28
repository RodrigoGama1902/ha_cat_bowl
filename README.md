# Cat Bowl — Home Assistant Integration

A custom Home Assistant integration that polls a local cat food detector server and exposes the results as entities.

## How it works

On every update cycle the integration pulls a snapshot from the configured Home Assistant `camera` entity, posts it to the server's `/detect` endpoint, and reports the fresh result. The sensor is fully self-contained and needs **no external automation**.

> **Note:** Values refresh once per update cycle (configurable scan interval, default every hour). The snapshot is sent to `/detect` as multipart form-data under the field name `image`.

## Entities

| Entity | Type | Description |
|---|---|---|
| `Cat Food` | Binary Sensor | `on` when food is present in the bowl |
| `Cat Food Coverage` | Sensor (%) | Percentage of the bowl area covered by food |
| `Cat Food Detector Latency` | Sensor (ms) | Response latency from the detector server |
| `Cat Bowl Camera` | Sensor (diagnostic) | The camera entity whose snapshots are sent to the detector |
| `Cat Bowl Scan Interval` | Sensor (diagnostic, s) | The configured polling interval |

## Requirements

- Home Assistant 2024.1 or newer
- A running instance of the [cat food detector server](https://github.com/RodrigoGama1902/cat_bowl_server) reachable on your local network

## Installation

### Option A — HACS (recommended)

1. Open **HACS** in your Home Assistant sidebar.
2. Go to **Integrations** → click the three-dot menu → **Custom repositories**.
3. Add `https://github.com/RodrigoGama1902/ha_cat_bowl` as an **Integration** repository.
4. Search for **Cat Bowl** and click **Download**.
5. Restart Home Assistant.

### Option B — Manual

1. Download or clone this repository.
2. Copy the `custom_components/cat_bowl` folder into your Home Assistant config directory:
   ```
   <config>/custom_components/cat_bowl/
   ```
3. Restart Home Assistant.

## Configuration

After installation, add the integration via the UI:

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Cat Bowl**.
3. Enter the **host** and **port** of your detector server (defaults: `192.168.68.50` / `8080`).
4. Pick the **Camera** entity whose snapshots will be sent to the detector.
5. Optionally adjust the **Scan interval** in seconds (default: `3600` — once per hour; minimum `10`).
6. Click **Submit**. The integration will validate the connection before saving.

## Troubleshooting

- **Cannot connect**: Make sure the detector server is running and reachable at the configured address. You can test it by opening `http://<host>:<port>/health` in a browser — it should return a successful response.
- **Unavailable entities**: The coordinator polls the server once per scan interval (default every hour). If the server goes offline, entities will become unavailable until the next successful poll.
- **Entities never leave "unavailable" / stuck values**: Make sure the configured camera entity is available and producing snapshots, and that the server's `/detect` endpoint accepts the image and returns a successful response.
