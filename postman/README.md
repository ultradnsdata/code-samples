# postman-collection

The files in this project can be imported into [postman](https://www.postman.com/) for testing the ultradata API calls.

The setup requires importing two files

* ultradata-api.postman_environment.json
* ultradata-api.postman_collection.json

---

Setup

1. import the environment.  go to `Manage Environments`, select import and import the `ultradata-api.postman_environment.json` file.
2. import the collection. select `Import` from the main window and load file `ultradata-api.postman_collection.json`.
3. set the working environment to `ultradata-api`. Here you can set the username and credential information for connecting - the only two variables that you may need to adjust would be.
    1. `ultradata-user`
    2. `ultradata-pw` 

----

Using

* Execute the `get auth token` request first.  This will set OAuth2 token information into the environment that are needed for authenticating API calls
* Explore other API calls using different query parameters as desired.
