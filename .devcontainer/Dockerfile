# Dev container for building and serving the Jekyll site
FROM mcr.microsoft.com/vscode/devcontainers/ruby:3.3

# Ensure we have a modern bundler
RUN gem install bundler --no-document

RUN mkdir -p /workspace && chown -R vscode:vscode /workspace


WORKDIR /workspace
