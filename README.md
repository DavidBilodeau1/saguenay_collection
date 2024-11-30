# Saguenay Waste Collection Schedule

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://hacs.xyz/docs/faq/custom_repositories)


_Home Assistant Integration for [Saguenay's Waste Collection](https://ville.saguenay.ca/services-aux-citoyens/environnement/recyclage/horaire-de-la-collecte)._

**Work in Progress**

Supported Features:
 * Track the collection dates for garbage, recycling and compost


## Installation


### Recommended: [HACS](https://www.hacs.xyz)

1. Add this repository as a custom repository to HACS: [![Add Repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=davidbilodeau1&repository=saguenay_collection&category=integration)
2. Use HACS to install the integration.
3. Restart Home Assistant.
4. Set up the integration using the UI: [![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=saguenay_collection)

### Alternative: Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `saguenay_collection`.
1. Download _all_ the files from the `custom_components/saguenay_collection/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Saguenay Collection Schedule"

## Configuration is done in the UI

<!---->

### Template to display in Home Assistant

To display the next waste collection date as something more user-friendly, I made a YAML template:

```yaml
  {% set t = now() %} # compare with now
  {% set midnight = today_at() %}
    # convert sensor value as y-m-d to datetime
  {% set event_date = as_local(states('sensor.saguenay_recyclage_schedule') | as_datetime('%Y-%m-%d')) %}
  {% if event_date %}
    {% set delta = (event_date - midnight).days %} # get difference in days
    {% if delta == 0 %}
      Aujourd'hui
    {% elif delta == 1 %}
      Demain
    {% elif delta == 2 %}
      Après demain
    {% else %}
      Dans {{ delta }} jours
    {% endif %}
  {% else %}
    Date invalide
  {% endif %}
```
[View gist](https://gist.github.com/DavidBilodeau1/4d42ea1d253e6ccf85365cd1395bd4a6)


## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/davidbilodeau1/saguenay_collection.svg?style=for-the-badge
[commits]: https://github.com/DavidBilodeau1/saguenay_collection/commits/main/
[license-shield]: https://img.shields.io/github/license/davidbilodeau1/saguenay_collection.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/davidbilodeau1/saguenay_collection.svg?style=for-the-badge
[releases]: https://github.com/DavidBilodeau1/saguenay_collection/releases
