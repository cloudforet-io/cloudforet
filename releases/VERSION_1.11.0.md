## New Feature
### Custom Dashboard
- The Custom Dashboard service has been released that configure your own dashboard using various data in Cloudforet.
- Dashboard service is a beta service and can be used through the console's `DASHBOARD_ENABLED` setting.
- Widgets that can be placed on a dashboard include:
  - Cost Explorer (DONE)
  - Asset Explorer (2023 2Q)
  - Alert Manager (2023 2Q)
### Console API v2
- REST-based Console API v2 service has been released.
- The programming language has changed from Node.js + Express method to Python + FastAPI.
- Both v1 and v2 APIs will be serviced, and will be migrated to v2 API sequentially.
- The specification for Console API v2 can be found at the URL `<console_api_v2_endpoint>/docs`.
- List of APIs that have been developed
  - Identity (IAM)
  - Inventory (Asset Inventory)
  - Repository
  - Notification
  - Cost Analysis (Cost Explorer)
  - Dashboard

## Improvement
### Cost Explorer
- The DataSourceRule API has been enhanced to allow adding custom rules.
### Asset Inventory
- Added CollectorRule API to change data when collecting cloud assets.
- The Cloud Service's data model has changed, adding the following features:
  - Tag-based search
  - Tag-based sort
  - Statistics API using tags
- Timezone cannot be changed when setting Collector Schedule.
- A Log Tab has been added in Cloud Service Details, allowing you to view all related logs.  
### Alert Manager
- The type of the `alert_number` field in the Alert resource has been changed.
  - `Integer` -> `String`
- Account information has been added in the message when sending alerts.
### etc.
#### Board Service
- The `Notice` Board is automatically added when searching the board list for the first time.
- You can set 'pinning' and 'pop-up' when creating domain notices.
#### Supervisor Service
- Added the following Kubernetes configuration features:
```yaml
KubernetesConnector:
  ...
  service_account: <kubernetes_service_account_name>
  imagePullSecrets:
  - name: <private_registry_secrets>
  env:
  - name: HTTP_PROXY
    value: <proxy_url>
  - name: HTTPS_PROXY
    value: <proxy_url>
  resources:
    requests:
      memory: 64Mi
      cpu: 250m
    limits:
      memory: 128Mi
      cpu: 500m
```
- You can specify the number of pods for each plug-in type.
```yaml
KubernetesConnector:
    ...
    replica:
        inventory.Collector: 1
        inventory.Collector?aws-ec2: 2
        inventory.Collector?aws-cloud-services: 2
```
#### Secret Service
- Supports MongoDB as Secret Storage.
#### Repository Service
- Supports Harbor as Image Registry.

## Bug Fixes
### Cost Explorer
- Fixed PDF download bug in Dashboard.
### Asset Inventory
- Fixed an issue where Cleanup Scheduler does not work in AWS DocumentDB.
- Fixed an issue where Collector could not be created when `plugin_id` was longer than 40 characters.
### Alert Manager
- Fixed receiving Low Urgency alarms even when set to only receive High Urgency alarms.
- When setting Escalation Policy, you cannot set negative numbers for `escalate_minutes` or `repeat_count`.
- Fixed a resource information display bug in alert details.
### Supervisor
- Fixed plugin connection errors by applying `Readiness Probe` when deploying plugins to kubernetes.

