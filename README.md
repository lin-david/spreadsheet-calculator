# Spreadsheet Calculator
### Calculates complex spreadsheet cell inputs

## Supported Functionalities
1. Supports operations on positive integers and cell references.
2. Detects and reports circular dependencies between cells
3. Supported Operations:
	1. Additon `+`
	2. Subtraction `-`
	3. Multiplication `*`
	4. Division `/`
	5. Cell references `A1`

## Examples
### 1. input001.txt

#### Input:
3 2

A2

4 5 *

A1

A1 B2 / 2 +

3

39 B1 B2 * /

| | 1        | 2           | 3  |
|----| ------------- |---------------| ------|
|A | A2 | 4 5 * | A1|
|B  | A1 B2 / 2 + |3 |39 B1 B2 * /|


#### Output:
20.00000

20.00000

20.00000

8.66667

3.00000

1.50000

| | 1        | 2           | 3  |
|----| ------------- |---------------| ------|
|A| 20.00000     | 20.00000 | 20.00000 |
|B| 8.66667      | 3.00000      | 1.50000 |
