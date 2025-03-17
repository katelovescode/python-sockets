# README

Sockets exercise from [Beej's Guide to Networking Concepts](https://beej.us/guide/bgnet0/)

Note: when running the client command, you can use `http://localhost:[port-your-server-is-running-on]/whatever/path/you/could/possibly_even/ever.really/want/index.txt` and it will always just look for `index.txt` in the path where the server is running. I did not do the entire exercise including HTML because the gist is the same and tbh I don't want to write an HTML page today.

Server: `python3 webserver.py 12332`
Client: `python3 webclient.py http://localhost:12332/dir/test.txt 12332`

> NB: for the client, port is required even if you define it in the url path; essentially as long as your URL says "localhost" or is a FQDN this will work against whatever domain you request, HOWEVER **all sub-paths/directories will be stripped** so if you pass `www.google.com/../../../../../../../../../../etc/password` or whatever, you'd be asking for `www.google.com/password`, and with no file extension it'll tell you it's unsupported anyway

Also in turning this into a file serving server, I removed the ability to hit `/` from a browser and get a 200, but you can get the correct responses in a browser if you also pass a filename with any directory path after your server port in the browser address bar.

Try:

- `http://google.com/index.txt`
- `http://localhost:12332/dir/test.txt`
- `http://localhost:12332/test1.txt`
- `http://localhost:12332/test1.pdf`
