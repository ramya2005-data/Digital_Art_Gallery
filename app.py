import streamlit as st
import database

st.set_page_config(
    page_title="Digital Art Gallery",
    page_icon="🎨",
    layout="wide"
)


if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
# -----------------------------
# BACKGROUND
# -----------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7F3EE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("🎨 Digital Gallery")

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

    if st.button("🖼️ Gallery", use_container_width=True):
        st.switch_page("pages/gallery.py")

    if st.button("🔔 Notifications", use_container_width=True):
        st.switch_page("pages/notifications.py")

    st.markdown("---")

    user_name = st.session_state.get("user_name", "Guest")

    st.write(f"👤 **{user_name}**")

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.clear()

        st.switch_page("pages/login.py")


# -----------------------------
# HOME
# -----------------------------

st.title("🎨 Digital Art Gallery")

st.markdown(
    "### DISCOVER • EXPLORE • APPRECIATE"
)

st.write(
    "Welcome to our digital art space, where creativity, "
    "culture and imagination come together. Explore "
    "remarkable artworks, discover their stories and "
    "learn about the artists behind them."
)

st.write("")

# -----------------------------
# EXPLORE GALLERY
# -----------------------------

col1, col2, col3 = st.columns(3)

with col2:

    if st.button(
        "🖼️ Explore Gallery",
        use_container_width=True
    ):

        st.switch_page("pages/gallery.py")


# -----------------------------
# EXPLORE OUR COLLECTION
# -----------------------------

st.markdown("---")

st.header("✨ Explore Our Collection")

st.write("")

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("🖼️ Discover Art")

    st.write(
        "Explore artworks from different periods, "
        "styles and artistic movements."
    )

with col2:

    st.subheader("👩‍🎨 Meet the Artists")

    st.write(
        "Learn about artists and discover the stories "
        "behind their artwork."
    )

with col3:

    st.subheader("💎 Find Your Art")

    st.write(
        "Check artwork prices and availability and "
        "submit a request for your favourite piece."
    )


# -----------------------------
# ABOUT PROJECT
# -----------------------------

st.markdown("---")

st.header("📚 About This Project")

st.write(
    "The Digital Art Gallery Management and Information "
    "System allows users to explore artworks, learn about "
    "artists, check prices and availability, submit "
    "purchase requests and receive notifications."
)


# -----------------------------
# PROJECT FEATURES
# -----------------------------

st.markdown("---")

st.header("⭐ Project Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🎨 15+ Artworks")

with col2:
    st.info("🛒 Purchase Requests")

with col3:
    st.info("🔔 Notifications")


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.caption(
    "Digital Art Gallery Management & Information System • "
    "B.Sc Data Science Mini Project"
)
