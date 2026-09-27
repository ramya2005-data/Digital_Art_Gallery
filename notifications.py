import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide"
)

# ---------------- STYLING ----------------

st.markdown("""
<style>

.stApp {
    background-color: #F7F3EE;
}

h1 {
    color: #2F2925;
}

h2, h3 {
    color: #4B4038;
}

.notification-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border-left: 5px solid #8B7355;
}

</style>
""", unsafe_allow_html=True)

st.title("🔔 Notifications")

st.write(
    "View updates about your artwork requests."
)

st.markdown("---")

# ---------------- USER CHECK ----------------

user_email = st.session_state.get(
    "user_email"
)

if not user_email:

    st.warning(
        "Please login to view your notifications."
    )

    if st.button("Go to Login"):

        st.switch_page(
            "pages/login.py"
        )

else:

    # ---------------- DATABASE ----------------

    connection = sqlite3.connect(
        "gallery.db"
    )

    notifications = connection.execute(
        """
        SELECT id, message, created_at, is_read
        FROM notifications
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (user_email,)
    ).fetchall()

    connection.close()

    # ---------------- DISPLAY ----------------

    if not notifications:

        st.info(
            "You don't have any notifications yet."
        )

    else:

        st.subheader(
            f"Notifications for {user_email}"
        )

        for notification in notifications:

            notification_id = notification[0]
            message = notification[1]
            created_at = notification[2]
            is_read = notification[3]

            st.markdown(
                '<div class="notification-card">',
                unsafe_allow_html=True
            )

            if is_read == 0:

                st.write(
                    "🆕 **New Notification**"
                )

            else:

                st.write(
                    "🔔 Notification"
                )

            st.write(message)

            st.caption(
                f"📅 {created_at}"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            # Mark as read

            if is_read == 0:

                if st.button(
                    "Mark as Read",
                    key=f"read_{notification_id}"
                ):

                    connection = sqlite3.connect(
                        "gallery.db"
                    )

                    connection.execute(
                        """
                        UPDATE notifications
                        SET is_read = 1
                        WHERE id = ?
                        """,
                        (notification_id,)
                    )

                    connection.commit()
                    connection.close()

                    st.rerun()