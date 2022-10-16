### Clean string
- Remove double-whitespace
- Remove tab, newline, return, formfeed, etc.
- Replace accented characters (e.g. ö becomes o)
- Trim leading and trailing whitespace

```console
from datahopper.normalize import clean_string

string = "Älvkarleovägen"
cleaned_string = clean_string(string)
```
<br>

### Rename DataFrame columns

```console
from datahopper.normalize import rename_column

df = pd.DataFrame(columns=["ID", "MUNCIPAL", "COUNTRI", "CONSTINENNT"])
column_names = ["id", "municipality", "country", "continent"]
rename_column(df, column_names)
```

<br>

### Drop DataFrame rows with missing values

```console
from datahopper.normalize import drop_rows_missing_values
```
