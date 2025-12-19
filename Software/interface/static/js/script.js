function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', showLoader);
});

function toggleMenu() {
    document.querySelector(".nav-menu").classList.toggle("active");
}

function addEventListenerIfExists(selector, event, callback) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        element.addEventListener(event, callback);
    });
}

addEventListenerIfExists('#apButton', 'click', function() {
    const messageDiv = document.getElementById('modeMessage');
    messageDiv.style.display = 'block';
    messageDiv.innerText = 'Le mode AP est en cours d’activation. Cela peut prendre quelques instants. Pensez à vous connecter au réseau CamTrap avant de rafraichir la page '; 
    messageDiv.style.color = 'red'; 

});


addEventListenerIfExists('#wifiButton', 'click', function() {
    const messageDiv = document.getElementById('modeMessage');
    messageDiv.style.display = 'block';
    messageDiv.innerText = 'Le mode Wi-Fi est en cours d’activation. Cela peut prendre quelques instants. Pensez à vous connecter au même réseau avant de rafraichir la page'; 
    messageDiv.style.color = 'red'; 
});

addEventListenerIfExists('#config_wifi', 'click', function() {
    const messageDiv = document.getElementById('modeMessage');
    messageDiv.style.display = 'block';
    messageDiv.innerText = 'Connexion au wifi en cours. Cela peut prendre quelques instants. Pensez à vous connecter au même réseau avant de rafraichir la page'; 
    messageDiv.style.color = 'red'; 

});

addEventListenerIfExists('#openDialogBtn', 'click', function() {
    const dialog = document.getElementById('confirmDateDialog');

    // mémoriser le bon formulaire correspondant
    const form = this.closest('form');
    dialog.currentForm = form;

    dialog.showModal();
});

addEventListenerIfExists('#closeDialogBtn', 'click', function() {
    const dialog = document.getElementById('confirmDateDialog');
    dialog.close();
});

addEventListenerIfExists('#confirmStartSession', 'click', function() {
    const dialog = document.getElementById('confirmDateDialog');
    const form = dialog.currentForm;
    dialog.close();
    form.submit()
});

addEventListenerIfExists('#redirectToDate', 'click', function() {
    const dialog = document.getElementById('confirmDateDialog');
    dialog.close();
    window.location.href = '/date';
});


addEventListenerIfExists('#filebrowserStart', 'click', function() {
    fetch('/start_filebrowser', {
        method: 'POST'
    })
    .then(response => {
        const messageDiv = document.getElementById('filebrowserMessage');
        
        if (response.ok) {
            messageDiv.style.display = 'block';
            messageDiv.innerText = 'Filebrowser a été activé.';
            messageDiv.style.color = 'green';
        } else {
            return response.json().then(data => {
                messageDiv.style.display = 'block';
                messageDiv.innerText = 'Erreur : ' + (data.error || 'Erreur lors du démarrage de filebrowser.');
                messageDiv.style.color = 'red';
            });
        }
    })
    .catch(error => {
        const messageDiv = document.getElementById('filebrowserMessage');
        messageDiv.style.display = 'block';
        messageDiv.innerText = 'Erreur de réseau : ' + error.message;
        messageDiv.style.color = 'red';
    });
});

addEventListenerIfExists('#filebrowserOpen', 'click', function() {
    fetch('/open_filebrowser')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Erreur lors de l'ouverture de filebrowser.");
            }
        })
        .then(data => {
            const messageDiv = document.getElementById('filebrowserMessage');
            const url = data.url; 
            window.open(url, '_blank');

            messageDiv.style.display = 'block';
            messageDiv.innerText = 'Filebrowser a été ouvert dans un autre onglet.';
            messageDiv.style.color = 'green';
        })
        .catch(error => {
            const messageDiv = document.getElementById('filebrowserMessage');
            messageDiv.style.display = 'block';
            messageDiv.innerText = 'Erreur de réseau : ' + error.message;
            messageDiv.style.color = 'red';
        });
});
/******************************************************************* form session *******************************************************************/

function toggleContainer(radio, container) {
    if (radio.checked) {
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
}

function addChangeListener(radioSelector, containerId) {
    const radio = document.getElementById(radioSelector);
    const container = document.getElementById(containerId);

    if (radio && container) {
        radio.addEventListener("change", function() {
            toggleContainer(radio, container);
        });
    }
}

function hideContainerForOtherRadios(groupSelector, exceptionId, containerId) {
    const radios = document.querySelectorAll(groupSelector);
    const container = document.getElementById(containerId);

    if (container) {
        radios.forEach(radio => {
            if (radio.id !== exceptionId) {
                radio.addEventListener("change", function() {
                    container.style.display = "none";
                });
            }
        });
    }
}

function syncRadiosAndCheckboxes(radioSelector, checkboxSelector) {
    const radios = document.querySelectorAll(radioSelector);
    const checkboxes = document.querySelectorAll(checkboxSelector);

    radios.forEach(radio => {
        radio.addEventListener("change", function() {
            if (radio.checked) {
                checkboxes.forEach(checkbox => checkbox.checked = false);
            }
        });
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            if (checkbox.checked) {
                radios.forEach(radio => radio.checked = false);
            }
        });
    });
}

