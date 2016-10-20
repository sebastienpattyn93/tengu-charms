Overview
--------

The Spout charm represents an Apache Storm spout.
Required Apache Storm version is 0.10 +.

Usage
-----

This charm can be used in the following way:

```
juju deploy zookeeper
juju deploy storm stormmaster
juju deploy storm stormworker
juju add-relation zookeeper stormmaster
juju add-relation zookeeper stormworker
juju add-relation stormmaster:master stormworker:worker

juju deploy storm-topology topo
juju add-relation topo stormmaster
juju deploy spout spout1
juju add-relation spout1 stormmaster
juju add-relation spout1 topo

juju set spout1 "class=https://raw.githubusercontent.com/xannz/WordCountExample/master/src/main/java/com/sborny/wordcountexample/RandomSentenceSpout.java"
```


# Contact Information

## Bugs

Report bugs on [Github](https://github.com/IBCNServices/tengu-charms/issues).

## Authors

This software was created in the [IBCN research group](https://www.ibcn.intec.ugent.be/) of [Ghent University](http://www.ugent.be/en) in Belgium. This software is used in [Tengu](http://tengu.intec.ugent.be), a project that aims to make experimenting with data frameworks and tools as easy as possible.

- Sander Borny <sander.borny@ugent.be>
- Merlijn Sebrechts <merlijn.sebrechts@gmail.com>