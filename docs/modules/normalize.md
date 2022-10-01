## Normalize

<br>

### Clean string
- Remove double-whitespace
- Remove tab, newline, return, formfeed, etc.
- Replace accented characters (e.g. ö becomes o)
- Trim leading and trailing whitespace

```console
import datahopper.normalize import clean_string
```
<br>

### Rename DataFrame columns

```console
import datahopper.normalize import rename_column
```

<br>

### Drop DataFrame rows with missing values

```console
import datahopper.normalize import drop_rows_missing_values
```
