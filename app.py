import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Recipe Dataset Viewer",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv(
    "https://huggingface.co/datasets/datahiveai/recipes-with-nutrition/resolve/main/recipes-with-nutrition.csv"
)

df = load_data()

st.title("🍽️ Recipe Dataset Viewer")

st.write(
    f"Dataset gồm **{len(df):,} dòng** và **{len(df.columns)} cột**."
)

search = st.text_input(
    "🔎 Tìm kiếm",
    placeholder="Nhập tên món, nguyên liệu..."
)

if search:
    mask = df.astype(str).apply(
        lambda col: col.str.contains(
            search,
            case=False,
            na=False
        )
    ).any(axis=1)

    filtered_df = df[mask]
else:
    filtered_df = df

PAGE_SIZE = 100

total_rows = len(filtered_df)
total_pages = max(
    1,
    (total_rows + PAGE_SIZE - 1) // PAGE_SIZE
)

if "page" not in st.session_state:
    st.session_state.page = 1

if st.session_state.page > total_pages:
    st.session_state.page = 1

col1, col2, col3, col4, col5 = st.columns(
    [1, 1, 2, 1, 1]
)

with col1:
    if st.button("⏮"):
        st.session_state.page = 1

with col2:
    if st.button("◀"):
        st.session_state.page = max(
            1,
            st.session_state.page - 1
        )

with col3:
    st.markdown(
        f"<center>Page {st.session_state.page} / {total_pages}</center>",
        unsafe_allow_html=True
    )

with col4:
    if st.button("▶"):
        st.session_state.page = min(
            total_pages,
            st.session_state.page + 1
        )

with col5:
    if st.button("⏭"):
        st.session_state.page = total_pages

start = (
    st.session_state.page - 1
) * PAGE_SIZE

end = min(
    start + PAGE_SIZE,
    total_rows
)

page_df = filtered_df.iloc[start:end].copy()

st.write(
    f"**Showing {start + 1:,} – {end:,} "
    f"of {total_rows:,} rows**"
)

st.dataframe(
    page_df,
    use_container_width=True,
    height=650
)
