Writes alerts to a file in `/moni/logs` directory.
    
!!! warning "Log size"
    Rotation is not implemented yet, so be sure to clean up (e.g. with a `cron` periodic task)

!!! info "Containerization"
    If you're deploying inside a container (e.g. Docker), be sure to mount `./logs/:/moni/logs` through `volumes`

~~~~ YAML title="settings.yml"
handlers:
  log:
    filename: moni.log
~~~~
