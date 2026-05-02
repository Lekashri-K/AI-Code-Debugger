import streamlit as st
import io
import contextlib
from debugger import AICodeDebugger

st.set_page_config(page_title="Friendly AI Debugger", page_icon="🐍")
debugger = AICodeDebugger()

st.title("🐍 Beginner's AI Code Debugger")
st.write("Paste your code and error below to get a simple explanation.")

col1, col2 = st.columns(2)

with col1:
    code_in = st.text_area("Your Python Code:", height=200, placeholder="print(x + ' years')")
    err_in = st.text_area("The Error Message:", height=100, placeholder="TypeError: ...")
    
    if st.button("Explain Fix 🔍"):
        if code_in and err_in:
            with st.spinner("Analyzing..."):
                res = debugger.explain_error(err_in, code_in)
                st.session_state.explanation = res['explanation']
        else:
            st.warning("Please fill both boxes.")

with col2:
    st.subheader("🤖 AI Explanation")
    if 'explanation' in st.session_state:
        st.markdown(st.session_state.explanation)
    else:
        st.info("Results will appear here.")

# Code Sandbox
st.divider()
if st.button("▶️ Test Run My Code"):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            exec(code_in)
            st.success("Code ran successfully!")
            st.code(output.getvalue())
        except Exception as e:
            st.error(f"Execution Failed: {e}")
