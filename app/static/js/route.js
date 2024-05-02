function extractViewContent(html) {
	const tempElement = document.createElement('div');
	tempElement.innerHTML = html;
	const viewContent = tempElement.querySelector('main');
    return viewContent.innerHTML;
}

function loadView(url, needHistory) {
    // Récupération du contenu des vues à partir du serveur Django
    fetch(url)
        .then(response => response.text())
        .then(html => {
            // Mise à jour de l'URL et de l'historique de navigation si nécessaire
            if (needHistory != false && location.pathname != url) {
                history.pushState(null, null, url);
            }
            // Mise à jour du contenu de la page avec le contenu de la vue récupéré
            document.querySelector('main').innerHTML = extractViewContent(html);

            if (url == '/ia/') {
                setupIA();
            }
            else if (url == '/game/') {
                setupSolo();
            }
            else if (url == '/gamepage/') {
                setupLaunch();
            }
            // Attachement des écouteurs d'événements spécifiques à la vue chargée
            attachEventListeners();
            // Optionnel : Mise en place des actions spécifiques en fonction de l'URL chargée
           //  setupActionsForURL(url);
        })
        .catch(error => {
            console.error('Erreur lors du chargement de la vue:', error);
        });
}

function attachEventListeners() {
    const navLinks = document.querySelectorAll('.redir');

    function attachClickEvent(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const url = link.getAttribute('href');
            loadView(url, true);
        });
    }

    navLinks.forEach(link => {
        if (!link.hasAttribute('data-click-event-attached')) {
            attachClickEvent(link);
            link.setAttribute('data-click-event-attached', true);
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
	attachEventListeners();

    const url = location.pathname;
    history.pushState(null, null, url);
    if (url == '/ia/') {
        setupIA();
    }
    else if (url == '/game/') {
        setupSolo();
    }
    else if (url == '/gamepage/') {
        setupLaunch();
    }
	window.addEventListener('popstate', function(event) {
		let url = location.pathname;
		loadView(url, false);
	});
});