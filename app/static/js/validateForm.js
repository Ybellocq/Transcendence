function validateForm() {
    var username = document.forms["loginForm"]["usernames"].value;
    var password = document.forms["loginForm"]["password"].value;

    if (username == "" || password == "") {
        alert("Veuillez remplir tous les champs.");
        return false;
    }
}