addChangeListener('type_site_autre', 'autre_type_container');
addChangeListener('composition_site_autre', 'autre_composition_container');
addChangeListener('entretien_autre', 'autre_entretien_container');
addChangeListener('vegetation_autre', 'autre_vegetation_container');
addChangeListener('couverture_sol_autre', 'autre_couverture_container');

hideContainerForOtherRadios('input[name="type_site"]', 'type_site_autre', 'autre_type_container');
hideContainerForOtherRadios('input[name="composition_site"]', 'composition_site_autre', 'autre_composition_container');
hideContainerForOtherRadios('input[name="entretien"]', 'entretien_autre', 'autre_entretien_container');
hideContainerForOtherRadios('input[name="vegetation"]', 'vegetation_autre', 'autre_vegetation_container');
hideContainerForOtherRadios('input[name="couverture_sol"]', 'couverture_sol_autre', 'autre_couverture_container');

syncRadiosAndCheckboxes('input[name="phytosanitaire_unique"]', 'input[name="phytosanitaire_multiple"]');
syncRadiosAndCheckboxes('input[name="entretien_unique"]', 'input[name="entretien_multiple"]');

/******************************************************************* plage time *******************************************************************/
function handleChoice(){
    var choixPlage = document.getElementById('choix2');
    var plageDiv = document.getElementById('plage');
    var plageFields = plageDiv.querySelectorAll('input');
    if (choixPlage.checked) {
        plageDiv.style.display = 'block';
        plageFields.forEach(field => field.disabled = false);
    } else {
        plageDiv.style.display = 'none';
        plageFields.forEach(field => field.disabled = true);
    }
}

function createLigne(num){
    const newRow = document.createElement('div');
    newRow.classList.add('timeWrapper');
    newRow.innerHTML=`<input type="time" name="time_debut_${num}" id="time_debut_${num}"> <input type="time" name="time_fin_${num}" id="time_fin_${num}"><img src="static/img/plus_fonce.png" alt="Ajout d'une plage horaire" onclick="ajouterLigne(${num}+1)"/><img src="static/img/moins_fonce.png" alt="Suppression d'une plage horaire" onclick="supprimerLigne(event)"/>`;
    const hours = document.getElementById("hours");
    hours.appendChild(newRow);
}

function ajouterLigne(num){
    createLigne(num);

}

function supprimerLigne(event) {
    const row = event.target.closest(".timeWrapper");
    row.remove();
}

/************************************************************************ liste session ************************************************************************/
function deleteSession(){
    const deleteButtons = document.querySelectorAll(".delete_btn");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", function() {
            const filePath = button.getAttribute('data-file');
            if (confirm("Êtes-vous sûr de vouloir supprimer ce dossier ? Cette action entraînera la suppression définitive du dossier ainsi que de tous les fichiers et sous-dossiers qu'il contient.")) {
                fetch('/delete_file', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ file_path: filePath })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                        this.closest('tr').remove();
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => console.error('Erreur:', error));
            }
        });
    });
};

function checkStatus(){
    fetch("/any_active_session")
    .then(response => response.json())
    .then(data => {
        if (data.active) {
            document.querySelectorAll('form.start-form button').forEach(button => {
                const tooltip = document.createElement('div');
                tooltip.classList.add('tooltip');

                const tooltipText = document.createElement('span');
                tooltipText.classList.add('tooltip-text');
                tooltipText.textContent = "Impossible de démarrer une autre session. Une session est déjà en cours.";

                button.disabled = true;
                button.parentNode.insertBefore(tooltip, button);
                tooltip.appendChild(button);
                tooltip.appendChild(tooltipText);
            });
        }
    })
    .catch(error => console.error('Erreur:', error));
}

function showToast(message, type='info', duration=5000){
    const container = document.getElementById('toast-container');
    if(!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => container.removeChild(toast), 300);
    }, duration);
}

/************************************************************************ form config ************************************************************************/
function toggleManualFocus() {
    var manualFocus = document.getElementById('manual-focus');
    var autofocusMode = document.getElementById('autofocus-mode');
    
    if (autofocusMode && manualFocus) {
        if (autofocusMode.value === 'manual') {
            manualFocus.classList.add('active');
        } else {
            manualFocus.classList.remove('active');
        }
    }
}

/************************************************************************ set_video ************************************************************************/
function led(){
    var led = document.getElementById('led');
    var ledValue = document.getElementById('ledValue');
    if (led && ledValue) {
        led.addEventListener('input', function() {
            ledValue.innerHTML = led.value;
        });
    }
}

/************************************************************************ Listener  ************************************************************************/

document.addEventListener("DOMContentLoaded", function() {
    deleteSession();
    checkStatus();
    toggleManualFocus(); 
    led();
    addEventListenerIfExists('#autofocus-mode', 'change', toggleManualFocus);
});
