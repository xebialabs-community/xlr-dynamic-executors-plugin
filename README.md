# Preface #

This document describes the functionality provided by the xlr-dynamic-executors-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-dynamic-executors-plugin is a XL Release plugin that allows to run commands/scripts on remote servers using ssh.
The tasks will be executed only if an executor is available. The number of `executors` can be defined on the global server configuration.

# Installation #

You'll need the following items:

+ Place the latest release under the `plugins` folder.
+ Place the [latest version](https://github.com/xebialabs-community/overthere-pylib/releases) from the overtherepy lib under the `plugins` folder.
+ If needed append the following to the `script.policy` under `conf`:

```
permission java.io.FilePermission "plugins/*", "read";
permission java.io.FilePermission "conf/logback.xml", "read";
```

## Types ##

+ `executors.Server`: Create as many servers as you want (Only linux/ssh supported)
  `serverName` must be unique.
  `label` will be used to autoselect the server to run the script on. Only 1 label supported. 
  `nrExecutors` defines the number of scripts that can run in parallel.
+ `executors.RunScript`: Defines the task to be run.
  `executorLabel`: must match a `executors.Server` label. Only 1 label supported.
  `scriptToExecute`: The script to be executed (will not be uploaded, so should be present).
