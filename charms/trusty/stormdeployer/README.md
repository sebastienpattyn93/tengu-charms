StormCharmConnector
===================

The storm charm connector is a library used by the StormDeployer subordinate Juju charm that provides a Storm bolt, spout, etc. with the host, port, user, password, etc. for the services that are related to the subordinate charm.

StormDeployer
=============

The storm deployer is a tool to deploy topologies to a Storm cluster that was deployed via Juju.
Deployment is possible via source code or via jar. A .storm yaml file is needed with deploy configurations. An example can be seen [here](https://github.com/xannz/WordCountExample).

Deploying with source code requires a .stom with the format:
```
topology:
    - name: name of the topology (this should be the same as the topologyname which is used in submitTopology())
      jar: jar of the topology
      topologyclass: full domain and class of the topology
      packaging: mvn package
      repository: the git url where the topology can be found
      scriptbeforepackaging: optional script to run before packaging
      scriptbeforedeploying: optional script to run before deployment
      datasources:
      - parameters:
        - {name: name1, value: value1}
        - {name: name2, value: value2}
        type: type, can my mysql/mongo/postgres/redis/kafka/etc.
        script: script to execute
    - name: another topology
```

Deploying with jar requires a .storm with the format:
```
topology:
    - name: WordCount
      jar: WordCountExample-1.0-SNAPSHOT.jar
      topologyclass: com.sborny.wordcountexample.WordCountTopology
      packaging: jar
      repository: https://github.com/xannz/WordCountExample.git
      release: https://github.com/xannz/WordCountExample/releases/download/1.0/WordCountExample-1.0-SNAPSHOT.jar
```

Deploying from a private repository requires username and password wich can be entered as credentials in the config:
```
juju set stormdeployer "credentials=username:password"
juju set stormdeployer "deploy=[url to .storm file on github]"
juju set stormdeployer "undeploy=TopologyName"
```
Deploying a topology with starting parameters is possible by entering them after the name:
```
-topology
  -name: ExampleTopologyName Arg1 Arg2
  ...
```

# Contact Information

## Bugs

Report bugs on [Github](https://github.com/IBCNServices/tengu-charms/issues).

## Authors

This software was created in the [IBCN research group](https://www.ibcn.intec.ugent.be/) of [Ghent University](http://www.ugent.be/en) in Belgium. This software is used in [Tengu](http://tengu.intec.ugent.be), a project that aims to make experimenting with data frameworks and tools as easy as possible.

- Sander Borny <sander.borny@ugent.be>
- Maarten Ectors <maarten.ectors@canonical.com>
- Merlijn Sebrechts <merlijn.sebrechts@gmail.com>
- Rocket icon made by [Dave Gandy](http://www.flaticon.com/authors/dave-gandy) from [www.flaticon.com](http://www.flaticon.com) licensed as [Creative Commons BY 3.0](http://creativecommons.org/licenses/by/3.0/)
