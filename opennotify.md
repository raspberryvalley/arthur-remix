# Open-Notify

The [open-notify](http://open-notify.org) service is the thing which keeps all our ISS software ticking. The documenation of the service is good and extensive, so here we just highlight basic usage and our applications.

## Using the service

The original Arthur Project uses IFTTT for gathering the ISS timeout. We found the approach great, but want more out of the notifications. Enter [open-notify](http://open-notify.org).

> "Open Notify is an open source project to provide a simple programming interface for some of NASA’s awesome data. I do some of the work to take raw data and turn them into APIs related to space and spacecraft."

The API is perfectly suited for our project. You can find the source code for the API and other applications (such as 'number of people currently in space') [here](https://github.com/open-notify).

For our **iss_overhead** class, we use the [ISS CUrrent Location](http://open-notify.org/Open-Notify-API/ISS-Pass-Times/) interface. By default it provides 5 predictions for the times ISS passes overhead, we use only one (next occurance).

The call looks something like this:

```json
http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON&n=1
```

For Karlskrona, Sweden, you would then call

```json
http://api.open-notify.org/iss-pass.json?lat=56.16156&lon=15.58661&n=1
```

and the expected response (Karlskrona query) looks somewhat like this:

```json
{
  "message": "success",
  "request": {
    "altitude": 100,
    "datetime": 1539429501,
    "latitude": 56.16156,
    "longitude": 15.58661,
    "passes": 1
  }, 
  "response": [
    {
      "duration": 600,
      "risetime": 1539430252
    }
  ]
}
```

We keep the altitude default (100).

Check the [open-notify](http://open-notify.org) site to find more features. Great work!

And while you're testing, try out other locations of our friends out there:

| Country        | City       | Latitude  | Longitude  |
| -------------- | ---------- | --------  | ---------- |
| Sweden         | Karlskrona | 56.16156  | 15.58661   |
| Sweden         | Ronneby    | 56.20999  | 15.27602   |
| Czech Republic | Liberec    | 50.76711  | 15.05619   |
| Canada         | North Bay  | 46.322536 | -79.456360 |
