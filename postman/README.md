# postman-collection

The files in this project can be imported into [postman](https://www.postman.com/) for testing the ultradata API calls. Postman 8.6.2 was used in building these files

The setup requires importing two files

* ultradata-api.postman_environment.json
* ultradata-api.postman_collection.json

---

Setup

1. create a new `Workspace` or use an active existing workspace.
2. import the environment.  Select the `Environments` tab of the active workspace. Select import and import the `ultradata-api.postman_environment.json` file.
3. import the collection. Select the `Collections` tab of the active workspace. select `Import` from the workspace window and load file `ultradata-api.postman_collection.json`.
4. set the working environment to `ultradata-api`. Here you can set the username and credential information for connecting - the variables that you may need to adjust would be.
    1. `ultradata-user`
    2. `ultradata-pw`
5. Optional - set a `starttime` and `endtime` in the environment.  The API uses times in seconds since the epoch, setting these once in the environment will force the API calls to use the same time window for each run.  To get the number of seconds:

linux

```
date +%s -d '2021-01-01'
```

mac

```
date -j -u 010100002021 +%s
```

----

Using

* Execute the `get auth token` request first.  This will set OAuth2 token information into the environment that are needed for authenticating API calls
* Explore other API calls using different query parameters as desired.
