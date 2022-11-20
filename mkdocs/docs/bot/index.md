# Bot
Moni **Bot** allows you to send HTTP GET requests to it's endpoints for on-demand checks. Response body will contain:

~~~~ JSON
{
    "host": str,
    "check": str,
    "status": bool,
    "message": str
}
~~~~

