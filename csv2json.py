import os
import json
import csv
from datetime import datetime, date, timedelta, timezone
from typing import List, Dict, Union

# https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
FILE = 'syukujitsu.csv'

JST = timezone(timedelta(hours=+9), 'JST')

# Defining types for type hints.
Record = Dict[str, Union[str, datetime]]
Records = List[Record]

# Mapping for English names.
en_name = {
    "元日":
        "New Year’s Day",
    "成人の日":
        "Coming of Age Day",
    "建国記念の日":
        "National Foundation Day",
    "天皇誕生日":
        "The Emperor's Birthday",
    "春分の日":
        "Vernal Equinox Day",
    "昭和の日":
        "Showa Day",
    "憲法記念日":
        "Constitution Memorial Day",
    "みどりの日":
        "Greenery Day",
    "こどもの日":
        "Children's Day",
    "海の日":
        "Marine Day",
    "山の日":
        "Mountain Day",
    "敬老の日":
        "Respect for the Aged Day",
    "秋分の日":
        "Autumnal Equinox Day",
    "スポーツの日":
        "Health and Sports Day",
    "体育の日":
        "Health and Sports Day",
    "体育の日（スポーツの日）":
        "Health and Sports Day",
    "文化の日":
        "Culture Day",
    "勤労感謝の日":
        "Labor Thanksgiving Day",
    "振替休日":
        "Substitute Holiday",
    "国民の休日":
        "National Holiday",
    "皇太子明仁親王の結婚の儀":
        "The Rite of Wedding of HIH Crown Prince Akihito",
    "皇太子徳仁親王の結婚の儀":
        "The Rite of Wedding of HIH Crown Prince Naruhito",
    "昭和天皇の大喪の礼":
        "The Funeral Ceremony of Emperor Showa",
    "皇太子明仁親王の即位礼正殿の儀":
        "The Ceremony of the Enthronement of His Majesty the Emperor Akihito",
    "皇太子徳仁親王の即位の日":
        "The Enthronement day of HIH Crown Prince Naruhito",
    "皇太子徳仁親王の即位礼正殿の儀":
        "The Ceremony of the Enthronement of His Majesty the Emperor Naruhito",
}


def is_holiday(records: Records, dt: datetime) -> Records:
    for record in records:
        if record['date'] == dt:
            return record
    return None


def json_datetime_format(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()


def json_date_format(o):
    if isinstance(o, (date, datetime)):
        return o.strftime("%Y-%m-%d")


def json_unixtime_format(o):
    if isinstance(o, (date, datetime)):
        return int(o.timestamp())


json_datetime_options = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
    'default': json_datetime_format,
}

json_date_options = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
    'default': json_date_format,
}

json_unixtime_options = {
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 4,
    'default': json_unixtime_format,
}


def get_holiday_name(dt: datetime, name: str) -> Dict[str, str]:
    # 1959-04-10 皇太子明仁親王の結婚の儀
    if dt.year == 1959 and dt.month == 4 and dt.day == 10:
        name = '皇太子明仁親王の結婚の儀'

    # 1989-02-24 昭和天皇の大喪の礼
    if dt.year == 1989 and dt.month == 2 and dt.day == 24:
        name = '昭和天皇の大喪の礼'

    # 1990-11-12 皇太子明仁親王の即位礼正殿の儀
    if dt.year == 1990 and dt.month == 11 and dt.day == 12:
        name = '皇太子明仁親王の即位礼正殿の儀'

    # 1993-06-09 皇太子徳仁親王の結婚の儀
    if dt.year == 1993 and dt.month == 6 and dt.day == 9:
        name = '皇太子徳仁親王の結婚の儀'

    # 2019-05-01 皇太子徳仁親王の即位の日
    if dt.year == 2019 and dt.month == 5 and dt.day == 1:
        name = '皇太子徳仁親王の即位の日'

    # 2019-10-22 皇太子徳仁親王の即位礼正殿の儀
    if dt.year == 2019 and dt.month == 10 and dt.day == 22:
        name = '皇太子徳仁親王の即位礼正殿の儀'

    return {'ja-JP': name, 'en-US': en_name.get(name, '')}


if __name__ == '__main__':
    records = []
    with open(FILE, newline='', encoding='cp932') as f:
        reader = csv.reader(
            f,
            delimiter=',',
            lineterminator='\r\n',
            skipinitialspace=True,
        )
        next(reader, None)
        for row in reader:
            dt = datetime.strptime(row[0], '%Y/%m/%d').replace(tzinfo=JST)
            i18n = get_holiday_name(dt, row[1])
            records.append({'date': dt, 'i18n': i18n})

    for record in records:
        i18n = record['i18n']
        if i18n['ja-JP'] == '休日':
            tomorrow = is_holiday(records, record['date'] + timedelta(days=1))
            yesterday = is_holiday(records, record['date'] - timedelta(days=1))
            if tomorrow and yesterday:
                i18n['ja-JP'] = '国民の休日'
                i18n['en-US'] = en_name['国民の休日']
            elif yesterday:
                name = yesterday['i18n']['ja-JP']
                i18n['ja-JP'] = f'振替休日（{name}）'
                i18n['en-US'] = f'Substitute Holiday ({en_name[name]})'

    records = sorted(records, key=lambda x: x['date'])

    records_per_year = {}
    for record in records:
        year = record['date'].year
        if year not in records_per_year:
            records_per_year[year] = []
        records_per_year[year].append(record)

    with open('v1/datetime.json', 'w') as f:
        json.dump({'holidays': records}, f, **json_datetime_options)
    with open('v1/time.json', 'w') as f:
        json.dump({'holidays': records}, f, **json_datetime_options)
    with open('v1/date.json', 'w') as f:
        json.dump({'holidays': records}, f, **json_date_options)
    with open('v1/unixtime.json', 'w') as f:
        json.dump({'holidays': records}, f, **json_unixtime_options)

    for year, records in records_per_year.items():
        os.makedirs(f'v1/{year}', exist_ok=True)
        with open(f'v1/{year}/datetime.json', 'w') as f:
            json.dump({'holidays': records}, f, **json_datetime_options)
        with open(f'v1/{year}/time.json', 'w') as f:
            json.dump({'holidays': records}, f, **json_datetime_options)
        with open(f'v1/{year}/date.json', 'w') as f:
            json.dump({'holidays': records}, f, **json_date_options)
        with open(f'v1/{year}/unixtime.json', 'w') as f:
            json.dump({'holidays': records}, f, **json_unixtime_options)
