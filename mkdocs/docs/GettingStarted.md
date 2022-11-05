# Getting Started

Ideal way to run Moni would be to set it up somewhere outside of your servers, so it doesn't go down with your production servers and can actually alert if they are down.
To run Moni in a container you need to:

1. Create `settings.yml` and define necessary settings (see **Settings** section).
2. Pull and run a Docker image from `podkosa/moni` 
    ~~~~ Bash
    docker run -v /yourdirectory/settings.yml:/moni/settings.yml podkosa/moni
    ~~~~

If you're familiar with *Docker Compose* see `example.docker-compose.yml` in the GitHub repo.
