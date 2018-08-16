# Data Transformation and Analysis

About how data are transformed and analyzed.

## Structure

Directories and their purpose:
1. `datasource`: provides all data.
1. `trading`: trading related lib.
1. `prototype`: research-like notebooks and utils for the prototype phase of the project.

## Tools Searching

### Aylien Text Analysis API

Registed using `chih.chiu.19@gmail` and password `S*97`, see [page](https://developer.aylien.com/).

SDK reference: https://aylien.com/text-api/sdks/

## Ideas

### Aggregating reports into events

One idea is to break reports into paragraphs, then use text similarity of the paragraphs to group them into clusters. Each cluster corresponds to an event.