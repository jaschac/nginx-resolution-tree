# **nginx-resolution-tree**
#### Table of Contents
1. [Legal notice and disclaimer](#legal-notice-and-disclaimer)
2. [Overview](#overview)
    * [The Resolution Problem](#the-resolution-problem)
    * [A Resolution Example](#a-resolution-example)
3. [Features](#features)
    * [What nginx-resolution-tree Does](#what-nginx-resolution-tree-does)
    * [What nginx-resolution-tree Does Not](#what-nginx-resolution-tree-does-not)
4. [Reference](#reference)
5. [Setup](#setup)
    * [Installing through pip](#installing-through-pip)
    * [Installing by manually building](#installing-by-manually-building)
6. [Usage](#usage)
    * [Unit Tests](#unit-tests)
7. [Limitations](#limitations)

## **Legal notice and disclaimer**
**This package is distributed under the Apache version 2.0 License, in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT  SHALL THE AUTHOR(s) BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF  SUCH DAMAGE.**

Make sure to read the [LICENSE](https://github.com/jaschac/nginx-resolution-tree/blob/master/LICENSE) that is distributed with `nginx-resolution-tree`.

## Overview
`nginx-resolution-tree`, also known as `nrt`, is a Python package that generates *production ready* Nginx's vhost configuration files by resolving different listening ports, server names and locations scenarios. 

Before installing and/or using `nginx-resolution-tree` make sure to check:

 - The [official Nginx documentation](http://nginx.org/en/docs/http/request_processing.html) for an in-depth description of how requests are processed.
 - The [Legal notice and disclaimer](#legal-notice-and-disclaimer). By installing and/or using `nrt` or any of its modules, **you accept and agree** with the terms it is distributed with.

#### The Resolution Problem
`nginx-resolution-tree` has been developed to support the [docker-nginx](https://github.com/jaschac/docker-nginx) project, which required a system able to generate valid Nginx virtual host configuration files dynamically, based on the containers it is linked with at execution time. It's sole role is thus to validate Nginx scenarios and generate valid *production ready* configuration files ready to be deployed.

As the official documentation states, *Nginx first tests the IP address and port of the request against the listen directives of the server blocks. It then tests the “Host” header field of the request against the server_name entries of the server blocks that matched the IP address and port. If the server name is not found, the request will be processed by the default server.*.

The typical scenario `nrt` is used in is that of an Nginx container linked with several others, each bearing details, including the listening port(s), the server name(s) and the location(s) to serve. Given these details, `nrt` builds a *tree-like* structure that allows it to:

 - Validate the input, spotting collisions.
 - Properly group the linked containers into valid vhost configuration files.

#### A Resolution Example
In order to show how `nrt` works, let's get through an example. Let imagine we have 3 containers linked to the same fourth Nginx (`docker-nginx`) container. The linked containers provide the fourth with the following **signatures**:

```sh
# alias:listening address:listening port:server name:location
gunicorn1:0.0.0.0:80:gunicorn1.lostinmalloc.com:/
gunicorn1:0.0.0.0:80:gunicorn1.lostinmalloc.com:/gunicorn1/
gunicorn1:0.0.0.0:8080:gunicorn1.lostinmalloc.com:/
gunicorn1:0.0.0.0:8080:gunicorn1.lostinmalloc.com:/gunicorn1/
gunicorn2:0.0.0.0:80:gunicorn2.lostinmalloc.com:/
gunicorn3:0.0.0.0:80:gunicorn2.lostinmalloc.com:/ # collision
gunicorn3:0.0.0.0:80:gunicorn2.lostinmalloc.com:/gunicorn2/
gunicorn3:0.0.0.0:80:gunicorn2.lostinmalloc.com:/home/
gunicorn3:0.0.0.0:8080:gunicorn3.lostinmalloc.com:/
```
These signatures are turned into the following Resolution Tree by `nrt`:
```sh
                                                                     NRT
                                                                      +
                                                                      |
                                 +------------------------------------+--------------------------------------+
                                 |                                                                           |
                                 v                                                                           v
                            0.0.0.0:80                                                                  0.0.0.0:8080
                                 +                                                                           +
                                 |                                                                           |
            +--------------------+----------------------+                      +-----------------------------+-------------+
            |                                           |                      |                                           |
            |                                           |                      |                                           |
            v                                           v                      v                                           v
gunicorn1.lostinmalloc.com                gunicorn2.lostinmalloc.com    gunicorn1.lostinmalloc.com       gunicorn3.lostinmalloc.com
           +                                       +                               +                               +
    +------+-----+                 +---------------+---+-------------+          +--+---------+                     |
    |            |                 |                   |             |          |            |                     |
    |            |                 |                   |             |          |            |                     |
    v            v                 v                   v             v          v            v                     v
    /       /gunicorn1/            /                 /home/     /gunicorn2/     /       /gunicorn1/                /
    +            +          +-------------+            +             +          +            +                     +
    |            |          |             |            |             |          |            |                     |
    |            |          |             |            |             |          |            |                     |
    v            v          v             v            v             v          v            v                     v
gunicorn1    gunicorn1  gunicorn2    gunicorn3     gunicorn1     gunicorn1  gunicorn1    gunicorn1             gunicorn3
                                    (collision)
```
Without considering the collision, `nginx-resolution-tree` would generate the following `server blocks`:

 - gunicorn1.lostinmalloc.com
   - listen 80
     - 2 locations
   - listen 8080
     - 1 location
 - gunicorn2.lostinmalloc.com
   - listen 80
     - 3 locations
 - gunicorn3.lostinmalloc.com
   - listen 8080
     - 1 location

## Features
`nginx-resolution-tree` is oriented to solve a very specific problem. As such it offer features aimed specifically at it, and nothing else.

#### What nginx-resolution-tree Does

 - Validates the input, failing in case containers collide.
 - Generates valid *production-ready* Nginx virtual host configuration files, one per `server_name`. 
 - Produces configurations able to serve Green Unicorn and PHP-FPM powered web applications.

#### What nginx-resolution-tree Does NOT
`nginx-resolution-tree`  is NOT responsible of:

 - Installing, configuring and deploying Ngnix.
 - Guaranteeing the remote servers are ready to listen to the given ports.

## Reference
The `nginx-resolution-tree` package is split into the following modules, each presenting a class named after it:

  - `nrt`
  - `listen`
  - `server_name`
  - `location`


#### Nrt
This module defines the `Nrt` class, which represents the resolution problem *per se*.

An NRT tree takes, as an input, a list of directives. Each synthetises the specific blocks required
to serve content at a specific location. Each directive is represented as a dictionary, whose keys
are a mandatory `signature` and optional `parameters`. The former is a colon separated string,
while the latter is, again, a dictionary which contains extra information such as default servers
and redirections.

The `Nrt` class is responsible of igniting the process of resolution of the input directives into
objects and relationships, and, eventually, into vhost configuration files, if the overall scenario
is *Nginx valid*. As such, an `Nrt` instance occupies **the root of the resolution tree**. Its
children are, in order, instances of the `Listen`, `ServerName` and `Location` classes. They do
occupy the second, third and fouth levels of the Nrt tree. The leafs of the tree are the aliases of
the containers. They are not represented by a class.

An `Nrt` instance, *per se*, does keep track of its unique `Listen` objects. This is achieved
through a dictionary which maps the unique address to the reference itself. The `Nrt` class is thus
responsible of instantiating Listen instances. The Nrt class, though, is not responsible of
generating any other component of the tree. Each level of the tree is indeed responsible of
generating its lower level, properly mapping those objects.


#### Listen
This module defines the `Listen` class, which represent a unique IP:port pair. This pair is usually
referred to as the address. It defaults to 0.0.0.0:80 and it is only able to deal with IPv4
addresses. Each `Listen` object is associated a list of unique server names.

`Listen` objects are the first to be checked when a signature is resolved into an Nginx Resolution
Tree.

#### Server Name
This module defines the `ServerName` class, which represents the server name that Nginx will try to
match once the listen directive has been satisfied. The server name is very likely to be a domain
or a subdomain, such as `example.com` or `www01.example.com`, but regular expressions are also
valid. If Nginx cannot match a server to the request, or if the request does not come with a host
field, the first entry that matched the listen directive will serve.

Each `ServerName` class is uniquely identified by a name, referred to as `domain`. Different
subdomains of the same domain are different `ServerName` objects, unless they are all catched
through a regular expression. Each `ServerName` instance is also associated a list of `Location`
objects.

#### Location
This module defines the `Location` class, which represent an Nginx's location block and its
properties. Multiple location blocks can be present within the same server block, but they must be
unique. Each instance of the `Location` class is identified by its name. The name of a location must
start and end with a forward slash, with the unique exception of the root location, which is
represented by a single forward slash.

A `Location` is associated to a list of containers, referred to as `alias`. For an Nginx configuration
file to be valid, multiple containers must not redefine the same location within the same server
block.

## Setup
`nrt` can be installed either through `pip` or by manually building it from the source. In both cases, the best scenario is to install it in a completely sandboxed [virtual environment](https://virtualenv.readthedocs.org/en/latest), which guarantees isolation from other projects and their dependencies. Note that in all cases, unless in a virtual environment, the install command needs to be executed as `sudo`.

#### Installing through pip
First thing first, make sure to install `nrt`'s dependencies. Installing all of them at once is very straightfoward:

```bash
$ pip install -r requirements
```

Next, proceed to install `nrt`:

```bash
$ pip install nginx-resolution-tree-x.y.z.tar.gz
```

#### Installing by manually building
If you are not using `pip` then you should. But if you really want to go on without it, then you are responsible to manually build and install not only `nrt` itself, but also all of its dependencies, if any. These are listed in the `requirements` file present in the root of the project. The packages can be downloaded from `PyPi`. Each should come with its own installation instructions.

Once the dependencies have been installed, `nrt` must be retrieved. There are two ways to get the source:

  - Downloading it in `.tar.gz`.
  - Cloning it from GitHub.

If you have the `.tar.gz`, then you must, first of all, extract it:

```bash
$ gunzip nginx-resolution-tree-x.y.z.tar.gz
$ tar xvf nginx-resolution-tree-x.y.z.tar
$ cd nginx-resolution-tree
```

If you instead prefer to clone the Git repository:

```bash
$ git clone git@github.com:jaschac/nginx-resolution-tree.git nginx-resolution-tree
$ cd nginx-resolution-tree
```

In both cases we end up inside the root directory of the project, which has the following structure:

```bash
nginx-resolution-tree/
├── [ 11K]  [ 11K]  LICENSE
├── [ 195]  MANIFEST.in
├── [ 583]  metadata.json
├── [4.0K]  nrt
│   ├── [   0]  __init__.py
│   ├── [2.9K]  listen.py
│   ├── [2.5K]  location.py
│   ├── [5.0K]  nrt.py
│   ├── [2.4K]  servername.py
│   └── [4.0K]  tests
│       ├── [4.0K]  files
│       │   ├── [   0]  listen.p
│       │   ├── [   0]  location.p
│       │   ├── [   0]  nrt.p
│       │   └── [   0]  servername.p
│       ├── [   0]  __init__.py
│       ├── [1.9K]  test_base.py
│       ├── [ 11K]  test_listen.py
│       ├── [7.3K]  test_location.py
│       ├── [9.2K]  test_nrt.py
│       └── [6.6K]  test_servername.py
├── [4.4K]  README
├── [ 15K]  README.md
├── [   0]  requirements
└── [ 742]  setup.py
```

We can now build and install `nrt`. These steps are the same independently of the way we had the package.

```bash
$ python setup.py build
$ python setup.py install
```


## Usage
@TODO

#### Unit Tests
`nrt` comes with an **exhaustive** set of unit tests. Make sure all of them pass before committing any change to the `master` branch.

```bash
$ for module in listen location nrt servername; do python -m unittest nrt.tests.test_$module; done

----------------------------------------------------------------------
Ran 24 tests in 0.006s
OK
----------------------------------------------------------------------
Ran 12 tests in 0.002s
OK
----------------------------------------------------------------------
Ran 18 tests in 0.004s
OK
----------------------------------------------------------------------
Ran 10 tests in 0.002s
OK
```

## Limitations
`nrt` has been developed and tested with the following scenarios. It is not guaranteed to work otherwise.

  - Linux
    - Debian
      - 3.2.68-1+deb7u6
      - 3.2.73-2+deb7u1
      - 3.16.7-ckt11-1+deb8u6~bpo70+1-amd64
  - Python
    - 3.4.3
  - pip
    - 7.1.2 (python 3.4)
  - virtualenv
    - 13.1.2