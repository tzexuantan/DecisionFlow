from io import BytesIO 
import base64
import streamlit as st

def save_chart_as_img(ax, chart_title, figsize=(10,9)):
    try:
        ax.figure.set_size_inches(figsize)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        buf = BytesIO()
        ax.figure.savefig(buf, format="png")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        img = f'<img src="data:image/png;base64,{image_base64}" />'
    
        st.session_state.messages.append({"user": "bot", "message": f"Here is the chart: {chart_title}"})
        st.session_state.messages.append({"user": "bot", "message": img})
        bot_response = "Please visit Visualizations for more customization!"
        st.session_state.messages.append({"user": "bot", "message": bot_response})

    except Exception as e:
        st.error(f"An error occurred while generating the chart: {e}")