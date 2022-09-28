# Home Assistant integration to create a QR-Code
[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]

This integration allows to create QR Codes with static or dynamic content.

## Features
* Static content
* Dynamic content with the help of Templates
* Custom QR-Code color
* Custom QR-Code background color
* Error correction adjustment

{% if not installed %}
## Installation

### Step 1:

<br>

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DeerMaximum&repository=QR-Code-Generator&category=integration)

### Step 2 (**Don't forget**):

1. Click install.
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "QR-Code".

{% endif %}

### Options

| Options    | Description                            | Default
| ------------ | -------------------------------------- | -------- |
| `Name` | *(str)* Name of the QR Code. | - |
| `Content` | *(str)* Content of the QR Code. Can be a template. | - |
| `Color` | *(str)* Color of the QR Code in hex. Supports transparency (#RRGGBBAA). | #000 |
| `Background color` | *(str)* Color of the background in hex. Supports transparency (#RRGGBBAA). | #FFF |
| `Scale` | *(int)* Scale of the QR Code. | 10 |
| `Border` | *(int)* Thickness of the QR Code border in "QR Code boxes". | 2 |
| `Error correction` | *(str)* Strength of error correction. Possible values: <br> L - About 7% or less errors can be corrected. <br> M - About 15% or less errors can be corrected. <br> Q - About 25% or less errors can be corrected. <br> H - About 30% or less errors can be corrected. | H |

### ATTRIBUTES

| Attribute    | Description                            |
| ------------ | -------------------------------------- |
| `text` | *(str)* Rendered content of the QR Code. |
| `color` | *(str)* Color of the QR Code in hex. |
| `background_color` | *(str)* Color of the background in hex.|
| `scale` | *(int)* Scale of the QR Code. |
| `border` | *(int)* Thickness of the QR Code border in "QR Code boxes". |
| `error_correction` | *(str)* Strength of error correction. Possible values: <br> L<br> M <br> Q  <br> H |

[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/v/release/DeerMaximum/QR-Code-Generator.svg?style=for-the-badge
[releases]: https://github.com/DeerMaximum/QR-Code-Generator/releases
