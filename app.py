import streamlit as st
import pandas as pd
from match_engine import recommend

# Load data once
DATA_PATH = "internships.csv"
raw_df = pd.read_csv(DATA_PATH, dtype=str).fillna("")
internships = raw_df.to_dict(orient="records")

# Streamlit UI
st.set_page_config(page_title="InternMitra", page_icon="🤝", layout="wide")

st.title("🤝 InternMitra")
st.subheader("AI-Based Internship Recommendation Engine for **PM Internship Scheme** 🇮🇳")

# Dropdown options
education_levels = ['10th', '12th', 'Diploma', 'UG', 'PG', 'PhD']
sample_skills = sorted(list({s.strip() for s in ";".join(raw_df["skills"].astype(str)).split(";") if s.strip()}))
sectors = sorted(list({s.strip() for s in raw_df["sector"].astype(str) if s.strip()}))
states = sorted(list({s.strip() for s in raw_df["state"].astype(str) if s.strip()}))

# Input widgets
education = st.selectbox("📘 Education Level", [""] + education_levels)
sector = st.selectbox("🏢 Preferred Sector", [""] + sectors)
state = st.selectbox("🌍 Preferred State", [""] + states)
remote_pref = st.checkbox("💻 Open to Remote Internships?")
skills = st.multiselect("🛠 Select Your Skills", sample_skills)

if st.button("🔍 Recommend Internships"):
    user_profile = {
        "education": education,
        "sector": sector,
        "state": state,
        "remote": remote_pref,
        "skills": skills
    }

    results = recommend(user_profile, internships, top_n=5)

    if not results:
        st.warning("⚠️ No matching internships found. Try different options.")
    else:
        st.success(f"✅ Found {len(results)} recommended internships")

        for idx, r in enumerate(results, start=1):
            st.markdown(f"### {idx}. **{r.get('title','Internship')}**")
            st.write(f"📍 Location: {r.get('state')} | 🏢 Sector: {r.get('sector')}")
            st.write(f"🎓 Education Required: {r.get('min_education','Any')}")
            st.write(f"🛠 Skills Required: {', '.join(r.get('skills', []))}")
            st.progress(r['score'] / 100)
            with st.expander("Why this recommendation?"):
                for reason in r['reasons']:
                    st.write("- " + reason)
