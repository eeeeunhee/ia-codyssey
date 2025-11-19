
import pandas as pd
import matplotlib.pyplot as plt

# 국가통계 포탈에서 다운받은 CSV 파일을 DataFrame으로 읽음
csv_file = "성__연령_및_가구주와의_관계별_인구__시군구_20251119210939.csv"
df = pd.read_csv(csv_file, encoding='utf-8')

# 컬럼들 중에서 일반가구원을 제외한 나머지 컬럼들은 분석에 필요 없으므로 필터링
columns_to_keep = ['시점', '행정구역별(시군구)', '성별', '연령별', '일반가구원']
df = df[columns_to_keep]

# 2015년 이후로 자료가 제공되는 최대 기간의 데이터만 사용한다.
df = df[df['시점'] >= 2015]

# 분석을 위해 행정구역별(시군구) '전국' 데이터만 선택
df = df[df['행정구역별(시군구)'] == '전국']

def convert_age_label(age_str):
    if age_str == '합계':
        return 'Total'
    if age_str == '15세미만':
        return '0-14'
    age_str = age_str.replace('세미만', '') 
    age_str = age_str.replace('세', '')
    age_str = age_str.replace('~', '-')
    return age_str

df['AgeGroup'] = df['연령별'].apply(convert_age_label)

# 2015년 이후 남자 및 여자의 연도별 일반가구원 데이터 통계 출력
df_yearly_male = df[(df['성별'] == '남자') & (df['AgeGroup'] == 'Total')][['시점', '일반가구원']]
df_yearly_female = df[(df['성별'] == '여자') & (df['AgeGroup'] == 'Total')][['시점', '일반가구원']]

print("2015년 이후 남자 일반가구원:\n", df_yearly_male)
print("\n2015년 이후 여자 일반가구원:\n", df_yearly_female)

# 2015년 이후 남자 및 여자의 연령별 일반가구원 데이터 통계 출력
# 남자
df_male = df[df['성별'] == '남자']
df_male_pivot = df_male.pivot(index='시점', columns='AgeGroup', values='일반가구원')
df_male_pivot.columns = df_male_pivot.columns.astype(str)
print("\n남자 연령별 일반가구원 데이터 (2015년 이후):\n", df_male_pivot)

# 여자
df_female = df[df['성별'] == '여자']
df_female_pivot = df_female.pivot(index='시점', columns='AgeGroup', values='일반가구원')
df_female_pivot.columns = df_female_pivot.columns.astype(str)
print("\n여자 연령별 일반가구원 데이터 (2015년 이후):\n", df_female_pivot)

# 2015년 이후 남자 및 여자의 연령별 일반가구원 꺾은선 그래프
# 남자 그래프
plt.figure(figsize=(12, 6))
for col in df_male_pivot.columns:
    plt.plot(df_male_pivot.index, df_male_pivot[col], marker='o', label=col)
plt.title('Population of Household Members by Age (Male) Since 2015')
plt.xlabel('Year')
plt.ylabel('Number of People')
plt.legend(title='Age Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# 여자 그래프
plt.figure(figsize=(12, 6))
for col in df_female_pivot.columns:
    plt.plot(df_female_pivot.index, df_female_pivot[col], marker='o', label=col)
plt.title('Population of Household Members by Age (Female) Since 2015')
plt.xlabel('Year')
plt.ylabel('Number of People')
plt.legend(title='Age Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
