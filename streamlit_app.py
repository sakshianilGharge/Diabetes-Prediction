import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Diabetes Analytics & Prediction",
    page_icon="🩺",
    layout="wide"
)

model = pickle.load(open("model.pkl", "rb"))
df = pd.read_csv("Diabetic_Prediction.csv")

st.markdown("""
    <style>
        .footer{
            text-align:center;
            color:#BFBFBF;
            font-size:18px;
            margine-top:50px;
            padding:15px 0;
            border-top:1px solid rgba(255, 255, 255, 0.15);
        }
        .footer span{
            color:#00E5FF
            font-weight:700;
            font-size:20px;
        }
    </style>
""",unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    st.title("🏥 Diabetes Prediction & Analytics System")
    st.write("Select a secion below.")

    st.markdown("""
                <style>
                .card{
                    background-color:#1e1e1e;
                    padding:30px;
                    border-radius:20px;
                    text-align:center;
                    box-shadow:0px 4px 15px rgba(0, 255, 255, 0.3);
                    transition: all 0.3s ease;
                }
                .card:hover{
                    transform:translateY(-6px);
                    box-shadow:0px 8px 25px rgba(0, 255, 255, 0.5);
                }
                </style>
                """, unsafe_allow_html=True)

    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
                    <div class="card">
                    <h2>🩺 Prediction</h2>
                    <p>Predict diabetes risk using patient data.</p>
                    </div>
                    """, unsafe_allow_html=True)
        if st.button("Open Prediction"):
            st.session_state.page="Prediction"
            st.rerun()
            
    with col2:
        st.markdown("""
                    <div class="card">
                    <h2>📊Analytics</h2>
                    <p>Explore dataset insights and visualizations.</p>
                    </div>
                    """, unsafe_allow_html=True)
        if st.button("Open Analytics"):
            st.session_state.page = "Analytics"
            st.rerun()

    with col3:
        st.markdown("""
                    <div class="card">
                    <h2>ℹ️ About</h2>
                    <p>Explore dataset insights and visualizations.</p>
                    </div>
                    """, unsafe_allow_html=True)
        if st.button("Open About"):
            st.session_state.page = "About"
            st.rerun()

    st.markdown("""
        <div class="footer">
            Developed by<span>Sakshi Anil Gharge</span>
        </div>
        """, unsafe_allow_html=True)
            
elif st.session_state.page == "Analytics":
    st.title("📊 Analytics Page")

    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Records", len(df))
    with col2:
        st.metric("🩺 Diabetic", int(df["diabetes"].sum()))
    with col3:
        st.metric("👩 Female", (df["gender"]==0).sum())
    with col4:
        st.metric("👨 Male", (df["gender"]==1).sum())

    st.markdown("""
    <style>
    .glass-card{
        background:rgba(255, 255, 255, 0.08);
        backdrop-filter:blur(18px);
        -webkit-backdrop-filter:blur(18px);
                
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius:18px;
                
        padding:20px;
        margin:15px 0;
                
        box-shadow:0 8px 32px rgba(31, 38, 135, 0.25);
    }
    .graph-title{
        font-size:20px;
        font-weight:700;
        color:white;
        margin-bottom:12px;
    }
    .insight-title{
        color:#7dd3fc;
        font-size:18px;
        font-weight:bold;
        margin-bottom:8px;
    }
    .insight-text{
        color:#e5e7eb;
        font-size:15px;
        line-height:1.8;
        white-space: normal;
        overflow:visible;
    }
    </style>
    """, unsafe_allow_html=True)
    st.subheader("📊 Gender Distribution")

    gender_count=df["gender"].replace({
        0: "Female",
        1:"Male"
    }).value_counts()

    female=(df["gender"]==0).sum()
    male=(df["gender"]==1).sum()

    left, right = st.columns([2.4, 1])
    with left: 
        fig=px.bar(
            x=gender_count.index,
            y=gender_count.values,
            labels={"x":"Gender", "y":"Count"},
            color=gender_count.index,
            text=gender_count.values,
        )
        fig.update_layout(
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        
        st.markdown(f"""
                <div class="glass-card">
                <div class="insight-title">Analysis</div>
                <div class="insight-text">
               
                Female Patients:
                {female}
                Male Patients:
                {male}
                The dataset contains a higher number
                of female patients than male patients, 
                indicating that females represents
                the larger portion of the collected 
                records.
            </div>
            </div>
            """, unsafe_allow_html=True)
        
    st.subheader("📊 Diabetes Distribution")

    diabetes_count=df["diabetes"].replace({
        0:"Non-Diabetic",
        1:"Diabetic"
    }).value_counts()
    diabetic = (df["diabetes"]==1).sum()
    non_diabetic=(df["diabetes"]==0).sum()

    right, left = st.columns([2.4, 1])

    with right:
        fig=px.pie(
            names=diabetes_count.index,
            values=diabetes_count.values,
            hole=0.45,
            color=diabetes_count.index,
            color_discrete_map={
                "Diabetic":"#ff4d4d", 
                "Non-Diabetic":"#4CAF50"
            }
        )
        fig.update_traces(
            textinfo="percent+label",
            textfont_size=14
        )
        fig.update_layout(
            height=450,
            font=dict(color="white")
        )
        st.plotly_chart(fig, use_container_width=True)

    with left:
        st.markdown(f"""
                <div class="glass-card">
                <div class="insight-title">Analysis</div>
                <div class="insight-text">
                    
                Diabetic Patients:
                {diabetic}
                Non-Diabetic Patients:
                {non_diabetic}
                Observation:
                This chart shows the proportion of diabetic 
                and non-diabetic patients in the dataset. 
                It provides a quick overview of the distri-
                bution used for prediction.
            </div>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("📊 BMI Distribution")
    left, right = st.columns([1, 2.4])
    with left:
        avg_bmi=df["bmi"].mean()
        min_bmi=df["bmi"].min()
        max_bmi=df["bmi"].max()

        st.markdown(f"""
                <div class="glass-card">
                <div class="insight-title">Analysis</div>
                <div class ="insight-text">
                    
                Average BMI:
                {avg_bmi:.1f}
                Minimum BMI:
                {min_bmi:.1f}
                Maximum BMI:
                {max_bmi:.1f}
                Observation:
                This graph shows how BMI values are
                distributed across all patients. it
                helps identify whether most patients
                fall whithin healthy, overweight, or
                obese BMI ranges.
            </div>
            </div>
            """, unsafe_allow_html=True)
    
    with right:
        fig=px.histogram(
        df,
        x="bmi",
        nbins=30,
        color_discrete_sequence=["#00BFFF"]
        )
        fig.update_traces(
        marker_line_width=1,
        marker_line_color="white"
        )
        fig.update_layout(
        height=450,
        font=dict(color="white"),
        xaxis_title="BMI",
        yaxis_title="Number of Patients"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🚬 Smoking History Distribution")
    smoking_count = df["smoking_history"].replace({
        0: "No Info",
        1: "Current",
        2: "Ever",
        3: "Former",
        4: "Never",
        5: "Not Current"
        }).value_counts()
        
    no_info=(df["smoking_history"]==0).sum()
    current=(df["smoking_history"]==1).sum()
    ever=(df["smoking_history"]==2).sum()
    never=(df["smoking_history"]==3).sum()
    former=(df["smoking_history"]==4).sum()
    not_current=(df["smoking_history"]==5).sum()

        
    fig = px.bar(
        x=smoking_count.index,
        y=smoking_count.values,
        color=smoking_count.index,
        text=smoking_count.values,
        labels={
            "x": "Smoking History",
            "y": "Count"
            }
    )
        
    fig.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1.5
    )
        
    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
    most_common = smoking_count.idxmax()
    count = smoking_count.max()
    st.markdown(f"""
                <div class="glass-card">
                <div class="insight-title">📌 Analysis</div>
                <div class="insight-text">
                    
                    🚬Most Common:
                    NO info: {no_info},  Current: {current}
                    Former: {former},  Ever:  {ever}
                    Not Current: {not_current},  Never: {never}
                    Observation:
                    This chart displays the smoking history of patients. It helps identify lifestyle patterns that may influence diabetes risk.
                </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.subheader("🩸 Blood Glucose Level Distribution")
            
    avg_glucose = df["blood_glucose_level"].mean()
    min_glucose = df["blood_glucose_level"].min()
    max_glucose = df["blood_glucose_level"].max()

    fig = px.histogram(
        df,
        x="blood_glucose_level",
        nbins=20,
        color_discrete_sequence=["#EF4444"]
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=1.5
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="Blood Glucose Level (mg/dL)",
        yaxis_title="Number of Patients"
    )

    st.plotly_chart(fig, use_container_width=True)
        
    st.markdown(f"""
                <div class="glass-card">
                <div class="insight-title">📌 Analysis</div>
                <div class="insight-text">
                    
                🩸 Average:</b> {avg_glucose:.1f} mg/dL<br>
                📉 Minimum:{min_glucose} mg/dL<br>
                📈 Maximum: {max_glucose} mg/dL<br>
                Observation:</b><br>
                This histogram shows the distribution of blood
                glucose levels among patients. Higher glucose 
                values are generally associated with an increased 
                risk of diabetes.
                </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.subheader("💉 HbA1c Level Distribution")
    
    avg_hba1c = df["HbA1c_level"].mean()
    min_hba1c = df["HbA1c_level"].min()
    max_hba1c = df["HbA1c_level"].max()

    fig = px.histogram(
        df,
        x="HbA1c_level",
        nbins=20,
        color_discrete_sequence=["#8B5CF6"]
        )
        
    fig.update_traces(
        marker_line_color="white",
        marker_line_width=1.5
        )
        
    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="HbA1c Level (%)",
        yaxis_title="Number of Patients"
        )

    st.plotly_chart(fig, use_container_width=True)
        
    st.markdown(f"""
                <div class="glass-card">
                <div class="insight-title">📌 Analysis</div>
                <div class="insight-text">
                    
                💉 Average HbA1c: {avg_hba1c:.2f}%<br>
                📉 Minimum: {min_hba1c}%<br>
                📈 Maximum: {max_hba1c}%<br>
                Observation:
                HbA1c reflects the average blood sugar level
                over the past 2–3 months. Higher HbA1c values
                are associated with a greater likelihood of
                diabetes.
                </div>
                </div>
                """, unsafe_allow_html=True)
                
    st.subheader("❤️ Heart Disease vs Diabetes")
    
    
    heart_yes = ((df["heart_disease"] == 1)).sum()
    heart_no = ((df["heart_disease"] == 0)).sum()

    heart_df = (
        df.groupby(["heart_disease", "diabetes"])
        .size()
        .reset_index(name="Count")
        )
        
    heart_df["heart_disease"] = heart_df["heart_disease"].replace({
        0: "No Heart Disease",
        1: "Heart Disease"
        })
        
    heart_df["diabetes"] = heart_df["diabetes"].replace({
        0: "Non-Diabetic",
        1: "Diabetic"
        })
        
    fig = px.bar(
        heart_df,
        x="heart_disease",
        y="Count",
        color="diabetes",
        barmode="group",
        text="Count",
        color_discrete_map={
            "Diabetic": "#EF4444",
            "Non-Diabetic": "#22C55E"
        })
        
    fig.update_traces(textposition="outside")
        
    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="Heart Disease",
        yaxis_title="Patients"
        
        )

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
            <div class="glass-card">
            <div class="insight-title">📌 Analysis</div>
            <div class="insight-text">
            
            ❤️ Heart Disease: {heart_yes}<br>
            💚 No Heart Disease: {heart_no}<br>
            Observation:
            This chart compares the number of diabetic and non-diabetic patients based on heart disease status. It helps identify whether heart disease is associated with diabetes.
            </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.subheader("🩺 Hypertension vs Diabetes")

    hypertension_yes = (df["hypertension"] == 1).sum()
    hypertension_no = (df["hypertension"] == 0).sum()

    hyper_df = (
        df.groupby(["hypertension", "diabetes"])
        .size()
        .reset_index(name="Count")
    )

    hyper_df["hypertension"] = hyper_df["hypertension"].replace({
        0: "No Hypertension",
        1: "Hypertension"
    })

    hyper_df["diabetes"] = hyper_df["diabetes"].replace({
        0: "Non-Diabetic",
        1: "Diabetic"
    })

    fig = px.bar(
        hyper_df,
        x="hypertension",
        y="Count",
        color="diabetes",
        barmode="group",
        text="Count",
        color_discrete_map={
            "Diabetic": "#EF4444",
            "Non-Diabetic": "#22C55E"
        }
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="Hypertension",
        yaxis_title="Number of Patients"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="glass-card">
    <div class="insight-title">📌 Analysis</div>
    <div class="insight-text">

    🩺 Hypertension: {hypertension_yes}<br>
    💚 No Hypertension: {hypertension_no}<br>
    Observation:<br>
    This chart compares diabetic and non-diabetic patients based on hypertension status. It helps understand the relationship between high blood pressure and diabetes.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔥 Correlation Heatmap")
    
    corr = df.drop(columns=["Unnamed: 0"], errors="ignore").corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="Blues",
        aspect="auto"
    )

    fig.update_layout(
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("""
                <div class="glass-card">
                <div class="insight-title">📌 Analysis</div>
                <div class="insight-text">
                    
                🔥 Purpose:<br>
                The correlation heatmap shows how strongly each feature is related to the others.<br>
                📊 Interpretation:<br>
                • Values close to <b>1</b> indicate a strong positive relationship.<br>
                • Values close to <b>-1</b> indicate a strong negative relationship.<br>
                • Values near <b>0</b> indicate little or no relationship.<br>
                Observation:<br>
                Features such as <b>HbA1c Level</b> and <b>Blood Glucose Level</b> generally show the strongest relationship with diabetes, while other features have weaker correlations.
                </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.subheader("🎯 Key Findings")
    
    st.markdown("""
            <div class="glass-card">
            <div class="insight-title">📌 Dashboard Summary</div>
            <div class="insight-text">
                
            ✅ The dataset contains both diabetic and non-diabetic patients for comparison.<br>
            👩 Female patients slightly outnumber male patients in the dataset.<br>
            🩸 Blood Glucose Level and HbA1c Level show the strongest relationship with diabetes.<br>
            ⚖️ Higher BMI values are associated with an increased risk of diabetes.<br>
            👴 Diabetes is more common among older patients.<br>
            ❤️ Heart disease and 🩺 hypertension are more frequently observed in diabetic patients.<br>
            🔥 The correlation heatmap provides an overall view of how different health indicators relate to diabetes.
            </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="footer">
            Developed by<span>Sakshi Anil Gharge</span>
        </div>
        """,unsafe_allow_html=True)

elif st.session_state.page == "Prediction":
    st.title("🤖 Diabetes Prediction")
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
        
    col1, col2 = st.columns([1, 1.3])
        
    with col1:
        st.subheader("📝 Input Details")
        
        gender = st.selectbox(
            "Gender",
            ["Select", "Female", "Male"]
            )
        gender = 1 if gender == "Male" else 0
            
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=25
            )
            
        hypertension = st.selectbox(
            "Hypertension",
            [0, 1]
            )

        heart_disease = st.selectbox(
            "Heart Disease",
            [0, 1]
            )

        smoking_history = st.selectbox(
            "Smoking History",
            [
                "Never",
                "No Info",
                "Current",
                "Former",
                "Ever",
                "Not Current"
            ]
            )
            
        smoking_history_map = {
            "Never": 0,
            "No Info": 1,
            "Current": 2,
            "Former": 3,
            "Ever": 4,
            "Not Current": 5
            }
            
        smoking_history = smoking_history_map[smoking_history]
            
        bmi = st.number_input(
            "BMI",
            min_value=0.0,
            value=25.0
            )

        hba1c = st.number_input(
            "HbA1c Level",
            min_value=0.0,
            value=5.5
            )
            
        glucose = st.number_input(
            "Blood Glucose Level",
            min_value=0,
            value=100
            )
            
        predict = st.button("🔮 Predict")
            
        with col2:
            st.subheader("📊 Prediction Result")
                
            if predict:
                data = np.array([[
                    gender,
                    age,
                    hypertension,
                    heart_disease,
                    smoking_history,
                    bmi,
                    hba1c,
                    glucose
                    ]])
                    
                prediction = model.predict(data)
                probability = model.predict_proba(data)
                    
                risk = probability[0][1] * 100
                    
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk,
                    number={"suffix": "%", 'font':{'size':50}},
                    title={"text": "<b>Diabetes Risk Meter</b>", 'font':{'size':28}},
                    gauge={
                        "axis": {
                            'range':[0, 100],
                            'tickwidth':2,
                            'tickcolor':"white"
                            },
                        "bar": {
                            'color':"#00BFFF",
                            'thickness':0.4
                            },
                        "steps": [
                            {"range": [0, 30], "color": "#1f1f1f"},
                            {"range": [30, 70], "color": "#252525"},
                            {"range": [70, 100], "color": "#2d2d2d"}
                            ],
                        'threshold':{
                            'line':{'color':'#00BFFF', 'width':8},
                            'thickness':0.8,
                            'value':risk                                
                            }
                            }
                        ))
                fig.update_layout(
                    paper_bgcolor="#0E1117",
                    font={'color':"white"},
                    height=500
                    )
                st.plotly_chart(fig, use_container_width=True)
                
                if risk < 30:
                    st.success("""
                               ✅ Low Risk of Diabetes
                               Maintain a healthy lifestyle, balanced diet, and regular exercise.""")
                elif risk < 70:
                    st.warning("""
                               ⚠️ Moderate Risk of Diabetes
                               Consider improving your diet, exercising regularly, and monitoring your health.""")
                else:
                    st.error("""
                             🚨 High Risk Diabetes
                             Please consult a doctor, maintain a healthy lifestyle, and monitor your blood sugar levels regularly.""")
    st.markdown("""
        <div class="footer">
            Developed by<span>Sakshi Anil Gharge</span>
        </div>
        """, unsafe_allow_html=True)
    
elif st.session_state.page == "About":

    st.title("🩺 About Diabetes Analytics & Prediction")

    if st.button("Back to Home"):
        st.session_state.page="Home"
        st.rerun()

    st.markdown("""
    <style>
    .glass-card{
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);

        border:1px solid rgba(255,255,255,0.18);
        border-radius:18px;

        padding:20px;
        margin-bottom:18px;

        box-shadow:0 8px 32px rgba(0,0,0,0.25);
        transition:0.3s;
    }

    .glass-card:hover{
        transform:translateY(-5px);
        box-shadow:0 12px 35px rgba(0,255,255,0.20);
    }

    .glass-title{
        font-size:40px;
        font-weight:700;
        color:#00E5FF;
        margin-bottom:12px;
    }
    .glass-card{
        font-size:35px;
        line-height:1.9;
    }

    .footer{
        text-align:center;
        margin-top:30px;
        color:#CCCCCC;
        font-size:18px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="
        font-size: 45px;
        line-height:2.0;
        color:#F5F5F5;
        text-align:center;
        margin: 20px 0 30px 0;
    ">   
    This application combines <span style="color:#00E5FF;"><b>Machine Learning</b></span>
    and <span style="color:#00F5FF;"><b>Data Analytics</b></span> to predict the likelihood 
    of diabetes based on patient health information.
    It also provides interactive visualizations to understand trends,
    patterns, and relationships within the dataset.
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass-card">
        <div class="glass-title">🎯 Project Objective</div>

        • Predict whether a patient has diabetes.<br>
        • Analyze health factors influencing diabetes.<br>
        • Provide an easy-to-use dashboard.<br>
        • Help understand diabetes through
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
        <div class="glass-title">✨ Features</div>
                    
        • Diabetes Prediction<br>
        • Interactive Analytics Dashboard<br>
        • Modern Graphs & Visualizations<br>
        • Responsive User Interface
        </div>
        """, unsafe_allow_html=True)
        
    with col1:
        st.markdown("""
        <div class="glass-card">
        <div class="glass-title">📊 Dataset Features</div>
                    
        • Gender<br>
        • Age<br>
        • Hypertension         
        • Heart Disease<br>
        • Smoking History        
        • BMI<br>
        • HbA1c Level<br                 
        • Blood Glucose Level<br>
        • Diabetes (Target)
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
        <div class="glass-title">⚙️ Technologies Used</div>
                    
        • Python<br>
        • Streamlit<br>
        • Pandas & NumPy<br>
        • Scikit-learn<br>
        • Plotly
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer">
            Developed by<span>Sakshi Anil Gharge</span>
        </div>
        """, unsafe_allow_html=True)