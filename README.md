# ip-000021

Display name: APB Quad SPI Master Controller

UID: ip-000021

Family: spi

Category: peripheral

Repository: git@github.com:openecos-projects/apb-quad-spi-master-controller.git

Upstream: local reference source under `ref/apb_spi_master`

Current baseline: local reference snapshot from 2026-06-15

License: Solderpad Hardware License 0.51

Status: candidate, source snapshot

This repository is managed as a child repository of `ip-catalog`.

## Summary

APB-based SPI/QSPI master controller with command, address, dummy-cycle and
data phase control, programmable clock divider, independent TX/RX FIFOs,
up to four chip-select outputs, and threshold-based interrupt event output.

The local repository contains a source mirror from `ref/apb_spi_master` for
catalog evaluation. The current RTL baseline should be treated as a local
reference source snapshot rather than an automatically synchronized upstream
checkout.

## Layout

```text
rtl/       Verilog RTL copied from ref/apb_spi_master
docs/      Datasheet and provenance notes
reports/   Review, lint, simulation, or synthesis report summaries
scripts/   Local metadata validation helper
```

## Top Level

The integration top module is:

```text
apb_spi_master
```

Top-level interfaces:

```text
APB slave ports; SPI/QSPI pins; interrupt event output
```

## Catalog Mapping

The corresponding catalog record is expected at:

```text
data/ip/peripheral/ip-000021.yaml
```

The local metadata source is:

```text
ip.yaml
```
