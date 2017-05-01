# REST API Specification (v.0)

----

## Users

### Account Creation

New user accounts are created by submitting a simple `POST` request to the users
endpoint.

**Example request:**

```json
POST api.stackcite.com/v0/users/

{
  "Content-Type": "application/json"
}

{
  "email": "some_user@example.com",
  "password": "Ex4mpl#Pa55word"
}
```

Creating a new user automatically triggers the creation of an account
confirmation token. This token should be sent to the new user's email address
as a link.

### Account Confirmation

User accounts default to a limited state. Full access will be granted to users
who "confirm" their account by submitting the correct confirmation token to the
server. Account confirmation tokens are only valid for 15 minutes, however new
tokens can be issued at the user's request.

#### How to confirm an existing token:

An existing confirmation token can be confirmed by submitting a `PUT` request to
the account confirmation endpoint. The body of this request must (only) contain
the requisite confirmation key.

**Example request:**

```json
PUT api.stackcite.com/v0/users/conf/

{
  "Content-Type": "application/json"
}

{
  "key": "a627f9ad6345c82fef5831f801e849fa0e47cfef71cbb3f10b0ce0f7"
}
```

A successful response will return `200 OK` and provide the unique id of the
(now) confirmed user.

**Example response:**
```json
{
  "user": {
    "id": "5906f49b30f193695b7dbf60"
  }
}
```

#### How to issue a new confirmation token:

If a new confirmation token is required (e.g. the old one has expired), one can
be issued by submitting a `POST` request to the server. This request must
include the user's email for which this confirmation token should be issued.
If an existing token has already been issued, it will be invalidated.

**Example request:**

```json
POST api.stackcite.com/v0/users/conf/

{
  "Content-Type": "application/json"
}

{
  "email": "some_user@example.com"
}
```

The server will respond with `204 Created` if the email address corresponds to
a known user and a new token was successfully created.

### Authentication

The Stackcite API uses a token-based authentication system. To "sign in," you
must issue a new authentication token, which will include an authenticated key.
This key should be included in the headers of any request that deals with
a protected resource (e.g. user account modification).

An important note is that the authenticated key is never used in a request body
or URL. It is only (and always) included with the "Authorization" header. If
any resource is unavailable due to failed authentication, the server will
respond with `403 Forbidden` (and very little else).

***Note:*** In general, any `POST`, `PUT`, or `DELETE` requests will need to be
authenticated.

#### How to issue a new token (sign in):

**Example request:**

```
POST api.stackcite.com/v0/users/auth/

{
  "Content-Type": "application/json"
}

{
  "email": "some_user@example.com",
  "password": "Ex4mpl#Pa55word"
}
```

#### How to authenticate a request:

Each request to a protected resource is authenticated by including an
authenticated key in the "Authorization" header.

**Authenticated request header:**

```json
{
  "Content-Type": "application/json",
  "Authorization": "key 4db1ae621ab33b3ac31ce58e29fa9488ac60e815540c4bb8375985fb"
}
```

#### How to keep a token active:

Authentication tokens will automatically invalidate after an hour of disuse.
This counter is reset any time they are used on a protected resource, or any
time an authenticated `PUT` request is sent to the authentication key endpoint.
The response will include updated token data.

If you need to check on the status of a token without triggering a refresh
(e.g. you have some loop to see if the user is still authenticated), you can
submit a `GET` request to the same endpoint. The response will include existing
token data.

#### How to log out:

Since tokens will eventually expire, it is not necessary to destroy one if you
want your application to log out. It is, however, encouraged. To log out in
this way, submit an authenticated `DELETE` request to the server.

----

## Data

**Resource map:**

```
api.stackcite.com/v0/
 +- users/                  [POST]
 |   +- auth/               [POST, GET, PUT, DELETE]
 |   +- conf/               [POST, PUT]
 +- people/{id}             [POST, GET, PUT, DELETE]
 +- organizations/{id}          (...)
 |   +- publishers/{id}
 +- sources/{id}
 |   +- text/{id}
 |   |   +- book/{id}
 |   |   +- article/{id}
 |   +- media/{id}
 |       +- audio/{id}
 |       +- video/{id}
 +- citations/{id}
```