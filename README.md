## Scaleway-scheduler

By Akimed

### What is this?

This is a small serverless function that allows you to start and stop specific instances at times, in order to reduce costs.

Once an instance is assigned the "on-schedule" tag, if it is running at the specified times, it will be turned off, then turned back on at the scheduled times (9:00 to 19:00 on weekdays).

The instance that was turned off by the script will be assigned a tag "scheduled-off", used to start the instance back on.

An instance that is off will not be turned on by this script if it wasn't turned off by the script.

### How to use

```
npm install serverless
echo "SCW_REGION=fr-par
SCW_SECRET_KEY=
SCW_DEFAULT_PROJECT_ID=
SCW_ACCESS_KEY_FUNCTION=
SCW_SECRET_KEY_FUNCTION=
SCW_DEFAULT_PROJECT_ID_FUNCTION=
SCW_DEFAULT_REGION_FUNCTION=fr-par
SCW_DEFAULT_ZONE_FUNCTION=fr-par-2 > .env"
serverless deploy
```

You obviously need to add the proper credentials to the .env file, including your own for uploading the function, as well as a key for the function itself to turn on and off the instances

### Support

This is provided as is, no support from Akimed for your usecase.