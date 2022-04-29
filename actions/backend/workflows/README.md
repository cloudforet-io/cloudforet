## Naming rule
```
[Trigger_Type] Content
```

## Versioning
- format
```
{major}.{minor}.{patch}.{current_date|rc[n]}
```
- scenario

```
1.2.3 -> 1.2.3.xxxx -> 1.2.4-rc[n] -> 1.2.4 
```


## Workflows
> By default, [Push] includes a manual trigger (dispatch).

- `[Push] Build dev`
    - EVENT
        - When code is pushed to master
            - (triggered by `[Push] Sync CI`)
        - When the workflow is triggered
    - CONTENT
        - Build code and push docker image to cloudforetdev
- `[Dispatch] Release`
    - EVENT
        - When the workflow is triggered by `[Dispatch] Create all release branch` in cloudforet-io/cloudforet
    - CONTENT
        - Create github release branch
        - Trigger `[Dispatch] Branch tagging`
- `[Dispatch] Branch tagging`
    - EVENT
        - When the workflow is triggered by `[Dispatch] Release`
        - When the workflow is triggered by `[Dispatch] Make final releases` in cloudforet-io/cloudforet
        - When the workflow is manually triggered
    - CONTENT
        - Create github tag
        - Build docker image and push to docker hub
- `[Push] Sync CI`
    - EVENT
        - When code is pushed to master
            - (trigger `[Push] Build dev`)
        - When the workflow is manually triggered    
    - CONTENT
        - [Push]
            - Get workflows from actions and Trigger `[Push] Build dev`
        - [Dispatch]
            - Just get workflows from cloudforet/actions
- `[Dispatch] Update version file`
    - EVENT
        - When the workflow is triggered by `[Dispatch] Branch tagging`
    - CONTENT
        -  Update version file

## Scenario
- Update workflows: 
    - Manually trigger `[Push] Sync CI`

### Dev build
- Build Dev (Push): 
    - Commit code to master branch(`[Push] Sync CI` -> `[Push] Build dev`)
- Build Dev (Dispatch): 
    - Manually trigger `[Push] Build dev`

### Relase build
- Release branch cutting
    - Manually trigger `[Dispatch] Create all release branch` in cloudforet-io/cloudforet
- Create new rc tag
    - Manually trigger `[Dispatch] Branch tagging` after cherry pick to release branch
- Release (code freeze)
    - Manually trigger `[Dispatch] Make final releases` in cloudforet-io/cloudforet

### Hotfix build
- Create hotfix tag
    - Manually trigger `[Dispatch] Branch tagging` after cherry pick to release branch

