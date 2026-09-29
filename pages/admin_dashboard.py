import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="👑",
    layout="wide"
)

# -----------------------------
# ADMIN LOGIN CHECK
# -----------------------------

if st.session_state.get("user_role") != "admin":
    st.error("Access denied. Admin login required.")

    if st.button("Go to Login"):
        st.switch_page("pages/login.py")

    st.stop()


# -----------------------------
# DATABASE
# -----------------------------

connection = sqlite3.connect("gallery.db")
cursor = connection.cursor()


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("👑 Admin Panel")

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

    if st.button("🖼️ Gallery", use_container_width=True):
        st.switch_page("pages/gallery.py")

    if st.button("🔔 Notifications", use_container_width=True):
        st.switch_page("pages/notifications.py")

    st.markdown("---")

    st.write("👤 **Admin**")

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/login.py")


# -----------------------------
# PAGE STYLE
# -----------------------------

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

</style>
""", unsafe_allow_html=True)


# -----------------------------
# TITLE
# -----------------------------

st.title("👑 Admin Dashboard")

st.write(
    "Manage artworks, purchase requests and availability requests."
)

st.markdown("---")


# -----------------------------
# DASHBOARD METRICS
# -----------------------------

cursor.execute("SELECT COUNT(*) FROM artworks")
total_artworks = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM artworks WHERE availability = 'Available'"
)
available_artworks = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM artworks WHERE availability = 'Sold'"
)
sold_artworks = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM purchase_requests WHERE status = 'Pending'"
)
pending_purchases = cursor.fetchone()[0]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎨 Total Artworks", total_artworks)

with col2:
    st.metric("🟢 Available", available_artworks)

with col3:
    st.metric("🔴 Sold", sold_artworks)

with col4:
    st.metric("🛒 Pending Requests", pending_purchases)


st.markdown("---")


# -----------------------------
# TABS
# -----------------------------

tab1, tab2, tab3 = st.tabs([
    "🎨 Artworks",
    "🛒 Purchase Requests",
    "🔔 Availability Requests"
])


# ============================================================
# ARTWORKS
# ============================================================

with tab1:

    st.subheader("🎨 Manage Artworks")

    cursor.execute("""
        SELECT id, title, artist, price, availability
        FROM artworks
        ORDER BY id
    """)

    artworks = cursor.fetchall()

    for artwork in artworks:

        artwork_id = artwork[0]
        title = artwork[1]
        artist = artwork[2]
        price = artwork[3]
        availability = artwork[4]

        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.write(f"**{title}**")
            st.caption(artist)

        with col2:
            st.write(f"₹{price:,.0f}")

        with col3:

            if availability == "Available":
                st.success("🟢 Available")
            else:
                st.error("🔴 Sold")

        with col4:

            if availability == "Available":

                if st.button(
                    "Mark Sold",
                    key=f"sold_{artwork_id}"
                ):

                    cursor.execute(
                        """
                        UPDATE artworks
                        SET availability = 'Sold'
                        WHERE id = ?
                        """,
                        (artwork_id,)
                    )

                    connection.commit()

                    st.success("Artwork marked as sold.")
                    st.rerun()

            else:

                if st.button(
                    "Mark Available",
                    key=f"available_{artwork_id}"
                ):

                    cursor.execute(
                        """
                        UPDATE artworks
                        SET availability = 'Available'
                        WHERE id = ?
                        """,
                        (artwork_id,)
                    )

                    # Find users waiting for this artwork
                    cursor.execute(
                        """
                        SELECT user_email
                        FROM availability_requests
                        WHERE artwork_id = ?
                        AND status = 'Waiting'
                        """,
                        (artwork_id,)
                    )

                    waiting_users = cursor.fetchall()

                    current_time = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    for user in waiting_users:

                        user_email = user[0]

                        cursor.execute(
                            """
                            INSERT INTO notifications
                            (user_email, message, created_at, is_read)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                user_email,
                                f"Good news! '{title}' is now available.",
                                current_time,
                                0
                            )
                        )

                    # Mark requests as notified
                    cursor.execute(
                        """
                        UPDATE availability_requests
                        SET status = 'Notified'
                        WHERE artwork_id = ?
                        AND status = 'Waiting'
                        """,
                        (artwork_id,)
                    )

                    connection.commit()

                    st.success(
                        "Artwork is available. Waiting users have been notified."
                    )

                    st.rerun()

        st.markdown("---")


# ============================================================
# PURCHASE REQUESTS
# ============================================================

with tab2:

    st.subheader("🛒 Purchase Requests")

    cursor.execute("""
        SELECT
            purchase_requests.id,
            purchase_requests.user_email,
            artworks.title,
            artworks.price,
            purchase_requests.request_date,
            purchase_requests.status
        FROM purchase_requests
        JOIN artworks
        ON purchase_requests.artwork_id = artworks.id
        ORDER BY purchase_requests.id DESC
    """)

    purchase_requests = cursor.fetchall()

    if not purchase_requests:

        st.info("No purchase requests yet.")

    else:

        for request in purchase_requests:

            request_id = request[0]
            user_email = request[1]
            title = request[2]
            price = request[3]
            request_date = request[4]
            status = request[5]

            st.markdown(f"### 🎨 {title}")

            st.write(f"**User:** {user_email}")
            st.write(f"**Price:** ₹{price:,.0f}")
            st.write(f"**Date:** {request_date}")
            st.write(f"**Status:** {status}")

            if status == "Pending":

                if st.button(
                    "✅ Approve Request",
                    key=f"approve_{request_id}"
                ):

                    cursor.execute(
                        """
                        UPDATE purchase_requests
                        SET status = 'Approved'
                        WHERE id = ?
                        """,
                        (request_id,)
                    )

                    cursor.execute(
                        """
                        INSERT INTO notifications
                        (user_email, message, created_at, is_read)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            user_email,
                            f"Your purchase request for '{title}' has been approved.",
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            0
                        )
                    )

                    connection.commit()

                    st.success("Purchase request approved.")
                    st.rerun()

            st.markdown("---")


# ============================================================
# AVAILABILITY REQUESTS
# ============================================================

with tab3:

    st.subheader("🔔 Availability Requests")

    cursor.execute("""
        SELECT
            availability_requests.id,
            availability_requests.user_email,
            artworks.title,
            availability_requests.request_date,
            availability_requests.status
        FROM availability_requests
        JOIN artworks
        ON availability_requests.artwork_id = artworks.id
        ORDER BY availability_requests.id DESC
    """)

    availability_requests = cursor.fetchall()

    if not availability_requests:

        st.info("No availability requests yet.")

    else:

        for request in availability_requests:

            request_id = request[0]
            user_email = request[1]
            title = request[2]
            request_date = request[3]
            status = request[4]

            st.markdown(f"### 🔔 {title}")

            st.write(f"**User:** {user_email}")
            st.write(f"**Date:** {request_date}")
            st.write(f"**Status:** {status}")

            st.markdown("---")


# -----------------------------
# CLOSE DATABASE
# -----------------------------

connection.close()
