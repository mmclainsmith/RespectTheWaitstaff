# CS 116 Final supplement
#### AKA respect the waitstaff
An only somewhat convoluted exploit of service workers.

#### Deliverable:

A demo of how to create a malicious service worker via XSS/JSONP abuse that injects malicious javascript.

## Goals:

#### Original project goal:
I was inspired <sup>1</sup> to see how far I could get in building a persistent service worker that executed arbitrary code in the background of Chrome.

#### Updated Project goal:
After attempting to figure out the continuous activity aspect of this <sup> see notes </sup> I decided to try and create a demo of a service worker created via XSS with its script stored in a different domain.

#### Learning goals:
* Gain some understanding of
    * Promises
    * Service workers
    * New javascript request APIs


## Running Instructions:
#### Requirements:
* `Python 3+`
* `Flask `

In two different terminal windows, navigate to the evil and server folders.

Use `flask run --port=<port>` to get both servers started. Make sure the normal server is running at port 5000 and the evil server at port 8000.

Navigate to `localhost:8000\` and follow the instructions.



#### Required vulnerabilities:
This exploit relies on a site both being susceptible to both XXS and having an unprotected JSONP endpoint.


I also had to turn off XSS-protection on the server since otherwise Chrome would detect and block the XSS, but I am using incredibly basic XSS rather than focusing on finding evasion strategies.


## Implementation/development notes:
Can't find much on the [SyncManager](https://developer.mozilla.org/en-US/docs/Web/API/SyncManager), which the suggested method of persistence in the original article. The source they provide has critical links to documentation that no longer exists.

Tried self-messaging method <sup>3</sup>, but it only has life time of [5 minutes](https://github.com/w3c/ServiceWorker/issues/980). The foreign-fetch has also been patched.

Given the difficulty with persistent service workers, I've decided to switch my focus onto being sneaky with service workers.

Using JavaScript redirects rather than links hides the link preview. If this was getting sent through emails a url shortener would probably need to be employed.  

I have determined via testing (aka adding an update button and inserting a console.log(e.request.url)) that update requests for the service worker do not seem to pass through the service worker itself. This prevents an attacker from bootstrapping their way into a valid looking script location that they can intercept via their own malicious service worker. Confirmed [here](https://gist.github.com/Rich-Harris/fd6c3c73e6e707e312d7c5d7d0f3b2f9)

Further experiment: Can you get push notifications working from the evil server?

## Resources:
1. Original inspiration, [MarioNet article](https://arxiv.org/pdf/1810.00464.pdf)

* Mozilla's [practical examples](https://serviceworke.rs/), for ref.

* [Blog post](https://sakurity.com/blog/2016/12/10/serviceworker_botnet.html) on abusing service workers.

* Google developer [intro](https://developers.google.com/web/fundamentals/primers/service-workers/#the_service_worker_life_cycle), [live-cycle guide](https://developers.google.com/web/fundamentals/primers/service-workers/lifecycle#updates)

* [Flask JSONP wrapper](https://github.com/miguelgrinberg/oreilly-flask-apis-video/issues/6)

* XSS/JSONP/Service Workers [video](https://www.youtube.com/watch?v=VtFHxU_IYLA) and [blog post](https://c0nradsc0rner.com/2016/06/17/xss-persistence-using-jsonp-and-serviceworkers/) w/ code snippets

* [Modifying Response](http://craig-russell.co.uk/2016/01/26/modifying-service-worker-responses.html), v useful code snippet

