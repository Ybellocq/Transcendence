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
            else if (url == '/friends/') {
                setupAddFriends();
                setupFriends();
            }
            else if (url == '/tournament_match/') {
                setupTournament();
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

    // Hide navbar on index page and register page
    const navbar = document.querySelector('.navbar');
    if (location.pathname == '/' || location.pathname == '/register/' || location.pathname == '/logout/') {
        navbar.style.display = 'none';
    } else {
        navbar.style.display = 'block';
    }

    // Highlight active link in navbar
    const navbarLinks = document.querySelectorAll('.nav-link');
    navbarLinks.forEach(link => {
        if (link.getAttribute('href') === location.pathname) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Manage the profile page with the chart
    if (location.pathname == '/profile/') {
        console.log('profile');
        var colors = ['#007bff','#333333'];
        var chartsOptions = {
            cutoutPercentage: 85, 
            legend: {position:'bottom', padding:5, labels: {pointStyle:'circle', usePointStyle:true}}
        };
        var chDonutData = {
            labels: ['Victoires', 'Défaites'],
            datasets: [
                {
                    backgroundColor: colors.slice(0, 1),
                    borderWidth: 0,
                    data: [parseInt(document.getElementById('victories').value), parseInt(document.getElementById('defeats').value)]
                }
            ]
        };
        var chDonut = document.getElementById("myChart");
        if (chDonut) {
            new Chart(chDonut, {
                type: 'pie',
                data: chDonutData,
                options: chartsOptions
            });
        }
    }
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
    else if (url == '/friends/') {
        setupAddFriends();
        setupFriends();
    }
    else if (url == '/tournament_match/') {
        setupTournament();
    }
	window.addEventListener('popstate', function(event) {
		let url = location.pathname;
		loadView(url, false);
	});
});