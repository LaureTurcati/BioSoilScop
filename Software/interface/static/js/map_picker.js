/******************************************************************* map picker *******************************************************************/
document.addEventListener('DOMContentLoaded', function() {
    var mapElement = document.getElementById('map');
    
    // Verifie si l'element 'map' existe
    if (mapElement) {
        var map = L.map('map').setView([48.8566, 2.3522], 13); // Coordonnées de Paris

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        var marker;
        var myIcon = L.icon({
            iconUrl: 'static/img/position.png',
            iconSize: [48, 48], 
            iconAnchor: [24, 48],  
        });

        // Gestion du clic sur la carte
        map.on('click', function(e) {
            if (marker) {
                map.removeLayer(marker);
            }

            marker = L.marker(e.latlng, {icon: myIcon}).addTo(map);

            var lat = e.latlng.lat;
            var lng = e.latlng.lng;

            var format = document.getElementById('formatSelect').value;

            // Remplir les champs d'entree selon le format selectionne
            if (format === 'dd') {
                document.getElementById('latitude').value = lat.toFixed(5);
                document.getElementById('longitude').value = lng.toFixed(5);
            } else if (format === 'dms') {
                var dms = convertToDMS(lat, lng);
                document.getElementById('latDegrees').value = dms.latDegrees;
                document.getElementById('latMinutes').value = dms.latMinutes;
                document.getElementById('latSeconds').value = dms.latSeconds;
                document.querySelector(`input[name="latDirection"][value="${dms.latDirection}"]`).checked = true;

                document.getElementById('lngDegrees').value = dms.lngDegrees;
                document.getElementById('lngMinutes').value = dms.lngMinutes;
                document.getElementById('lngSeconds').value = dms.lngSeconds;
                document.querySelector(`input[name="lngDirection"][value="${dms.lngDirection}"]`).checked = true;
            } else if (format === 'dmm') {
                var dmm = convertToDMM(lat, lng);
                document.getElementById('latDegrees').value = dmm.latDegrees;
                document.getElementById('latMinutesDecimal').value = dmm.latMinutesDecimal;
                document.querySelector(`input[name="latDirection"][value="${dmm.latDirection}"]`).checked = true;

                document.getElementById('lngDegrees').value = dmm.lngDegrees;
                document.getElementById('lngMinutesDecimal').value = dmm.lngMinutesDecimal;
                document.querySelector(`input[name="lngDirection"][value="${dmm.lngDirection}"]`).checked = true;
            }
        });

        document.getElementById('setMarker').addEventListener('click', function() {
            var format = document.getElementById('formatSelect').value;
            var lat, lng;

            if (format === 'dd') {
                // Recupere les valeurs DD
                lat = parseFloat(document.getElementById('latitude').value);
                lng = parseFloat(document.getElementById('longitude').value);
            } else if (format === 'dms') {
                // Recupere et convertis les valeurs DMS
                var latDegrees = parseInt(document.getElementById('latDegrees').value);
                var latMinutes = parseInt(document.getElementById('latMinutes').value);
                var latSeconds = parseFloat(document.getElementById('latSeconds').value);
                var latDirection = document.querySelector('input[name="latDirection"]:checked').value;

                var lngDegrees = parseInt(document.getElementById('lngDegrees').value);
                var lngMinutes = parseInt(document.getElementById('lngMinutes').value);
                var lngSeconds = parseFloat(document.getElementById('lngSeconds').value);
                var lngDirection = document.querySelector('input[name="lngDirection"]:checked').value;

                lat = convertToDD(latDegrees, latMinutes, latSeconds, latDirection);
                lng = convertToDD(lngDegrees, lngMinutes, lngSeconds, lngDirection);
            } else if (format === 'dmm') {
                // Recupere et convertis les valeurs DMM
                var latDegrees = parseInt(document.getElementById('latDegrees').value);
                var latMinutesDecimal = parseFloat(document.getElementById('latMinutesDecimal').value);
                var latDirection = document.querySelector('input[name="latDirection"]:checked').value;

                var lngDegrees = parseInt(document.getElementById('lngDegrees').value);
                var lngMinutesDecimal = parseFloat(document.getElementById('lngMinutesDecimal').value);
                var lngDirection = document.querySelector('input[name="lngDirection"]:checked').value;

                lat = convertToDD(latDegrees, latMinutesDecimal, 0, latDirection);
                lng = convertToDD(lngDegrees, lngMinutesDecimal, 0, lngDirection);
            }

            // Verification des coordonnees avant de placer le marqueur
            if (!isNaN(lat) && !isNaN(lng)) {
                // Si un marqueur existe dejà, le retirer
                if (marker) {
                    map.removeLayer(marker);
                }

                // Ajoute un nouveau marqueur à l'emplacement defini
                marker = L.marker([lat, lng], {icon: myIcon}).addTo(map);

                // Centre la carte sur le nouveau marqueur
                map.setView([lat, lng], 13);
            } else {
                alert("Veuillez entrer des coordonnées valides.");
            }
        });
    }

    // Fonction qui met a jour les champs de saisie en fonction du format
    function updateCoordinateInputs() {
        var format = document.getElementById('formatSelect').value;
        var coordinateInputs = document.getElementById('coordinateInputs');
        coordinateInputs.innerHTML = '';

        var lat, lng;

        // Si un marqueur est present, recuperer ses coordonnées
        if (marker) {
            var latlng = marker.getLatLng();
            lat = latlng.lat;
            lng = latlng.lng;
        } else {
            // Si pas de marqueur, essayer de recuperer les coordonnees des inputs actuels
            var currentLatInput = document.getElementById('latitude');
            var currentLngInput = document.getElementById('longitude');

            if (currentLatInput && currentLngInput) {
                lat = parseFloat(currentLatInput.value);
                lng = parseFloat(currentLngInput.value);
            }
        }

        // Affichage des inputs en fonction du format selectionne
        if (format === 'dd') {
            // Format Degres Decimaux (DD)
            coordinateInputs.innerHTML = `
                <label for="latitude">Latitude </label>
                <input type="text" id="latitude" name="latitude" placeholder="Latitude (DD)" />
                <label for="longitude">Longitude </label>
                <input type="text" id="longitude" name="longitude" placeholder="Longitude (DD)" />
            `;
            if (!isNaN(lat) && !isNaN(lng)) {
                document.getElementById('latitude').value = lat.toFixed(5);
                document.getElementById('longitude').value = lng.toFixed(5);
            }
        } else if (format === 'dms') {
            // Format Degres, Minutes, Secondes (DMS)
            coordinateInputs.innerHTML = `
                <label>Latitude </label>
                <div class='row'>
                    <label><input type="radio" name="latDirection" value="N" checked> N</label>
                    <label><input type="radio" name="latDirection" value="S"> S</label>
                    <input type="text" id="latDegrees" name="latDegrees" placeholder="°" style="width: 50px;" />
                    <input type="text" id="latMinutes" name="latMinutes" placeholder="'" style="width: 50px;" />
                    <input type="text" id="latSeconds" name="latSeconds" placeholder='"' style="width: 70px;" />
                </div>
                <label>Longitude </label>
                <div class='row'>
                    <label><input type="radio" name="lngDirection" value="E" checked> E</label>
                    <label><input type="radio" name="lngDirection" value="W"> W</label>
                    <input type="text" id="lngDegrees" name="lngDegrees" placeholder="°" style="width: 50px;" />
                    <input type="text" id="lngMinutes" name="lngMinutes" placeholder="'" style="width: 50px;" />
                    <input type="text" id="lngSeconds" name="lngSeconds" placeholder='"' style="width: 70px;" />
                </div>
            `;
            if (!isNaN(lat) && !isNaN(lng)) {
                var dms = convertToDMS(lat, lng);
                document.getElementById('latDegrees').value = dms.latDegrees;
                document.getElementById('latMinutes').value = dms.latMinutes;
                document.getElementById('latSeconds').value = dms.latSeconds;
                document.querySelector(`input[name="latDirection"][value="${dms.latDirection}"]`).checked = true;

                document.getElementById('lngDegrees').value = dms.lngDegrees;
                document.getElementById('lngMinutes').value = dms.lngMinutes;
                document.getElementById('lngSeconds').value = dms.lngSeconds;
                document.querySelector(`input[name="lngDirection"][value="${dms.lngDirection}"]`).checked = true;
            }
        } else if (format === 'dmm') {
            // Format Degres, Minutes Decimales (DMM)
            coordinateInputs.innerHTML = `
                <label>Latitude </label>
                <div class='row'>
                    <label><input type="radio" name="latDirection" value="N" checked> N</label>
                    <label><input type="radio" name="latDirection" value="S"> S</label>
                    <input type="text" id="latDegrees" name="latDegrees" placeholder="°" style="width: 50px;" />
                    <input type="text" id="latMinutesDecimal" name="latMinutesDecimal" placeholder="'" style="width: 100px;" />
                </div>
                <label>Longitude </label>
                <div class='row'>
                    <label><input type="radio" name="lngDirection" value="E" checked> E</label>
                    <label><input type="radio" name="lngDirection" value="W"> W</label>
                    <input type="text" id="lngDegrees" name="lngDegrees" placeholder="°" style="width: 50px;" />
                    <input type="text" id="lngMinutesDecimal" name="lngMinutesDecimal" placeholder="'" style="width: 100px;" />
                </div>
            `;
            if (!isNaN(lat) && !isNaN(lng)) {
                var dmm = convertToDMM(lat, lng);
                document.getElementById('latDegrees').value = dmm.latDegrees;
                document.getElementById('latMinutesDecimal').value = dmm.latMinutesDecimal;
                document.querySelector(`input[name="latDirection"][value="${dmm.latDirection}"]`).checked = true;

                document.getElementById('lngDegrees').value = dmm.lngDegrees;
                document.getElementById('lngMinutesDecimal').value = dmm.lngMinutesDecimal;
                document.querySelector(`input[name="lngDirection"][value="${dmm.lngDirection}"]`).checked = true;
            }
        }
    }

    // Fonction pour convertir les coordonnees DMS ou DMM en DD
    function convertToDD(degrees, minutes, seconds, direction) {
        var dd = Math.abs(degrees) + minutes / 60 + (seconds ? seconds / 3600 : 0);
        if (direction === "S" || direction === "W") {
            dd = -dd;
        }
        return dd;
    }

    // Fonction pour convertir DD en DMS
    function convertToDMS(lat, lng) {
        var latDegrees = Math.floor(Math.abs(lat));
        var latMinutes = Math.floor((Math.abs(lat) - latDegrees) * 60);
        var latSeconds = ((Math.abs(lat) - latDegrees - (latMinutes / 60)) * 3600).toFixed(2);
        var latDirection = lat >= 0 ? "N" : "S";

        var lngDegrees = Math.floor(Math.abs(lng));
        var lngMinutes = Math.floor((Math.abs(lng) - lngDegrees) * 60);
        var lngSeconds = ((Math.abs(lng) - lngDegrees - (lngMinutes / 60)) * 3600).toFixed(2);
        var lngDirection = lng >= 0 ? "E" : "W";

        return {
            latDegrees: latDegrees,
            latMinutes: latMinutes,
            latSeconds: latSeconds,
            latDirection: latDirection,
            lngDegrees: lngDegrees,
            lngMinutes: lngMinutes,
            lngSeconds: lngSeconds,
            lngDirection: lngDirection
        };
    }

    // Fonction pour convertir DD en DMM
    function convertToDMM(lat, lng) {
        var latDegrees = Math.floor(Math.abs(lat));
        var latMinutesDecimal = ((Math.abs(lat) - latDegrees) * 60).toFixed(5);
        var latDirection = lat >= 0 ? "N" : "S";

        var lngDegrees = Math.floor(Math.abs(lng));
        var lngMinutesDecimal = ((Math.abs(lng) - lngDegrees) * 60).toFixed(5);
        var lngDirection = lng >= 0 ? "E" : "W";

        return {
            latDegrees: latDegrees,
            latMinutesDecimal: latMinutesDecimal,
            latDirection: latDirection,
            lngDegrees: lngDegrees,
            lngMinutesDecimal: lngMinutesDecimal,
            lngDirection: lngDirection
        };
    }

    document.getElementById('formatSelect').addEventListener('change', updateCoordinateInputs);

    // Initialisation des champs pour le format par defaut
    updateCoordinateInputs();
});