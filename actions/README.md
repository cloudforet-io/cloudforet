# actions
SpaceONE github action workflow repository

## description
`Actions` is a github action repository used by SpaceONE repositories.<br>
The SpaceONE repository linked to `Action` imports the latest workflow before executing CI.<br>

`Actions` is for the purpose of centralized management of github actions workflows<br>
so that provides an environment in which developers can proceed with development without caring about CI changes.

<img src = "https://user-images.githubusercontent.com/19552819/148719878-f6b48702-65d2-49a0-88a7-ee3773d0305f.png" width="80%" height="80%">

## How to use

### 1. prerequisite
- Set [topic](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) in each github repository
- Create [PAT_TOKEN](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) secret in each github repository.


### 2. Deploy push_sync_ci.yaml
The SpaceONe repository linked to `Action` import the github action workflow through `push_sync_ci.yaml`.<br>
For manage workflow through `Actions`, you just deploy `push_sync_ci.yaml` in the github repository.

There are two ways to deploy as follows.

- Use [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- Execute github action of `actions`
  - [[CI] init group](https://github.com/spaceone-dev/actions/actions/workflows/init_group.yaml)
    - need group name input and deploy `push_sync_ci.yaml` to all repositories that have topic matching the group.
  - [[CI] init repository](https://github.com/spaceone-dev/actions/actions/workflows/init_repository.yaml)
    - need repository name input and deploy `push_sync_ci.yaml` to repository that matched input.

*) `group` is directory name in `Actions` and there are github action workflow

---

**WARN: When `push_sync_ci.yaml` is deployed all existing workflow is deleted**

---

## Create new workflow
If you want add new workflows, Upload workflows to directory of `actions`<br>
Thereafter, `push_sync_ci.yaml` of each repository synchronizes the newly added workflow to the repository.<br>

```
.
├── README.md
├── backend
│   └── workflows           ★ 
├── common
│   └── workflows
│       ├── [Dispatch]sync_ci.yaml
│       └── [Push]sync_ci.yaml
├── plugin
│   └── workflows           ★ 
│       ├── README.md
│       ├── [Dispatch]release.yaml
│       └── [Push|dispatch]Build_dev.yaml
├── requirements.txt
└── src
    ├── main.py
    └── module
```
