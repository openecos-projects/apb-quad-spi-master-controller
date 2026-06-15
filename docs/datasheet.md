## Datasheet

### Overview

The APB Quad SPI Master Controller is a memory-mapped SPI/QSPI master. It
accepts APB register accesses and drives command, address, dummy-cycle and data
phases on standard SPI or quad SPI pins.

The implementation is organized as an APB register block, TX/RX FIFOs, a clock
generator, and a SPI transfer controller.

### Features

- APB slave register interface
- SPI master operation
- Standard SPI transmit and receive
- Quad SPI transmit and receive
- Command, address, dummy and data phase control
- Programmable 8-bit SPI clock divider
- Independent 32-bit TX and RX FIFOs
- Configurable FIFO depth through `BUFFER_DEPTH`
- Up to four chip-select outputs
- FIFO threshold interrupt event output
- Active-low reset
- Synthesizable Verilog RTL

### Top-Level Module

```text
apb_spi_master
```

### Parameters

| Parameter | Default | Description |
|---|---:|---|
| `BUFFER_DEPTH` | `10` | TX/RX FIFO depth |
| `APB_ADDR_WIDTH` | `12` | APB address width; default maps a 4 KiB slave window |

### Interface

| Port | Direction | Description |
|---|---|---|
| `HCLK` | input | APB/system clock |
| `HRESETn` | input | Active-low reset |
| `PADDR` | input | APB address |
| `PWDATA` | input | APB write data |
| `PWRITE` | input | APB write control |
| `PSEL` | input | APB select |
| `PENABLE` | input | APB enable |
| `PRDATA` | output | APB read data |
| `PREADY` | output | APB ready; tied high |
| `PSLVERR` | output | APB error; tied low |
| `events_o` | output | FIFO threshold interrupt event |
| `spi_clk` | output | SPI serial clock |
| `spi_csn0..spi_csn3` | output | Active-low chip selects |
| `spi_sdo0..spi_sdo3` | output | SPI/QSPI output data pins |
| `spi_oe0..spi_oe3` | output | Output enable for data pins |
| `spi_sdi0..spi_sdi3` | input | SPI/QSPI input data pins |

### Register Map

Registers are 32-bit and decoded from `PADDR[5:2]`.

| Offset | Name | Access | Description |
|---:|---|---|---|
| `0x00` | `REG_STATUS` | R/W | Status readback and operation control write |
| `0x04` | `REG_CLKDIV` | R/W | SPI clock divider |
| `0x08` | `REG_SPICMD` | R/W | Command phase data |
| `0x0C` | `REG_SPIADR` | R/W | Address phase data |
| `0x10` | `REG_SPILEN` | R/W | Command, address and data lengths |
| `0x14` | `REG_SPIDUM` | R/W | Dummy cycles for read and write flows |
| `0x18` | `REG_TXFIFO` | W | TX FIFO write port |
| `0x20` | `REG_RXFIFO` | R | RX FIFO read port |
| `0x24` | `REG_INTCFG` | R/W | FIFO interrupt thresholds and interrupt enable |
| `0x28` | `REG_INTSTA` | R | Interrupt event status |

Offset `0x1C` is not decoded by the RTL.

#### REG_STATUS

Read returns the internal 32-bit `spi_status` value assembled by the top module.
The write side is pulse-oriented for transfer start and reset controls.

| Bits | Access | Field | Description |
|---|---|---|---|
| `[0]` | W | `spi_rd` | Start standard SPI read |
| `[1]` | W | `spi_wr` | Start standard SPI write |
| `[2]` | W | `spi_qrd` | Start quad SPI read |
| `[3]` | W | `spi_qwr` | Start quad SPI write |
| `[4]` | W | `spi_swrst` | Pulse software reset/flush |
| `[11:8]` | W | `spi_csreg` | Chip-select value |

The write pulse fields are cleared by the APB register block when no write
transfer is active.

#### REG_CLKDIV

| Bits | Access | Description |
|---|---|---|
| `[7:0]` | R/W | SPI clock divider value |
| `[31:8]` | R | Reads as zero |

#### REG_SPICMD

| Bits | Access | Description |
|---|---|---|
| `[31:0]` | R/W | Command phase shift data |

#### REG_SPIADR

| Bits | Access | Description |
|---|---|---|
| `[31:0]` | R/W | Address phase shift data |

#### REG_SPILEN

| Bits | Access | Field | Description |
|---|---|---|---|
| `[5:0]` | R/W | `spi_cmd_len` | Command phase length |
| `[7:6]` | R | reserved | Reads as zero |
| `[13:8]` | R/W | `spi_addr_len` | Address phase length |
| `[15:14]` | R | reserved | Reads as zero |
| `[31:16]` | R/W | `spi_data_len` | Data phase length |

#### REG_SPIDUM

| Bits | Access | Field | Description |
|---|---|---|---|
| `[15:0]` | R/W | `spi_dummy_rd` | Dummy cycles for read transactions |
| `[31:16]` | R/W | `spi_dummy_wr` | Dummy cycles for write transactions |

#### REG_TXFIFO

| Bits | Access | Description |
|---|---|---|
| `[31:0]` | W | Push one 32-bit word into the transmit FIFO |

#### REG_RXFIFO

| Bits | Access | Description |
|---|---|---|
| `[31:0]` | R | Pop/read one 32-bit word from the receive FIFO |

#### REG_INTCFG

Let `LOG_BUFFER_DEPTH = log2(BUFFER_DEPTH)`.

| Bits | Access | Field | Description |
|---|---|---|---|
| `[LOG_BUFFER_DEPTH:0]` | R/W | `spi_int_th_tx` | TX FIFO threshold |
| `[8 + LOG_BUFFER_DEPTH:8]` | R/W | `spi_int_th_rx` | RX FIFO threshold |
| `[31]` | R/W | `spi_int_en` | Interrupt event enable |

#### REG_INTSTA

| Bits | Access | Description |
|---|---|---|
| `[0]` | R | TX threshold event status |
| `[1]` | R | RX threshold event status |

### Integration Notes

- `PREADY` is always `1'b1`; the block does not insert APB wait states.
- `PSLVERR` is always `1'b0`.
- Standard mode drives only `spi_sdo0`; quad transmit drives all four data
  outputs; quad receive disables all four output enables.
- `events_o` is asserted when enabled FIFO threshold conditions are met.
