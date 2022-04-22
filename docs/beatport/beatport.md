
## Search API

> https://www.beatport.com/api/v4/catalog/search?q=QUERY
> https://www.beatport.com/search/tracks?page=2&q=demuja&_pjax=%23pjax-inner-wrapper
## Me

### Login

#### HTTP request

> POST https://www.beatport.com/api/account/login
> Origin: https://www.beatport.com
> X-CSRFToken: TOKEN

:warning: CSRF token can be retrieved via cookies


#### Request data

```json
{
    "username": "string",
    "password": "string",
    "remember": "boolean"
}
```

#### Response

```json
{
    "dj_profile": {},
    "email_address": "felix@voituret.fr",
    "id": 7174166,
    "name": {
        "first": "Félix",
        "last": "Voituret"
    },
    "total_orders": 8,
    "username": "octomusic"
}
```

https://www.beatport.com/api/my-beatport