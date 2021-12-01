# holidays-jp

🎌 holidays-jp generates data for the API that provides Japanese holidays.

## API

### Date format JSON

https://kenkyu392.github.io/holidays-jp/v1/date.json

```javascript
{
  "holidays": [
    {
      "date": "1955-01-01",
      "i18n": {
        "en-US": "New Year’s Day",
        "ja-JP": "元日"
      }
    },
    .
    .
    .
  ]
}
```

### Date Time format JSON

https://kenkyu392.github.io/holidays-jp/v1/datetime.json

```javascript
{
  "holidays": [
    {
      "date": "1955-01-01T00:00:00+09:00",
      "i18n": {
        "en-US": "New Year’s Day",
        "ja-JP": "元日"
      }
    },
    .
    .
    .
  ]
}
```

### Unix Time format JSON

https://kenkyu392.github.io/holidays-jp/v1/unixtime.json

```javascript
{
  "holidays": [
    {
      "date": -473418000,
      "i18n": {
        "en-US": "New Year’s Day",
        "ja-JP": "元日"
      }
    },
    .
    .
    .
  ]
}
```

### Yearly JSON

You can access the data by year in `/v1/<year>/<format>.json`.

- https://kenkyu392.github.io/holidays-jp/v1/2021/date.json
- https://kenkyu392.github.io/holidays-jp/v1/2021/datetime.json
- https://kenkyu392.github.io/holidays-jp/v1/2021/unixtime.json

## License

[MIT](LICENSE)
