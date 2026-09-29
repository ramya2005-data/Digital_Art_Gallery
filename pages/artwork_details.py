import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Artwork Details",
    page_icon="🎨",
    layout="wide"
)

# ---------------- DATABASE ----------------

connection = sqlite3.connect("gallery.db")

artworks = connection.execute(
    "SELECT * FROM artworks"
).fetchall()

connection.close()

# ---------------- SELECTED ARTWORK ----------------

selected_id = st.session_state.get("selected_artwork")

artwork = None

for item in artworks:
    if item[0] == selected_id:
        artwork = item
        break

# ---------------- ARTWORK DETAILS ----------------

if artwork:

    title = artwork[1]
    artist = artwork[2]
    year = artwork[3]
    style = artwork[4]
    medium = artwork[5]
    description = artwork[6]
    price = artwork[7]
    availability = artwork[8]
    image = artwork[9]

    st.title(f"🎨 {title}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    # ---------------- IMAGE ----------------

    with col1:

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

    # ---------------- INFORMATION ----------------

    with col2:

        st.header(title)

        st.write(f"**Artist:** {artist}")

        st.write(f"**Year:** {year}")

        st.write(f"**Style:** {style}")

        st.write(f"**Medium:** {medium}")

        st.subheader(
            f"₹{price:,.0f}"
        )

        # ---------------- AVAILABLE ----------------

        if availability == "Available":

            st.success(
                "🟢 This artwork is available."
            )

            st.markdown("---")

            if st.button(
                "🛒 Purchase Artwork",
                use_container_width=True
            ):

                st.session_state[
                    "show_purchase_form"
                ] = True

        # ---------------- SOLD ----------------

        else:

            st.error(
                "🔴 This artwork is currently sold."
            )

            st.markdown("---")

            if st.button(
                "🔔 Request Availability",
                use_container_width=True
            ):

                st.session_state[
                    "show_availability_form"
                ] = True

    # ---------------- PURCHASE FORM ----------------

    if st.session_state.get(
        "show_purchase_form",
        False
    ):

        st.markdown("---")

        st.header("🛒 Purchase Request")

        user_email = st.session_state.get(
            "user_email",
            ""
        )

        st.write(
            f"**Artwork:** {title}"
        )

        st.write(
            f"**Price:** ₹{price:,.0f}"
        )

        st.write(
            "Submit a request to purchase this artwork. "
            "The gallery will contact you regarding the purchase."
        )

        if st.button(
            "Submit Purchase Request",
            use_container_width=True
        ):

            if not user_email:

                st.error(
                    "Please login before submitting a request."
                )

            else:

                connection = sqlite3.connect(
                    "gallery.db"
                )

                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO purchase_requests
                    (
                        user_email,
                        artwork_id,
                        request_date,
                        status
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_email,
                        artwork[0],
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Pending"
                    )
                )

                cursor.execute(
                    """
                    INSERT INTO notifications
                    (
                        user_email,
                        message,
                        created_at,
                        is_read
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_email,
                        f"Your purchase request for '{title}' has been submitted successfully.",
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        0
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "✅ Purchase request submitted successfully!"
                )

                st.info(
                    "The gallery will review your request and contact you."
                )

    # ---------------- AVAILABILITY FORM ----------------

    if st.session_state.get(
        "show_availability_form",
        False
    ):

        st.markdown("---")

        st.header("🔔 Availability Request")

        user_email = st.session_state.get(
            "user_email",
            ""
        )

        st.write(
            f"**Artwork:** {title}"
        )

        st.write(
            "This artwork is currently sold. "
            "Submit your request and we will notify you "
            "when it becomes available again."
        )

        if st.button(
            "Submit Availability Request",
            use_container_width=True
        ):

            if not user_email:

                st.error(
                    "Please login before submitting a request."
                )

            else:

                connection = sqlite3.connect(
                    "gallery.db"
                )

                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO availability_requests
                    (
                        user_email,
                        artwork_id,
                        request_date,
                        status
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_email,
                        artwork[0],
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Waiting"
                    )
                )

                cursor.execute(
                    """
                    INSERT INTO notifications
                    (
                        user_email,
                        message,
                        created_at,
                        is_read
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_email,
                        f"You will be notified when '{title}' becomes available.",
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        0
                    )
                )

                connection.commit()
                connection.close()

                st.success(
                    "🔔 Availability request submitted!"
                )

                st.info(
                    "We will notify you when this artwork becomes available."
                )

    # ---------------- ABOUT ARTWORK ----------------

    st.markdown("---")

    st.header("📖 About the Artwork")

    st.write(description)

    # ---------------- ABOUT ARTIST ----------------

    st.header("👩‍🎨 About the Artist")

    artist_information = {

        "Leonardo da Vinci":
            "Leonardo da Vinci was an Italian Renaissance artist, inventor and thinker known for works such as the Mona Lisa and The Last Supper.",

        "Vincent van Gogh":
            "Vincent van Gogh was a Dutch post-impressionist painter known for his expressive colours and emotional artistic style.",

        "Claude Monet":
            "Claude Monet was a French Impressionist painter famous for his landscapes and studies of light and colour.",

        "Edvard Munch":
            "Edvard Munch was a Norwegian artist known for expressive works exploring emotion and human experience.",

        "Salvador Dali":
            "Salvador Dalí was a Spanish Surrealist artist known for imaginative and dream-like paintings.",

        "Grant Wood":
            "Grant Wood was an American painter associated with the Regionalist art movement.",

        "Sandro Botticelli":
            "Sandro Botticelli was an Italian Renaissance painter famous for mythological and religious artworks.",

        "Gustav Klimt":
            "Gustav Klimt was an Austrian Symbolist painter known for decorative compositions and gold leaf.",

        "Rembrandt":
            "Rembrandt was a Dutch Baroque painter famous for portraits, dramatic lighting and historical scenes.",

        "Michelangelo":
            "Michelangelo was an Italian Renaissance artist celebrated for painting, sculpture and architecture.",

        "Pablo Picasso":
            "Pablo Picasso was a Spanish artist who played a major role in the development of Cubism.",

        "Johannes Vermeer":
            "Johannes Vermeer was a Dutch Golden Age painter known for intimate interior scenes and careful use of light."
    }

    st.write(
        artist_information.get(
            artist,
            f"{artist} is an important artist associated with the {style} movement."
        )
    )

else:

    st.warning(
        "Please select an artwork from the Gallery."
    )
