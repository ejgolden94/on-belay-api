# on-belay-api

This is the API of a Personal Climbing Tracker app, On Belay. This app is meant to allow climbers to track their progress as they get better at the sport. It also is a place to record "beta" for yourself so you can remember your climbs and what you did to achieve them.

[See Front End React APP Repo Here](https://github.com/ejgolden94/on-belay)
[Access The Deployed API Here](https://on-belay-api.herokuapp.com/)

Technologies Used for this API:
`Flask`
`Python`
`Peewee`

----
## End Points 
You can access this API through the deployed site above. 

there are 4 groups of enpoint you can hit via this API:
- Routes
- Climbs
- Users
- Comments

### Routes 
Get all Routes: `https://on-belay-api.herokuapp.com/api/v1/routes/` 
- Method: `GET`
- Query Params: This enpoint will accept a `setting` query param of either `indoor` or `outdoor` to show indoor (gym) routes vs outdoor 
- Will return an object containing all routes data in an array of JSON, a message, and a status 

Creat a Route: Get all Routes: `https://on-belay-api.herokuapp.com/api/v1/routes/` 
- Method: `POST`
- Accepts JSON
- Payload: this route requires a payload -- example:
```javascript 
{
    name: "Pile-o-mania",
    description:"I don't know what the name refers to, but this route is not a \"pile\" the way I use the word to describe a climb....",
    protection: "7 bolts to chains with fixed biners. The last bolt might be hard to get to for a short climber but you are still safe.",
    image:"https://d36ai2hkxl16us.cloudfront.net/thoughtindustries/image/upload/v1498500090/scrbwmci4pojai2zcdgo.jpg",
    location: "Right next to Cuckoo's Nest. Look up for the huge flake.", // 255 char max
    gym_outdoor:"outdoor", // this must be indoor or outdoor 
    height: 50,
    rating:"5.10c",
    wall_type:"overhang",
    creator: 1 // this is a user id 
}
```
- Will return an object containing the new route as JSON, a message, and a status 

Get Current Users Routes `https://on-belay-api.herokuapp.com/api/v1/routes/my_routes`
- Method: `GET`
- The client must be logged in for this route to send back any data
- Will return an object containing all of the routes that user has created data in an array of JSON, a message, and a status 

Get All Routes Climbs `https://on-belay-api.herokuapp.com/api/v1/routes/<route_id>/route_climbs`
- Methd:`GET`
- Query Params: This enpoint will accept a `user` query param of either `true` or `false` to return only those climbs on a route logged by a specific user
- Will return an object containing all of the climbs logged on a given route in an array of JSON, a message, and a status 

Show Route `https://on-belay-api.herokuapp.com/api/v1/routes/<route_id>`
- Methd:`GET`
- Will return an object containing the data of a given route as JSON, a message, and a status 
- If no route is found this will send back a `404` and an error message

Edit Route `https://on-belay-api.herokuapp.com/api/v1/routes/<route_id>`
- Methd:`PUT`
- Accepts JSON
- Payload: this route requires a payload including any or multiple fields from the `POST` route example
- Will return an object containing the data of the deleted route as JSON, a message, and a status 

Delete Route `https://on-belay-api.herokuapp.com/api/v1/routes/<route_id>`
- Methd:`DELETE`
- Will return an object containing the data of the deleted route as JSON, a message, and a status 