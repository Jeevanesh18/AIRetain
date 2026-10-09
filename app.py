import streamlit as st
import plotly.express as px
from data_loader import load_data
from ai_engine import generate_ai_insight
import pandas as pd
# --- PAGE CONFIG ---
st.set_page_config(page_title="RetainAI | Glocomp", layout="wide")
st.title("🧠 RetainAI: Glocomp Action-Loop Dashboard")

# --- LOAD DATA ---
employees, onboarding, pulse, exit_surv, actions = load_data()

# --- SIDEBAR: GLOBAL FILTERS & API ---
with st.sidebar:
    st.header("⚙️ Settings & Filters")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Get this from Google AI Studio")
    
    st.divider()
    st.subheader("Global Filters")
    selected_location = st.selectbox("Location", ["All"] + list(employees['location'].unique()))
    selected_division = st.selectbox("Division", ["All"] + list(employees['division'].unique()))

# Apply Filters
def filter_data(df):
    if selected_location != "All" and 'location' in df.columns:
        df = df[df['location'] == selected_location]
    if selected_division != "All" and 'division' in df.columns:
        df = df[df['division'] == selected_division]
    return df

f_onboarding = filter_data(onboarding)
f_pulse = filter_data(pulse)
f_exit = filter_data(exit_surv)

# --- 4 TAB STRUCTURE ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Onboarding Hub", "🌊 Wave Analyzer", "📈 Trend & Impact", "🚨 Leavers & Flight Risk"])

