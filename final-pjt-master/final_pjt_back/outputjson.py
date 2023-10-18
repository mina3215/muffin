import sqlite3
import json
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_pjt_back.settings')
import django
django.setup()
# SQLite 데이터베이스 연결
conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
cursor = conn.cursor()


# 데이터베이스에서 정보를 검색
cursor.execute('SELECT * FROM fan_community_actor_fan')
results = cursor.fetchall()

# 결과 집합의 열 정보 가져오기
columns = [desc[0] for desc in cursor.description]

print(columns)

model = 'fan_community.actor_fan'

# 결과를 JSON 형식으로 변환
json_data = []
for row in results:
    row_data = {  
        "model": model,
        "pk": row[0],
        "fields": {}
    }
    for i in range(1,len(columns)):
        row_data['fields'][columns[i]] = row[i]
    print(row_data)
    json_data.append(row_data)

# JSON 파일로 저장
with open('fan.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=1)

# 연결 종료
cursor.close()
conn.close()