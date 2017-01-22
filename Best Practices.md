# Best Practices

## Extracting from HTML

The following formats return `null` in a timely manner if the regex isn't matched. Replace `YOUR_REGEX_HERE`.

`script` field:

```
function process(url, completionHandler) { var xmlhttp = new XMLHttpRequest(); xmlhttp.onreadystatechange = function() { if (xmlhttp.readyState == 4 && xmlhttp.status == 200) { var res = xmlhttp.responseText; var regex = RegExp('.*(YOUR_REGEX_HERE).*'); var results = regex.exec(res); var match = null; if (results != null && results.length > 1) { match = results[1]; }; completionHandler(match); } }; xmlhttp.open('GET', url, true); xmlhttp.send(); }
```

`script2` field:

```
function process(url, completionHandler) { var res = httpRequest(url); var regex = RegExp('.*(YOUR_REGEX_HERE).*'); var results = regex.exec(res); var match = null; if (results != null && results.length > 1) { match = results[1] }; completionHandler(match); }
```

## URL Encoding

Replace `YOUR_*_HERE`.

`script` and `script2` fields:

```
function process(url, completionHandler) { completionHandler('YOUR_SCHEME_HERE://YOUR_PATH_HERE?url=' + encodeURIComponent(url)); }
```
