In this challenge we are given a link to a website and his source code.

Giving a fast look at the source code is easy to notice that the accounts are saved in a Map with an id like "ghast:0", where 0 is an increasing number, converted in base64 without the equal sign.

```javascript
const makeId = () => Buffer.from(`ghast:${idIdx++}`).toString('base64').replace(/=/g, '')

const things = new Map()

things.set(makeId(), {
  name: secrets.adminName,
  // to prevent abuse, the admin account is locked
  locked: true,
})
```

Furthermore there is a route at /api/flag that you can access only if your account "name" attribute is the same as the admin one (which is secret) and you don't have the "locked" attribute (which is automatically set to true in the pre-existent admin account).

```javascript
if (req.url === '/api/flag' && req.method === 'GET') {
    if (user.locked) {
      res.writeHead(403)
      res.end('this account is locked')
      return
    }
    if (user.name === secrets.adminName) {
      res.writeHead(200)
      res.end(secrets.flag)
    } else {
      res.writeHead(403)
      res.end('only the admin can wield the flag')
    }
}
```

Here it comes the fun fact: in this site you can also save some objects (called ghasts) with a title and a text content but looking at the source code you can notice that it saves them in the same Map as the users. This means that going to /api/things/[id] you can view a ghast or a user with a given id. Because the admin account was created first his id will be "ghast:0" in base64, without the equal sign: Z2hhc3Q6MA. Infact visiting /api/things/Z2hhc3Q6MA we now know the admin's username: "sherlockholmes99".

Now we have to create a new account with that same username so we don't have the lock attribute. This is impossible to do in the registration page due to a condition: you cannot create an account with the same name of the admin. So we have to use again the fun fact found earlier: we create a ghast with the name "sherlockholmes99" and any content, grab the id from the url and paste it into the cookie named user.

Here we are, now it is possible to visit the page /api/flag and grab your flag without any problem.

```
flag{th3_AdM1n_ne3dS_A_n3W_nAme}
```