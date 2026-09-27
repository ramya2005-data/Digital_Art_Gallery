import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Digital Art Gallery",
    page_icon="🎨",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background-color: #F7F3EE;
}

h1 {
    text-align: center;
    color: #2F2925;
}

h2, h3 {
    color: #4B4038;
}

p {
    color: #5F5751;
}

</style>
""", unsafe_allow_html=True)


st.title("🎨 Digital Art Gallery")

st.write(
    "Discover beautiful artworks, explore their stories "
    "and find your next masterpiece."
)

st.markdown("---")


option = st.radio(
    "Choose an option",
    ["Login", "Register"],
    horizontal=True
)


# ==================================================
# REGISTER
# ==================================================

if option == "Register":

    st.subheader("Create Your Account")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Create Account"):

        if name and email and password:

            connection = sqlite3.connect(
                "gallery.db"
            )

            cursor = connection.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO users
                    (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        password,
                        "user"
                    )
                )

                connection.commit()

                st.success(
                    "Account created successfully! "
                    "Please login."
                )

            except sqlite3.IntegrityError:

                st.error(
                    "This email is already registered."
                )

            connection.close()

        else:

            st.warning(
                "Please fill in all the fields."
            )


# ==================================================
# LOGIN
# ==================================================

else:

    st.subheader("Welcome Back 👋")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):

        connection = sqlite3.connect(
            "gallery.db"
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email, password, role
            FROM users
            WHERE email = ?
            AND password = ?
            """,
            (
                email,
                password
            )
        )

        user = cursor.fetchone()

        connection.close()

        if user:

            user_id = user[0]
            user_name = user[1]
            user_email = user[2]
            user_role = user[4]

            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
            st.session_state["user_name"] = user_name
            st.session_state["user_email"] = user_email
            st.session_state["user_role"] = user_role

            st.success(
                f"Welcome, {user_name}! 🎨"
            )

            # Admin goes to admin dashboard

            if user_role == "admin":

                st.switch_page(
                    "pages/admin_dashboard.py"
                )

            # Normal user goes to gallery

            else:

                st.switch_page(
                    "pages/gallery.py"
                )

        else:

            st.error(
                "Invalid email or password."
            )