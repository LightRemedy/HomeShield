# modules/telegram.py
import streamlit as st
import requests
from .logger import logger

class TelegramConfig:
    def __init__(self):
        if "telegram_configured" not in st.session_state:
            st.session_state.telegram_configured = False
        if "show_success_message" not in st.session_state:
            st.session_state.show_success_message = False

    def configure_sidebar(self):
        st.sidebar.subheader("Telegram Alerts")

        if not st.session_state.telegram_configured:
            with st.sidebar.expander("Configure Telegram"):
                bot_token = st.text_input(
                    "Telegram Bot Token",
                    value="",
                    type="password"
                )
                chat_id = st.text_input(
                    "Telegram Chat ID",
                    value="",
                    type="password"
                )

                if st.button("Save Telegram Settings"):
                    if bot_token.strip() == "" or chat_id.strip() == "":
                        st.sidebar.error("Both Bot Token and Chat ID are required.")
                    else:
                        # Save bot token and chat ID in session state
                        st.session_state.bot_token = bot_token
                        st.session_state.chat_id = chat_id
                        st.session_state.telegram_configured = True
                        st.session_state.show_success_message = True
                        logger.info("Telegram settings configured.")

                        # Use st.query_params to reload
                        st.query_params["reload"] = ["true"]

        if st.session_state.telegram_configured:
            if st.session_state.show_success_message:
                st.sidebar.success("Telegram settings saved successfully!")
                st.session_state.show_success_message = False

            st.session_state.enable_telegram = st.sidebar.checkbox(
                "Enable Telegram Notifications",
                value=st.session_state.get("enable_telegram", False)
            )

    def send_telegram_alert(self, detection_type: str, mode: str, confidence: float):
        bot_token = st.session_state.get("bot_token")
        chat_id = st.session_state.get("chat_id")

        if not bot_token or not chat_id:
            st.warning("Please configure Telegram Bot Token and Chat ID in the settings.")
            logger.warning("Telegram alert attempted without configuration.")
            return

        try:
            if detection_type.lower() == "fire":
                alert_message = f"🔥 *Fire Alert!* Fire detected through *{mode}* with confidence of {confidence:.2f}%!"
            else:
                alert_message = f"💨 *Smoke Alert!* Smoke detected through *{mode}* with confidence of {confidence:.2f}%!"

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {"chat_id": chat_id, "text": alert_message, "parse_mode": "Markdown"}

            response = requests.post(url, data=data)
            if response.status_code == 200:
                st.info("Alert sent successfully!")
                logger.info(f"Sent {detection_type} alert via Telegram.")
            else:
                st.error(f"Failed to send alert: {response.json().get('description')}")
                logger.error(f"Failed to send Telegram alert: {response.json().get('description')}")
        except Exception as e:
            st.error(f"Error sending Telegram message: {e}")
            logger.error(f"Error sending Telegram message: {e}")
