
import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="Resumetric | Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 750 !important;
        letter-spacing: -1.5px;
    }
    .subtitle {
        color: #8892A0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("resumetric.")
st.markdown(
    '<p class="subtitle">Precision in every application.</p>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("Resume Intelligence")
st.write(
    "Understand how your experience aligns with "
    "the requirements of your next opportunity."
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### Your Resume")
    resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Supported format: PDF"
    )

with right:
    st.markdown("#### Target Position")
    job_title = st.text_input(
        "Job Title",
        placeholder="e.g. Software Engineer"
    )

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...",
        height=200
    )

st.divider()

if st.button("Analyze Resume", type="primary"):

    if resume is None:
        st.warning("Please upload a resume.")

    elif not job_description.strip():
        st.warning("Please provide a job description.")

    else:
        try:
            reader = PdfReader(resume)

            resume_text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

            if not resume_text.strip():
                st.error(
                    "No readable text was found. "
                    "Please upload a text-based PDF."
                )
            else:
                st.success("Resume processed successfully.")

                st.subheader("Document Overview")

                col1, col2, col3 = st.columns(3)

                col1.metric("Resume Pages", len(reader.pages))
                col2.metric(
                    "Resume Words",
                    len(resume_text.split())
                )
                col3.metric(
                    "Job Description Words",
                    len(job_description.split())
                )

                if job_title.strip():
                    st.info(f"Target Position: {job_title}")

                with st.expander("Extracted Resume Content"):
                    st.text_area(
                        "Resume Text",
                        resume_text,
                        height=300
                    )

                st.caption(
                    "Skill matching and AI recommendations "
                    "will be available in the next development stage."
                )

        except Exception as error:
            st.error(f"Unable to process this PDF: {error}")
