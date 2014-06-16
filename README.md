# Stresser

Stresser is a large-scale stress testing framework consists of one *Commander*
(client) and an arbitrary number of *Soldiers* (servers).

By broadcasting a pre-defined *task*, the Commander can trigger all Soldiers to
generate workload concurrently.

A *task* can be:

* [Sikuli](http://www.sikuli.org/) - Great for tests based on GUI operations.
* script - e.g. `*.sh` on *nix system or `*.bat` on Windows.
* binary executable.

To generate more stress, just add more Soldiers.

## Installation

You can install Stresser by `pip`:

```bash
pip install stresser
```

## Quick Start

TODO
