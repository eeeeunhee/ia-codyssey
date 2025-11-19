
import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 파일 읽기
def load_csv_files(train_path, test_path):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

# 2. 두 데이터 합치기
def merge_dataframes(df1, df2):
    merged_df = pd.concat([df1, df2], ignore_index=True)
    return merged_df

# 3. 데이터 전체 개수 확인
def count_rows(df):
    return len(df)

# 4. Transported와 가장 관련 있는 항목 찾기
def find_most_related_column(df):
    if 'Transported' in df.columns:
        df = df.copy()
        df['Transported'] = df['Transported'].astype(int)
    numeric_df = df.select_dtypes(include='number')
    if 'Transported' not in numeric_df.columns:
        return None
    correlation = numeric_df.corr()['Transported'].abs().sort_values(ascending=False)
    return correlation.index[1]

# 5. 나이를 10대, 20대, ...로 나누는 함수
def categorize_age(age):
    if pd.isna(age):
        return None
    return int(age) // 10 * 10

# 6. 나이대별 Transported 여부 그래프
def plot_transported_by_age(df):
    df['AgeGroup'] = df['Age'].apply(categorize_age)
    grouped = df.groupby(['AgeGroup', 'Transported']).size().unstack(fill_value=0)
    grouped.plot(kind='bar')
    plt.title('Transported by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

# 7. Destination별 연령대 분포 그래프
def plot_age_distribution_by_destination(df):
    df['AgeGroup'] = df['Age'].apply(categorize_age)
    grouped = df.groupby(['Destination', 'AgeGroup']).size().unstack(fill_value=0)
    grouped.plot(kind='bar', stacked=True)
    plt.title('Age Group Distribution by Destination')
    plt.xlabel('Destination')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

# 8. 전체 실행
def main():
    train, test = load_csv_files('train.csv', 'test.csv')
    merged = merge_dataframes(train, test)
    print('전체 데이터 수량 :', count_rows(merged))
    related = find_most_related_column(train)
    if related is not None:
        print('Transported와 가장 관련성 높은 항목 :', related)
    plot_transported_by_age(train)
    plot_age_distribution_by_destination(train)

if __name__ == '__main__':
    main()
