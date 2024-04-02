# Canadian Citizenship Application Tracker for Home Assistant 🇨🇦

This Home Assistant integration allows you to track the last update time of your Canadian citizenship application
directly from your Home Assistant instance. It automatically checks for updates every 6 hours.

> [!CAUTION]
> Please be aware that Home Assistant exposes the configuration values of all integrations to every other installed
> integration. This means that if there is a malicious integration installed that sends back all configuration values from
> your Home Assistant, your credentials could potentially be leaked. Use this integration at your own risk.

## Installation

To manually install this integration from GitHub, follow these instructions:

- Add `cit_canada` folder with the contents of this repository into the `custom_components` directory of your Home
  Assistant installation. If the `custom_components` directory does not exist, create it at the same level as
  your `configuration.yaml` file.
- Restart Home Assistant to apply the changes.
- After restarting, configure the integration through the Home Assistant UI.

## Configuration

To configure this custom integration, follow these steps:

1. Navigate to your Home Assistant's `Settings` -> `Devices and Services`.
2. Click on the `Add Integration` button.
3. Search for the `Canadian Citizenship Application Tracker` and select it.
4. Enter your credentials as required from the citizenship tracker website to authenticate.

With this integration, you can monitor multiple citizenship applications simultaneously. To include additional UCIs,
navigate to the "Canadian Citizenship Application Tracker" device within the Home Assistant UI, and select "Add entry".

## Usage

Upon successful authentication, a new entity will be added to your Home Assistant
named `sensor.uci_1234_last_update_time`, where `1234` represents the last 4 digits of your UCI. This entity will track
the last update time of your application.

This integration automatically updates the sensor's timestamp whenever there is a change on your application,
including "ghost updates".

### Automations

You can set up automations in Home Assistant to act upon updates. For example, to receive a notification on your phone
when your citizenship application receives any updates, you can configure an automation like this:

```yaml
alias: Notify on Citizenship Application Update
description: Sends a notification to my phone when the citizenship application status updates.
trigger:
  - platform: state
    entity_id: sensor.uci_1234_last_update_time
action:
  - service: notify.mobile_app_<your_device>
    data:
      message: "Your Canadian Citizenship application has been updated."
```

Replace `sensor.uci_1234_last_update_time` with the actual entity ID corresponding to your application
and `<your_device>` with your mobile device identifier in Home Assistant.
