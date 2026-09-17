from pathlib import Path
import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title='판매 대시보드',
    page_icon='🔮',
    layout='wide',
)

# 2. 데이터 경로 설정 및 로드
TARGET_DIR = 'data'
TARGET_CSV = 'data.csv'

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / TARGET_DIR / TARGET_CSV

df = pd.read_csv(DATA_PATH)

st.title('판매 대시보드')

# 3. 사이드바 필터링 영역
with st.sidebar:
    st.header('조회조건')

    # 선택된 지역을 region 변수에 저장 (데이터의 실제 지역 목록을 동적으로 가져옵니다)
    region = st.selectbox(
        '지역',
        ['전체', *(df['region'].unique().tolist())]
    )

    # 선택된 최소매출 금액을 minimum_sales 변수에 저장
    minimum_sales = st.slider(
        '최소매출',
        min_value=0,
        max_value=int(df['sales'].max()),
        value=0,
        step=500_000
    )

# 4. 데이터 필터링 로직 (사이드바 외부로 이동하여 순서 보장)
filtered = df[df['sales'] >= minimum_sales].copy()

if region != '전체':
    filtered = filtered[filtered['region'] == region]

##kpi
##1. 총매출
##2. 총 판매량
##3. 평균매출
##4. 사용된 데이터 행수

total_sales = filtered['sales'].sum()

total_amount = filtered['quantity'].sum()

total_rows = len(filtered)

if total_rows >0:
    average_sales = filtered['sales'].mean()
else:
    average_sales = 0

col1, col2, col3,col4 = st.columns(4)

with col1:
    st.metric(
        label='총매출',
        value=f'{total_sales:,}원',
        border = True
    )

with col2:
    st.metric(
        label='총판매량',
        value=f'{total_amount:,}건',
        border=True
        )
with col3:
    st.metric(
        label='평균매출',
        value=f'{average_sales:,}원',
        border = True
    )

with col4:
    st.metric(
        label='데이터 행수',
        value=f'{total_rows:,}건',
        border = True
    )

st.divider()

if filtered.empty:
    st.success('조건에 맞는 데이터가 맞습니다!')

monthly_sales = filtered.groupby('month')['sales'].sum().reset_index()

left,right = st.columns([2,1])

with left:
    st.subheader('월별 매출')

    st.line_chart(
        monthly_sales,
        x = 'month',
        y = 'sales',

    )
with right:
    st.subheader('조회 데이터')
    st.dataframe(
        filtered,
        hide_index=True,
        column_config={
            'quantity': st.column_config.NumberColumn(
                '판매량',
                format='%d개'
            ),
            'sales': st.column_config.NumberColumn(
                '매출액',
                format='%d원'  # 매출액 단위 포맷도 추가 가능
            )
        }
    )

