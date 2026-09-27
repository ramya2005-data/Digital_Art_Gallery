import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠️",
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

</style>
""", unsafe_allow_html=True)


# ---------------- ADMIN CHECK ----------------

if st.session_state.get("user_email") != "admin@gmail.com":

    st.error("Admin access required.")

    if st.button("Go to Login"):
        st.switch_page("pages/login.py")

    st.stop()


# ---------------- TITLE ----------------

st.title("🛠️ Admin Dashboard")

st.write(
    "Manage artworks and customer requests."
)

st.markdown("---")


# ---------------- DATABASE ----------------

connection = sqlite3.connect("gallery.db")

cursor = connection.cursor()

# Get artwork statistics

total_artworks = cursor.execute(
    "SELECT COUNT(*) FROM artworks"
).fetchone()[0]

available_artworks = cursor.execute(
    "SELECT COUNT(*) FROM artworks WHERE availability = 'Available'"
).fetchone()[0]

sold_artworks = cursor.execute(
    "SELECT COUNT(*) FROM artworks WHERE availability = 'Sold'"
).fetchone()[0]

purchase_count = cursor.execute(
    "SELECT COUNT(*) FROM purchase_requests"
).fetchone()[0]

availability_count = cursor.execute(
    "SELECT COUNT(*) FROM availability_requests"
).fetchone()[0]

connection.close()


# ---------------- STATISTICS ----------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🎨 Artworks",
        total_artworks
    )

with col2:
    st.metric(
        "🟢 Available",
        available_artworks
    )

with col3:
    st.metric(
        "🔴 Sold",
        sold_artworks
    )

with col4:
    st.metric(
        "🛒 Purchases",
        purchase_count
    )

with col5:
    st.metric(
        "🔔 Availability",
        availability_count
    )


st.markdown("---")


# ---------------- TABS ----------------

tab1, tab2, tab3 = st.tabs(
    [
        "🎨 Artworks",
        "🛒 Purchase Requests",
        "🔔 Availability Requests"
    ]
)


# ==================================================
# TAB 1 — ARTWORKS
# ==================================================

with tab1:

    st.header("🎨 Manage Artworks")

    connection = sqlite3.connect(
        "gallery.db"
    )

    artworks = connection.execute(
        """
        SELECT id, title, artist, price, availability
        FROM artworks
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    for artwork in artworks:

        artwork_id = artwork[0]
        title = artwork[1]
        artist = artwork[2]
        price = artwork[3]
        availability = artwork[4]

        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(f"**{title}**")
            st.caption(artist)

        with col2:
            st.write(
                f"₹{price:,.0f}"
            )

        with col3:

            if availability == "Available":

                st.success("🟢 Available")

            else:

                st.error("🔴 Sold")

        with col4:

            if availability == "Available":

                if st.button(
                    "Mark as Sold",
                    key=f"sold_{artwork_id}"
                ):

                    connection = sqlite3.connect(
                        "gallery.db"
                    )

                    connection.execute(
                        """
                        UPDATE artworks
                        SET availability = 'Sold'
                        WHERE id = ?
                        """,
                        (artwork_id,)
                    )

                    connection.commit()
                    connection.close()

                    st.rerun()

            else:

                if st.button(
                    "Make Available",
                    key=f"available_{artwork_id}"
                ):

                    connection = sqlite3.connect(
                        "gallery.db"
                    )

                    connection.execute(
                        """
                        UPDATE artworks
                        SET availability = 'Available'
                        WHERE id = ?
                        """,
                        (artwork_id,)
                    )

                    connection.commit()

                    # Find users waiting for this artwork

                    waiting_users = connection.execute(
                        """
                        SELECT user_email
                        FROM availability_requests
                        WHERE artwork_id = ?
                        AND status = 'Waiting'
                        """,
                        (artwork_id,)
                    ).fetchall()

                    # Create notifications

                    for user in waiting_users:

                        connection.execute(
                            """
                            INSERT INTO notifications
                            (
                                user_email,
                                message,
                                created_at,
                                is_read
                            )
                            VALUES (?, ?, datetime('now'), 0)
                            """,
                            (
                                user[0],
                                f"Good news! '{title}' is now available for purchase."
                            )
                        )

                    # Update availability requests

                    connection.execute(
                        """
                        UPDATE availability_requests
                        SET status = 'Notified'
                        WHERE artwork_id = ?
                        AND status = 'Waiting'
                        """,
                        (artwork_id,)
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        f"{title} is now available!"
                    )

                    st.rerun()


# ==================================================
# TAB 2 — PURCHASE REQUESTS
# ==================================================

with tab2:

    st.header("🛒 Purchase Requests")

    connection = sqlite3.connect(
        "gallery.db"
    )

    purchase_requests = connection.execute(
        """
        SELECT
            purchase_requests.id,
            purchase_requests.user_email,
            artworks.title,
            purchase_requests.request_date,
            purchase_requests.status
        FROM purchase_requests
        JOIN artworks
        ON purchase_requests.artwork_id = artworks.id
        ORDER BY purchase_requests.id DESC
        """
    ).fetchall()

    connection.close()

    if not purchase_requests:

        st.info(
            "No purchase requests yet."
        )

    else:

        for request in purchase_requests:

            request_id = request[0]
            user_email = request[1]
            artwork_title = request[2]
            request_date = request[3]
            status = request[4]

            st.markdown("---")

            st.write(
                f"**🎨 Artwork:** {artwork_title}"
            )

            st.write(
                f"**👤 Customer:** {user_email}"
            )

            st.write(
                f"**📅 Date:** {request_date}"
            )

            st.write(
                f"**Status:** {status}"
            )

            if status == "Pending":

                if st.button(
                    "✅ Approve Request",
                    key=f"approve_{request_id}"
                ):

                    connection = sqlite3.connect(
                        "gallery.db"
                    )

                    connection.execute(
                        """
                        UPDATE purchase_requests
                        SET status = 'Approved'
                        WHERE id = ?
                        """,
                        (request_id,)
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "Purchase request approved."
                    )

                    st.rerun()


# ==================================================
# TAB 3 — AVAILABILITY REQUESTS
# ==================================================

with tab3:

    st.header("🔔 Availability Requests")

    connection = sqlite3.connect(
        "gallery.db"
    )

    availability_requests = connection.execute(
        """
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
        """
    ).fetchall()

    connection.close()

    if not availability_requests:

        st.info(
            "No availability requests yet."
        )

    else:

        for request in availability_requests:

            request_id = request[0]
            user_email = request[1]
            artwork_title = request[2]
            request_date = request[3]
            status = request[4]

            st.markdown("---")

            st.write(
                f"**🎨 Artwork:** {artwork_title}"
            )

            st.write(
                f"**👤 Customer:** {user_email}"
            )

            st.write(
                f"**📅 Date:** {request_date}"
            )

            if status == "Waiting":

                st.warning(
                    "⏳ Waiting for availability"
                )

            else:

                st.success(
                    "🔔 User notified"
                )