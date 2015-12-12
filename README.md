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
6. [Usage](#usage)
    * [Unit Tests](#unit-tests)
7. [Limitations](#limitations)
8. [FAQs](#faqs)

## **Legal notice and disclaimer**
**This package is distributed under the Apache version 2.0 License, in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT  SHALL THE AUTHOR(s) BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF  SUCH DAMAGE.**

Make sure to read the `LICENSE` that is distributed with `nginx-resolution-tree`.

## Overview
`nginx-resolution-tree` is a Python package that generates *production ready* Nginx's vhost configuration files by resolving different listening ports, server names and locations scenarios. 

Before installing and/or using `nginx-resolution-tree`, also known as `nrt`, make sure to check:

 - The [official Nginx documentation](http://nginx.org/en/docs/http/request_processing.html) for an in-depth description of how requests are processed.
 - The [Legal notice and disclaimer](#legal-notice-and-disclaimer) before installing it. By installing and/or using `nrt` or any of its modules, **you accept and agree** with the terms it is distributed with.

#### The Resolution Problem
`nginx-resolution-tree` has been developed to support the [docker-nginx](https://github.com/jaschac/docker-nginx) project, which required a system able to generate valid Nginx virtual host configuration files dynamically, based on the containers it is linked with at execution time. It's sole role is thus to validate Nginx scenarios and generate valid *production ready* configuration files ready to be deployed.

As the official documentation states, *Nginx first tests the IP address and port of the request against the listen directives of the server blocks. It then tests the “Host” header field of the request against the server_name entries of the server blocks that matched the IP address and port. If the server name is not found, the request will be processed by the default server.*.

The typical scenario `nrt` is used in is that of an Nginx container linked with several others, each bearing details, including the listening port(s), the server name(s) and the location(s) to serve. Given these details, `nrt` builds a *tree-like* structure that allows it to:

 - Validate the input, spotting collisions.
 - Properly group the linked containers into valid vhost configuration files.

#### A Resolution Example
In order to show how `nrt` works, let's get through an example. Let imagine we have 3 containers linked to the same fourth Nginx container. The linked containers provide the fourth with the following **signatures**:

```sh
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
These signatures are turned into the following Resolution Tree:
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
    +------+-----+                 +---------------+---+-------------+             |                               |
    |            |                 |                   |             |             |                               |
    |            |                 |                   |             |             |                               |
    v            v                 v                   v             v             v                               v
    /       /gunicorn1/            /                 /home/     /gunicorn2/        /                               /
    +            +          +-------------+            +             +             +                               +
    |            |          |             |            |             |             |                               |
    |            |          |             |            |             |             |                               |
    v            v          v             v            v             v             v                               v
gunicorn1    gunicorn1  gunicorn2    gunicorn3     gunicorn1     gunicorn1     gunicorn1                       gunicorn3
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
 - Produces configurations able to serve Green Unicorn and PPHP-FPM powered web applications.

#### What nginx-resolution-tree Does NOT
`nginx-resolution-tree`  is NOT responsible of:

 - Installing, configuring and deploying Ngnix.
 - Guaranteeing the remote servers are ready to listen to the given ports.

## Reference
The `nginx-resolution-tree` package is split into the following modules, each presenting a class named after it: `nrt`, `listen`, `server_name`, and `location`.

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
@TODO

## Usage
@TODO

#### Unit Tests
@TODO

## Limitations
@TODO

## Frequently Asked Questions
@TODO

