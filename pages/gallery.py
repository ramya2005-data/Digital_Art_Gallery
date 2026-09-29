import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Digital Art Gallery",
    page_icon="🎨",
    layout="wide"
)

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.title("🎨 Digital Gallery")

    st.markdown("---")

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.switch_page("app.py")

    if st.button(
        "🖼️ Gallery",
        use_container_width=True
    ):
        st.switch_page("pages/gallery.py")

    if st.button(
        "🔔 Notifications",
        use_container_width=True
    ):
        st.switch_page("pages/notifications.py")

    st.markdown("---")

    user_name = st.session_state.get(
        "user_name",
        "Guest"
    )

    st.write(f"👤 **{user_name}**")

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "pages/login.py"
        )


# ==================================================
# PAGE STYLING
# ==================================================

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

p {
    color: #5F5751;
}

.art-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #FFFFFF;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# PAGE TITLE
# ==================================================

st.title("🎨 Digital Art Gallery")

st.write(
    "Explore beautiful artworks, discover their stories "
    "and admire the artists behind them."
)

st.markdown("---")


# ==================================================
# SEARCH
# ==================================================

search = st.text_input(
    "🔍 Search artwork or artist",
    placeholder="Search for an artwork or artist..."
)


# ==================================================
# DATABASE
# ==================================================

connection = sqlite3.connect(
    "gallery.db"
)

artworks = connection.execute(
    "SELECT * FROM artworks"
).fetchall()

connection.close()


# ==================================================
# FILTER OPTIONS
# ==================================================

styles = ["All"]

for artwork in artworks:

    style = artwork[4]

    if style and style not in styles:

        styles.append(style)


col1, col2 = st.columns(2)


with col1:

    style_filter = st.selectbox(
        "🎨 Art Style",
        styles
    )


with col2:

    availability_filter = st.selectbox(
        "Availability",
        [
            "All",
            "Available",
            "Sold"
        ]
    )


st.markdown("---")


# ==================================================
# COLLECTION TITLE
# ==================================================

st.subheader(
    "✨ Explore Our Collection"
)


# ==================================================
# FILTER ARTWORKS
# ==================================================

filtered_artworks = []

for artwork in artworks:

    title = artwork[1]

    artist = artwork[2]

    style = artwork[4]

    availability = artwork[8]


    # Search condition

    search_match = (
        search.strip() == ""
        or search.lower() in title.lower()
        or search.lower() in artist.lower()
    )


    # Style condition

    style_match = (
        style_filter == "All"
        or style == style_filter
    )


    # Availability condition

    availability_match = (
        availability_filter == "All"
        or availability == availability_filter
    )


    if (
        search_match
        and style_match
        and availability_match
    ):

        filtered_artworks.append(
            artwork
        )


# ==================================================
# DISPLAY ARTWORKS
# ==================================================

if filtered_artworks:

    for i in range(
        0,
        len(filtered_artworks),
        3
    ):

        columns = st.columns(3)


        for j, col in enumerate(columns):

            if i + j < len(filtered_artworks):

                artwork = filtered_artworks[
                    i + j
                ]


                # Artwork information

                artwork_id = artwork[0]

                title = artwork[1]

                artist = artwork[2]

                year = artwork[3]

                style = artwork[4]

                price = artwork[7]

                availability = artwork[8]

                image = artwork[9]


                with col:

                    st.markdown(
                        '<div class="art-card">',
                        unsafe_allow_html=True
                    )


                    # ---------------- IMAGE ----------------

                    if image:

                        try:

                            st.image(
                                "images/" + image,
                                use_container_width=True
                            )

                        except:

                            st.warning(
                                "Artwork image unavailable."
                            )


                    # ---------------- TITLE ----------------

                    st.subheader(
                        title
                    )


                    # ---------------- ARTIST ----------------

                    st.write(
                        f"**{artist}**"
                    )


                    # ---------------- STYLE + YEAR ----------------

                    st.write(
                        f"{style} • {year}"
                    )


                    # ---------------- PRICE ----------------

                    st.write(
                        f"₹{price:,.0f}"
                    )


                    # ---------------- AVAILABILITY ----------------

                    if availability == "Available":

                        st.success(
                            "🟢 Available"
                        )

                    else:

                        st.error(
                            "🔴 Sold"
                        )


                    # ---------------- VIEW BUTTON ----------------

                    if st.button(
                        "View Artwork",
                        key=f"view_{artwork_id}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "selected_artwork"
                        ] = artwork_id

                        st.switch_page(
                            "pages/artwork_details.py"
                        )


                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


# ==================================================
# NO RESULTS
# ==================================================

else:

    st.info(
        "No artworks found."
    )
