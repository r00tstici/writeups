# OPA Secrets - H@cktivityCon 2021

- Category: Web
- Points: 298
- Solves: 136
- Solved by: RxThorn

## Description

OPA! Check out our new secret management service

## Solution

After registration, by accessing the security screen, you will see the link to the source code: http://github.com/congon4tor/opa_secrets.

It is a Flask application. The interesting part is in the function executed before the first request: it sends some data to `localhost:8181`. Reading `deploy.yaml` (the Kubernetes deployment file) you notice that on that port is exposed `open policy agent`, so probably the web app checks if the user can read/write secrets by communicating with it.

The user can have the role `admin`, which can read every secret, or `user`, which has to be authorized by the author. The vulnerability is in the line of code where the server adds a new user to open policy agent: `payload = f"""{{"user":"{username}","role":"{role}"}}"""`. `role` is controlled by the web server while `username` is the user input at the registration. By inserting `something","role":"admin` as username, the payload sent to open policy agent would be `{{"user":"something","role":"admin","role":"user"}}` that overwrites the user role.

Then it is possible to create a secret and press the button to read it. While doing it is important to change the request (for example with Burp) to read the secret with id `afce78a8-23d6-4f07-81f2-47c96ddb10cf` which is written in the code. It contains the flag.