# ==========================================
# TAB 1: ONBOARDING HUB (UPGRADED UI)
# ==========================================
with tab1:
    st.header("🚀 New Joiner Onboarding Experience")

    # 1. High-Level KPI Summary
    col1, col2, col3, col4 = st.columns(4)
    avg_clarity = f_onboarding['role_clarity'].mean()
    avg_tools = f_onboarding['tools_access'].mean()
    avg_support = f_onboarding['manager_support'].mean()
    
    # Calculate % of joiners struggling (< 3.0 overall score)
    low_scorers = f_onboarding[f_onboarding['overall_score'] < 3.0]
    struggle_rate = (len(low_scorers) / len(f_onboarding) * 100) if len(f_onboarding) > 0 else 0

    col1.metric("Avg Role Clarity", f"{avg_clarity:.1f} / 5.0")
    col2.metric("Avg Tools Access", f"{avg_tools:.1f} / 5.0")
    col3.metric("Avg Manager Support", f"{avg_support:.1f} / 5.0")
    col4.metric("At-Risk Joiners (<3.0)", f"{len(low_scorers)} ({struggle_rate:.0f}%)", delta_color="inverse")

    st.divider()

    # 2. Top 3 Problems & Contextual AI Action Section
    st.subheader("⚠️ Top 3 Onboarding Bottlenecks & Action Plans")
    st.write("Identifies recurring complaints from employees rating their experience under 3.0, mapped to their specific division and location.")

    if st.button("✨ Identify Problems & Prescribe Actions", type="primary", key="btn_onboard_ai"):
        if low_scorers.empty:
            st.success("🎉 No onboarding responses below 3.0 found for the selected filter.")
        else:
            with st.spinner("AI is synthesizing low-scoring feedback across locations and divisions..."):
                # Prepare a structured payload of comments + dept + location
                feedback_sample = low_scorers[['division', 'location', 'overall_score', 'comment']].dropna().head(12).to_dict(orient='records')
                
                # Fetch structured output
                from ai_engine import generate_structured_actions
                recommendations = generate_structured_actions(feedback_sample, gemini_key)

                if recommendations:
                    # Display the Top 3 cards in clean containers
                    for idx, item in enumerate(recommendations, 1):
                        with st.container(border=True):
                            header_col, badge_col = st.columns([3, 1])
                            
                            severity_color = "red" if item.get("severity") == "Critical" else ("orange" if item.get("severity") == "High" else "blue")
                            header_col.markdown(f"### #{idx}: {item.get('problem', 'Identified Issue')}")
                            badge_col.markdown(f"**Severity:** :{severity_color}[{item.get('severity', 'High')}]")

                            # Context tags
                            c1, c2, c3 = st.columns(3)
                            c1.caption(f"🏢 **Division:** {item.get('department', 'All')}")
                            c2.caption(f"📍 **Location:** {item.get('location', 'All')}")
                            c3.caption(f"👤 **Accountable Owner:** **{item.get('owner', 'HR Lead')}**")

                            # Prescribed action box
                            st.markdown(f"**💡 Targeted Action Plan:**")
                            st.info(item.get("action", "No action provided."))
                else:
                    st.error("Failed to parse AI output. Check API key or data format.")

    # 3. Clean collapsible view for transparency
    with st.expander("🔍 View Raw Survey Feedback (Overall Score < 3.0)"):
        st.dataframe(
            low_scorers[['employee_id', 'division', 'location', 'overall_score','manager_support','role_clarity', 'tools_access', 'comment']],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# TAB 2: WAVE ANALYZER (SYNCHRONIZED WITH TAB 3)
# ==========================================
with tab2:
    st.header("🌊 Pulse Survey Wave Analyzer")
    st.caption("Inspect a single wave's metrics, flag underperforming scores (< 3.5), discover problem clusters, and generate accountable fixes.")

    # 1. Wave Selection
    wave_options = ["Survey 1 (2026-Q1_1)", "Survey 2 (2026-Q1_2)"]
    selected_wave = st.selectbox("Select Survey Wave to Inspect", wave_options, index=0)
    
    # Synchronized Scores matching Tab 3 perfectly
    if "1" in selected_wave:
        scores = {
            "Overall Engagement": 2.4,
            "Workload Stress": 1.8,
            "Tools & Access": 2.1,
            "Manager Support": 2.3,
            "Career Growth": 2.9
        }
        unhappy_count = 45
        total_respondents = 320
    else:
        scores = {
            "Overall Engagement": 3.1,
            "Workload Stress": 1.5,
            "Tools & Access": 4.0,
            "Manager Support": 2.5,
            "Career Growth": 3.0
        }
        unhappy_count = 38
        total_respondents = 315

    # 2. Metric Scorecards
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Engagement Score", f"{scores['Overall Engagement']:.1f} / 5.0")
    m2.metric("Workload", f"{scores['Workload Stress']:.1f} / 5.0")
    m3.metric("Tools & Access", f"{scores['Tools & Access']:.1f} / 5.0")
    m4.metric("Manager Support", f"{scores['Manager Support']:.1f} / 5.0")
    m5.metric("Career Growth", f"{scores['Career Growth']:.1f} / 5.0")

    st.divider()

    # 3. Underperforming Scores Watchlist (< 3.5 Threshold)
    st.subheader("⚠️ Metric Health & Dimension Watchlist")
    low_scores = {k: v for k, v in scores.items() if v < 3.5}
    
    if low_scores:
        st.warning(f"Found **{len(low_scores)} dimensions** falling below the healthy threshold (< 3.5 / 5.0):")
        cols = st.columns(len(low_scores))
        for idx, (dim, val) in enumerate(low_scores.items()):
            with cols[idx]:
                sev = "🔴 Critical" if val < 2.0 else "🟡 Needs Attention"
                st.markdown(f"**{dim}**")
                st.markdown(f"Score: `{val:.1f}` ({sev})")
    else:
        st.success("All dimensions are currently performing at or above healthy baseline (>= 3.5).")

    st.divider()

    # Session state for persistent button outputs
    if f"clusters_{selected_wave}" not in st.session_state:
        st.session_state[f"clusters_{selected_wave}"] = None
    if f"actions_{selected_wave}" not in st.session_state:
        st.session_state[f"actions_{selected_wave}"] = None

    # 4. STEP 1: Problem Clustering Engine
    st.subheader("1️⃣ Problem Clustering Engine")
    st.write(f"Clusters complaints from the **{unhappy_count} unhappiest employees** (Score < 3.0) in this wave.")

    if st.button("🔍 Discover Problem Clusters", type="primary", key="btn_cluster"):
        with st.spinner("Clustering complaints and ranking by severity..."):
            from ai_engine import cluster_unhappy_feedback
            st.session_state[f"clusters_{selected_wave}"] = cluster_unhappy_feedback(selected_wave, gemini_key)
            st.session_state[f"actions_{selected_wave}"] = None  # Reset downstream actions

    # Render Clusters
    current_clusters = st.session_state[f"clusters_{selected_wave}"]
    if current_clusters:
        st.markdown("#### 🚨 Discovered Problem Clusters (Ranked by Urgency)")
        for item in current_clusters:
            with st.container(border=True):
                c_title, c_badge = st.columns([3, 1])
                sev_color = "red" if item.get("severity") == "Critical" else "orange"
                c_title.markdown(f"**Rank #{item.get('rank')}: {item.get('cluster_title')}**")
                c_badge.markdown(f"**Severity:** :{sev_color}[{item.get('severity')}]")
                
                st.write(f"📌 **Core Issue:** {item.get('summary')}")
                st.caption(f"📊 **Impact:** {item.get('affected_ratio')} | 💬 *\"{item.get('sample_quote')}\"*")

        st.divider()

        # 5. STEP 2: Prescribe Actions (Combines Clusters + Low Scores < 3.5)
        st.subheader("2️⃣ Prescribe Accountable Actions")
        st.write("Generates concrete fixes for both the **discovered clusters** and the **scores below 3.5**.")

        if st.button("📋 Generate Targeted Action Plan", key="btn_pulse_actions"):
            with st.spinner("Generating targeted action cards with assigned owners..."):
                from ai_engine import generate_actions_for_pulse_clusters
                st.session_state[f"actions_{selected_wave}"] = generate_actions_for_pulse_clusters(
                    current_clusters, low_scores, selected_wave, gemini_key
                )

        # Render Actions
        current_actions = st.session_state[f"actions_{selected_wave}"]
        if current_actions:
            st.markdown("#### ✅ Prescribed Action Cards (Fed directly into Tab 3's Tracker)")
            for act in current_actions:
                with st.container(border=True):
                    st.markdown(f"##### 🎯 Target: {act.get('target')}")
                    st.markdown(f"**Action Step:** {act.get('action')}")
                    
                    a_col1, a_col2 = st.columns(2)
                    a_col1.caption(f"👤 **Accountable Owner:** **{act.get('owner')}**")
                    a_col2.caption(f"📈 **Target KPI:** `{act.get('target_metric')}`")

                    
# ==========================================
# TAB 3: TREND & ACTION IMPACT (SYNCHRONIZED LOOP)
# ==========================================
with tab3:
    st.header("📈 Survey 1 vs. Survey 2: The Decision Loop")
    st.caption("Tracking how specific management actions impacted scores and whether Survey 1's problem clusters were resolved or are still active.")

    from ai_engine import evaluate_action_impact_and_clusters
    report = evaluate_action_impact_and_clusters(gemini_key)

    # 1. Multi-Metric Comparison Chart (All scores from Survey 1 to Survey 2)
    st.subheader("1️⃣ Score Movements (Survey 1 ➡️ Survey 2)")
    
    chart_data = pd.DataFrame({
        "Survey Wave": ["Survey 1 (Baseline)", "Survey 2 (Follow-up)"] * 5,
        "Metric": [
            "Tools & Access", "Tools & Access",
            "Workload", "Workload",
            "Manager Support", "Manager Support",
            "Career Growth", "Career Growth",
            "Engagement Score", "Engagement Score"
        ],
        "Score": [
            2.1, 4.0,   # Tools & Access (+1.90)
            1.8, 1.5,   # Workload (-0.30)
            2.3, 2.5,   # Manager Support (+0.20)
            2.9, 3.0,   # Career Growth (+0.10)
            2.4, 3.1    # Engagement Score (+0.70)
        ]
    })
    
    fig_sync = px.line(
        chart_data, 
        x="Survey Wave", 
        y="Score", 
        color="Metric", 
        markers=True,
        title="Metric Trajectory Across Waves (1.0 to 5.0 Scale)"
    )
    fig_sync.update_yaxes(range=[1.0, 5.0])
    st.plotly_chart(fig_sync, use_container_width=True)

    # 2. Score Delta Summary Cards
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Tools & Access", "4.0 / 5.0", delta="+1.90 (Lift)", delta_color="normal")
    d2.metric("Workload", "1.5 / 5.0", delta="-0.30 (Drop)", delta_color="inverse")
    d3.metric("Manager Support", "2.5 / 5.0", delta="+0.20 (Minor Lift)", delta_color="normal")
    d4.metric("Engagement Score", "3.1 / 5.0", delta="+0.70 (Recovering)", delta_color="normal")

    st.divider()

    # 3. Two-Column Deep Dive: Clusters vs. Actions Taken
    col_clusters, col_actions = st.columns([1, 1])

    # Left Column: Problem Clusters in Survey 1 vs Survey 2
    with col_clusters:
        st.subheader("2️⃣ Cluster Survival Tracker")
        st.write("Did the complaints identified in Survey 1 disappear or persist in Survey 2?")
        
        for cl in report["cluster_comparison"]:
            with st.container(border=True):
                status_color = "green" if cl["status"] == "Resolved" else "red"
                st.markdown(f"**{cl['cluster_name']}**")
                st.markdown(f"**Status:** :{status_color}[**{cl['status']}**]")
                st.caption(f"📊 {cl['evidence']}")

    # Right Column: Management Actions & Attributed Verdicts
    with col_actions:
        st.subheader("3️⃣ Action Accountability & ROI")
        st.write("Which actions succeeded, which failed, and who is responsible?")
        
        for act in report["actions_verdict"]:
            with st.container(border=True):
                v = act["verdict"]
                v_color = "green" if v == "Effective" else ("red" if v == "Ineffective" else "orange")
                
                h1, h2 = st.columns([3, 1])
                h1.markdown(f"**Action:** {act['action']}")
                h2.markdown(f":{v_color}[**{v}**]")
                
                c1, c2 = st.columns(2)
                c1.caption(f"🎯 **Target:** {act['target_cluster']}")
                c2.caption(f"👤 **Owner:** **{act['owner']}**")
                
                st.write(f"💡 *{act['reasoning']}*")



# ==========================================
# TAB 4: LEAVERS & FLIGHT RISK RADAR
# ==========================================
with tab4:
    st.header("🚨 Retention & Predictive Flight Risk Radar")
    st.caption("Inspect verified exit survey data across years, identify macro retention trends, and intercept active flight risks using vector similarity.")

    # 1. Year Filter & Primary Exit Reasons
    col_yr, col_empty = st.columns([1, 2])
    selected_year = col_yr.selectbox("📅 Select Exit Year to Analyze", ["2026", "2025", "2024"], index=0)

    # Bar chart for exit reasons tailored to year
    st.subheader(f"1️⃣ Primary Exit Reasons ({selected_year})")
    
    mock_exit_reasons = {
        "2026": {"Workload & Burnout": 23, "Manager Relationship": 14, "Career Opportunity": 10, "Tools & Access": 8},
        "2025": {"Career Opportunity": 20, "Certification Deficit": 14, "Manager Relationship": 10, "Compensation": 6},
        "2024": {"Culture / Team Fit": 18, "Manager Relationship": 15, "Compensation": 10, "Role Clarity": 7}
    }
    
    df_reasons = pd.DataFrame(
        list(mock_exit_reasons[selected_year].items()), 
        columns=["Primary Reason", "Number of Leavers"]
    )
    
    fig_reasons = px.bar(
        df_reasons, 
        x="Primary Reason", 
        y="Number of Leavers", 
        color="Number of Leavers",
        color_continuous_scale="Reds",
        title=f"Distribution of Resignation Drivers ({selected_year})"
    )
    st.plotly_chart(fig_reasons, use_container_width=True)

    st.divider()

    # 2. Top 3 Problem Clusters via Vector Similarity + Prescribed Actions
    st.subheader(f"2️⃣ Top 3 Exit Problem Clusters ({selected_year})")
    st.write(f"Unsupervised Vector Clustering of exit comments in **{selected_year}** synthesized into root causes and recommended actions:")

    from ai_engine import get_exit_clusters_by_year, get_multi_year_retention_trends, find_flight_risks_mock
    clusters = get_exit_clusters_by_year(selected_year, gemini_key)

    for item in clusters:
        with st.container(border=True):
            h1, h2 = st.columns([3, 1])
            h1.markdown(f"**Rank #{item['rank']}: {item['cluster']}**")
            h2.caption(f"📊 `{item['frequency']}`")
            
            st.write(f"🔍 **Root Cause:** {item['description']}")
            
            c1, c2 = st.columns([3, 1])
            c1.info(f"💡 **Recommended Action:** {item['action']}")
            c2.caption(f"👤 **Owner:** **{item['owner']}**")

    st.divider()

    # 3. Macro Multi-Year Trend Analysis (All Years)
    st.subheader("3️⃣ Multi-Year Macro Retention Trends")
    st.write("Compare systemic patterns across 2024, 2025, and 2026 to see what has improved vs. what is chronic.")

    if st.button("📊 Analyze Multi-Year Trend (2024 - 2026)", key="btn_multi_year"):
        trends = get_multi_year_retention_trends(gemini_key)
        
        col_chronic, col_resolved = st.columns(2)
        
        # Column A: Chronic Issues
        with col_chronic:
            st.markdown("#### 🔴 Chronic Issues (Exist in All Years)")
            for ch in trends["chronic_issues"]:
                with st.container(border=True):
                    st.markdown(f"**{ch['issue']}**")
                    st.markdown(f":red[**{ch['status']}**]")
                    st.caption(f"⚠️ {ch['impact']}")
                    st.write(f"📌 *{ch['insight']}*")

        # Column B: Resolved / Reduced Issues
        with col_resolved:
            st.markdown("#### 🟢 Resolved or Reduced Issues")
            for res in trends["resolved_issues"]:
                with st.container(border=True):
                    st.markdown(f"**{res['issue']}**")
                    st.markdown(f":green[**{res['status']}**]")
                    st.caption(f"📉 {res['evidence']}")
                    st.write(f"✅ *{res['why']}*")

    st.divider()

    # 4. Predictive Flight Risk Radar (Vector Matching Active vs. Leavers)
    st.subheader("4️⃣ Predictive Flight Risk Radar (Active Employees)")
    st.write("Scans active pulse survey comments against historical exit vectors. Flags high-risk employees before they submit resignations.")

    if st.button("🔍 Scan Active Workforce for Flight Risks", type="primary", key="btn_scan_risks"):
        risks = find_flight_risks_mock(f_pulse, f_exit)
        
        st.error(f"🚨 Identified **{len(risks)} Active Employees** exhibiting linguistic similarity to past leavers:")
        
        for r in risks:
            with st.container(border=True):
                top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
                top_col1.markdown(f"👤 **Employee ID:** `{r['employee_id']}` ({r['division']} - {r['location']})")
                top_col2.caption(f"⏳ **Tenure:** {r['tenure_months']} months")
                top_col3.markdown(f"🔥 **Vector Match:** :red[**{r['similarity_score']}%**]")

                st.markdown(f"**Matched Exit Theme:** `{r['matched_exit_theme']}`")
                st.caption(f"💬 *Active Comment:* \"{r['active_comment']}\"")
                
                st.warning(f"⚡ **Recommended Intervention:** {r['recommended_intervention']}")