# Stresser

Stresser is a large-scale stress testing framework consists of one
**Commander** (client) and an arbitrary number of **Soldiers** (servers).

By broadcasting a pre-defined **task**, the Commander can trigger all Soldiers
to generate workloads concurrently.

A task can be:

* [Sikuli](http://www.sikuli.org/) - Great for tests based on GUI operations.
* script - e.g. `script.sh` on Unix-like systems or `batch.bat` on Windows.
* bin - Binary executables.

To generate more stress, just add more Soldiers.

## Installation

You can install Stresser by `pip`:

```bash
pip install stresser
```

## Quick Start

Once you've got Stresser installed, prepare config files for the Commander and
Soldiers. Then run `stress-commander` and `stress-soldier` respectively.

### Start Soldiers

A sample configuration file for Soldiers:

```INI
[amqp]
# The AMQP server for message broker
server = 5.5.6.6

[bin]
# Path for Java binary
java_bin = C:\Program Files (x86)\Java\jre6\bin\java.exe
# Path for Sikuli IDE
sikuli_ide = C:\Program Files (x86)\Sikuli X\sikuli-ide.jar
# Path for Shell (*nix systems only)
shell = /bin/zsh
```

Start listening tasks:

```
$ stress-soldier soldier.conf
 [x] Soldier bd88148e-fa36-4017-ac5b-099ba83570fe is awaiting RPC requests
 ...
```

### Start the Commander

A sample configuration file (with a Sikuli task defined) for the Commander:

```INI
[amqp]
# The AMQP server for message broker
server = 5.5.6.6

[task]
# Task name
name = The First Task
# Task type, e.g. sikuli, script, bin.
type = sikuli
# URL for executable which will be downloaded by Soldiers
url = http://5.5.6.6:8000/first.skl
# The number of Soldiers. Commander will stop when the specified number of
# results have got.
count = 32
```

Start broadcasting task:

```
$ stress-commander commander.conf
 [x] Broadcasting task: 'The First Task'...
```

### Soldiers performing task

After the Commander broadcasting a task, Soldiers are wake up to download and
perform that task. You may see following messages on the Soldiers's console:

```
 [x] Soldier bd88148e-fa36-4017-ac5b-099ba83570fe is awaiting RPC requests
 [.] Discoverd task: 'The First Task'
 [.] Downloading task executable from http://5.5.6.6:8000/first.skl
 [.] Running task: 'The First Task'
... (some outputs for task)
 [.] Task: 'The First Task' is completed
```

### The Commander stops after all results from Soldiers are collected

On the Commander's console:

```
 [.] Solider dfbe093d-54e0-4b6d-adb3-6935f3c6a31e took 0:12:02 to complete.
 [.] Solider 1bcfb3e2-dd69-4957-ab6d-be91422c44f7 took 0:12:03 to complete.
 ... (skipped)
 [.] Soldier bd88148e-fa36-4017-ac5b-099ba83570fe took 0:11:59 to complete.
```

The Commander will stop when the task is done on all Soldiers, but Soldiers are
still running, hence you can submit another task over and over again.

## Requirements

You only have to deploy a message broker which speaks
[AMQP](http://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol).

## Versioning
Stresser follows [Semantic Versioning](http://semver.org/), both SemVer and
SemVerTag.
