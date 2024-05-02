function setupLaunch() {
const buttons = document.querySelectorAll('#levelModal .modal-body button');
    let selectedLevel = '';

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            if (selectedLevel !== this.id) {
                if (selectedLevel) {
                    document.getElementById(selectedLevel).disabled = false;
                }
                selectedLevel = this.id;
                this.disabled = true;
            }
        });
    });
    
    document.querySelector('#ia-game').addEventListener('click', function () {
        launchGame('/ia/', '/ia/');
    })
    
    document.querySelector('#solo-game').addEventListener('click', function () {
        launchGame('/game/', '/game/');
    })


function launchGame(url, redirectUrl) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('#data-csrf').getAttribute('data-csrf'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            level: 0
        })
    }).then(response => {
        if (response.ok) {
            console.log('Match launched successfully!');
            loadView(redirectUrl);
        } else {
            console.error('Failed to launch match!');
        }
    }).catch(error => {
        console.error('Error launching match:', error);
    });
}
}