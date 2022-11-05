Sends a POST request to your url with check results.

~~~~ JSON
{
    "host": str,
    "check": str,
    "status": bool,
    "message": str
}
~~~~

~~~~ YAML title="settings.yml"
handlers:
  webhook:
    url: http://your/webhook/url/
    user: user
    password: password
    headers:
      header1: header1
    cookies:
      cookie1: cookie1
~~~~
