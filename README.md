# What is this?

See docs under "notes" folder.

# How to use this?

## Run Python code

Run from project root directory using `-m`, for example

```shell
python -m foo.bar
```

# Directory Structure

## `datastruct`

Common data structures when data is exchanged between data collection and analysis.

## `datacollection`

For collecting data; use `provider` to reader collected data.

## `analysis`

For performing analysis; use `datasource` to read collected data (from `provider`).

## `tool`

Common tools.