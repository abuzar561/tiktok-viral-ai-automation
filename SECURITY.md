# Security Policy

## Supported Version

The `main` branch contains the maintained public template.

## Reporting Security Issues

Please do not open a public issue containing private workflow exports, credentials, browser sessions, or scraped private data. Contact the maintainer directly:

- Email: contactbyabuzar@gmail.com

## Safe Configuration

This project should not contain:

- n8n credential IDs or credential exports
- browser profile data or cookies
- API keys or bearer tokens
- private scraped datasets
- private IP addresses from a local deployment

If a secret is accidentally committed, rotate it immediately and remove it from the repository history.
