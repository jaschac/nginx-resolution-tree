# **nginx-resolution-tree**
#### Table of Contents
1. [Overview](#overview)
    * [The Resolution Problem](#the-resolution-problem)
2. [Legal notice and disclaimer](#legal-notice-and-disclaimer)
3. [Features](#features)
    * [What nginx-resolution-tree Does](#what-nginx-resolution-tree-does)
    * [What nginx-resolution-tree Does Not](#what-nginx-resolution-tree-does-not)
4. [Setup](#setup)
5. [Usage](#usage)
    * [Unit Tests](#unit-tests)
6. [Limitations](#limitations)
7. [FAQs](#faqs)

## Overview
`nginx-resolution-tree` is a Python package that generates *production ready* Nginx's vhost configuration files by resolving different listening ports, server names and locations scenarios. 

Before installing and/or using `nginx-resolution-tree`, also known as `nrt`, make sure to check:

 - The [Official Nginx Documentation](http://nginx.org/en/docs/http/request_processing.html) for an in-depth description of how requests are processed.
 - The [Legal notice and disclaimer](#legal-notice-and-disclaimer) before installing it. By installing and/or using `nrt` or any of its modules, **you accept and agree** with the terms it is distributed with.

#### The Resolution Problem
`nginx-resolution-tree` has been developed to support the [docker-nginx](https://github.com/jaschac/docker-nginx) project, which required a system able to generate valid Nginx virtual host configuration files dynamically, based on the containers it is linked with at execution time. It's sole role is thus to validate Nginx scenarios and generate valid *production ready* configuration files ready to be deployed.

As the Official Nginx Documentation states, requests are validated first against the IP:port, then against server names. Finally the location.

The typical scenario `nrt` is used in is that of an Nginx container linked with several others, each bearing details, including the listening port(s), the server name(s) and the location(s) to serve. Given these details, `nrt` builds a *tree-like* structure that allows it to:

 - Validate the input, spotting collisions.
 - Properly group the linked containers into valid vhost configuration files.

#### **Legal notice and disclaimer**
**This package is distributed under the Apache version 2.0 License, in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT  SHALL THE AUTHOR(s) BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF  SUCH DAMAGE.**

Make sure to read the `LICENSE` that is distributed with `nginx-resolution-tree`.

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
