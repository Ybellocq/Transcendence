// Autor: Lorenzo & Lartaxx & Wasied
// Function that sends a POST request to add a friend to the user's friend list


const searchInput = document.getElementById("search");
const usersContainer = document.getElementById("users");

searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        fetch(searchUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                'search': searchInput.value
            })
        })
        .then(response => response.json())
        .then(response => {
            console.log(response);
            usersContainer.innerHTML = '';
            if (response.users.length === 0 || searchInput.value === '' ) {
                usersContainer.innerHTML = `
                    <div class="col-12 d-flex justify-content-center">
                        <p class="fw-bold fs text-white">Aucun utilisateur trouvé</p>
                    </div>
                `;
            } else {
                response.users.forEach((user) => {
                    let addButtonLabel = user.is_friend ? "Déjà amis" : "Ajouter";
                    let disabledAttribute = user.is_friend ? "disabled" : "";
                    if (user.is_self) {
                        addButtonLabel = "Vous";
                        disabledAttribute = "disabled";
                    }
                    usersContainer.innerHTML += `
                        <div class="col d-flex justify-content-center">
                            <div class="user-card p-3 bg-darkdark text-white rounded-5">
                                <img src="${user.profile_image}" class="rounded-circle" width="100" height="100">
                                <p class="fw-bold fs-5 text-center">${user.username}</p>
                                <div class="d-flex justify-content-center items-center">
                                    <button class="btn btn-primary" data-toggle="button" aria-pressed="false" id="add-button" data-user-id="${user.id}" onclick="addFriend('${user.id}')" ${disabledAttribute}>${addButtonLabel}</button>
                                </div>
                            </div>
                        </div>
                    `;
                });                                
            }
        });
    }
});