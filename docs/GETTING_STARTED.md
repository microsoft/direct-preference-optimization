# Getting Started

This document serves to describe how to setup your environment to run the code base - and optionally integrate it into your own code.

## Required Infrastructure

This project depends on Azure resources. If you don't have an Azure account, you may create one for free [here](https://azure.microsoft.com/en-us/free/).

To use this codebase, you must have deployed an [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service/) instance, an [Azure Storage](https://azure.microsoft.com/en-us/products/storage/blobs/) account, and an [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search/) instance.

## Environment Configurations

It is advised to use the preconfigured dev container to run this project. A docker container as a remote container in VSCode or a GitHub codespace should be sufficient.

[Learn more about dev containers here](https://learn.microsoft.com/en-us/training/modules/use-docker-container-dev-env-vs-code/).
There are environment variables necessary for this code base to connect to the required infrastructure.
These are:

* "AZURE_SEARCH_ENDPOINT": The Azure AI Search endpoint
* "AZURE_AI_SEARCH_API_KEY": The Azure AI Search API key
* "AZURE_OPENAI_ENDPOINT": The Azure OpenAI endpoint
* "AZURE_OPENAI_API_KEY": The Azure OpenAI API key
* "STORAGE_ACCOUNT_NAME": The storage account name
* "STORAGE_ACCOUNT_URL": The storage account url

For all other environment configurations, please refer to [/.devcontainer/devcontainer.json](/.devcontainer/devcontainer.json) for recommended extensions and setup commands - if running locally.

## Running the project

It is advised to use the launch settings provided in this repo to run the project.
Running Backend/Frontend will attach the debug process to both the python backend and the javascript/typescript frontend.

## Importing the project

Some aspects of the code base are reusable for your own projects.
These components are located in ```backend/libs/core```
Two ways to integrate those components are outlined below.

### Multi-repo workspaces with submodules

Using the following commands, you can import this code as a submodule in your project:
```git submodule add https://github.com/microsoft/direct-preference-optimization```
```git submodule init```
```git submodule update```

To get latest from a submodule, you can read more about submodules [here](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

### python package

You can optionally distribute the backend/libs/core modules as a python package with the package backend tooling of your choice. Then, you may distribute that package to an internal pip server for distribution.

Read more [here](https://packaging.python.org/en/latest/guides/hosting-your-own-index/) about packaging python modules locally. Or [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for using pypi.

## Customizing the project

### Customizing Option Settings

We use [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for settings management. This allows for auto-loading config values if they match the access patterns we've specified in out module ```backend.libs.core.models.options```.

If you would like to override the access patterns with paths that differentiate from ours, you can supply your own mappings by monkeypatching ```from_settings``` on the relevant options class. For an example of how we do this, go to ```/backend/settings_factory.py```.

### Customizing Prompts

If you would like to customize some of the settings for the llm, you may edit the fields in ```/backend/chat_config.yaml```
