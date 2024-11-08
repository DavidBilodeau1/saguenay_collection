# Saguenay Waste Collection Schedule

## Integration for HACS


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
