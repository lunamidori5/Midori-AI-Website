FROM ghcr.io/gohugoio/hugo:latest

# Compose mounts the site here and inherits Hugo's official entrypoint.
WORKDIR /project

# Expose port for the live development server.
EXPOSE 1313
