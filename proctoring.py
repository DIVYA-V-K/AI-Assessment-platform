import streamlit as st
import streamlit.components.v1 as components

def monitor_user_behavior():
    # Initialize alert count if not already set
    if "alert_count" not in st.session_state:
        st.session_state["alert_count"] = 0

    # JavaScript injection to monitor tab switch, copy-paste, right-click
    components.html(f"""
        <script>
        let alertCount = {st.session_state["alert_count"]};
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                alertCount += 1;
                window.parent.postMessage({{ type: "alert-trigger", count: alertCount }}, "*");
                alert("⚠️ Tab switching is not allowed! (" + alertCount + "/3)");
                if (alertCount >= 3) {{
                    window.parent.postMessage({{ type: "exit-test" }}, "*");
                    window.location.href = "/";  // Redirect to home page (Start New Assessment)
                }}
            }}
        }});

        document.addEventListener('copy', function(e) {{
            e.preventDefault();
            alert("❌ Copying is disabled during the test.");
        }});
        document.addEventListener('paste', function(e) {{
            e.preventDefault();
            alert("❌ Pasting is disabled during the test.");
        }});
        document.addEventListener('contextmenu', function(e) {{
            e.preventDefault();
        }});
        </script>
    """, height=0)

    # Script to listen for postMessage from iframe JS
    st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            const data = event.data;
            if (data.type === "alert-trigger") {
                fetch(`/alert_count_update?count=${data.count}`);
            } else if (data.type === "exit-test") {
                fetch(`/exit_test`);
            }
        });
        </script>
    """, unsafe_allow_html=True)


def handle_alert_routes():
    query_params = st.query_params  # Replaced st.experimental_get_query_params() with st.query_params
    if "alert_count_update" in query_params:
        count = int(query_params.get("count", [0])[0])
        st.session_state["alert_count"] = count
        if st.session_state["alert_count"] >= 3:
            # After the 3rd alert, redirect the user to "Start New Assessment" page
            st.session_state["page"] = "home"  # Reset to home page
            st.session_state["questions"] = []
            st.session_state["user_answers"] = {}
            st.session_state["alert_count"] = 0
            st.rerun()  # Rerun to reflect changes
    if "exit_test" in query_params:
        st.session_state["page"] = "home"
        st.session_state["questions"] = []
        st.session_state["user_answers"] = {}
        st.session_state["alert_count"] = 0
        st.rerun()