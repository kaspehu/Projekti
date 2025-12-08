
const player = JSON.parse(localStorage.getItem("chosenCharacter"));

if (player) {
    document.getElementById("player-name").textContent = player.name;
    document.getElementById("player-icon").src = player.image;
}

const map = L.map('map', { tap: false }).setView([-14.235, -51.925], 5);

L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);

let allAirports = [];
let currentAirport = null;
let currentMarker = null;
let airportMarkers = [];
let visitedMarkers = new Set();

const DICE_BTN_ID = "rollDiceBtn";
const goldenBallPopup = document.getElementById("goldenBallPopup");
const collectBallBtn = document.getElementById("collectBallBtn");


function handleGoldenBallCollection() {
    if (!currentAirport || !currentAirport.hasGoldenBall) return;

    addGoldenBall();
    currentAirport.hasGoldenBall = false;
    addMessage(`The Golden Ball has been collected at ${currentAirport.name}!`);

    goldenBallPopup.classList.add("hide");

    document.getElementById(DICE_BTN_ID).disabled = false;
}

collectBallBtn.addEventListener('click', handleGoldenBallCollection);


// 10 randomia palloa lentokentille
function initializeGoldenBalls(airports) {
    const numAirports = airports.length;
    const numBalls = 10;

    airports.forEach(a => a.hasGoldenBall = false);

    const indices = Array.from({ length: numAirports }, (_, i) => i).sort(() => 0.5 - Math.random());

    for (let i = 0; i < numBalls; i++) {
        if (indices[i] !== undefined) {
            airports[indices[i]].hasGoldenBall = true;
        }
    }
}

function resetAirportMarkers() {
    airportMarkers.forEach(marker => {
        marker.off('click');

        if (visitedMarkers.has(marker)) {
            marker.setStyle({
                radius: 12,
                fillColor: 'red',
                color: 'white',
                weight: 2,
                fillOpacity: 0.8
            });
        } else if (marker === currentMarker) {
            marker.setStyle({
                radius: 12,
                fillColor: 'yellow',
                color: 'black',
                weight: 2,
                fillOpacity: 0.8
            });
        } else {
            marker.setStyle({
                radius: 12,
                fillColor: '#2474ff',
                color: 'white',
                weight: 2,
                fillOpacity: 0.8
            });
        }
    });
}


function movePlayerTo(airport, marker) {
    resetAirportMarkers();

    // vanha lentokenttä
    if (currentMarker) {
        visitedMarkers.add(currentMarker);
        currentMarker.setStyle({
            fillColor: 'red',
            color: 'white'
        });
    }

    currentAirport = airport;
    currentMarker = marker;

    visitedMarkers.delete(currentMarker);

    map.setView([airport.latitude_deg, airport.longitude_deg], 8); // eeppinen zoomi lentokentälle
    addMessage(`You arrived at ${airport.name} (${airport.ident})!`);
    moveSnail(); // etana liikkuu samalla kuin pelaaja

    // nykyinen lentokenttä
    currentMarker.setStyle({
        fillColor: 'yellow',
        color: 'black',
        weight: 2
    });

    if (currentAirport.hasGoldenBall) {

        // jos pallo niin aukee ikkuna
        document.getElementById(DICE_BTN_ID).disabled = true;
        addMessage(`**Golden Ball found!** Click 'Continue' to collect it.`);

        // bossi tänne kiitos
        document.getElementById("goldenBallText").textContent = "bossi tähän";
        goldenBallPopup.classList.remove("hide");

    } else {
        document.getElementById(DICE_BTN_ID).disabled = false;
    }
}

// noppa tässä
function rollDice() {
    return Math.floor(Math.random() * 6) + 1;
}

function handleMovement() {
    if (checkGameEnd()) return;

    resetAirportMarkers();

    const roll = rollDice();
    addMessage(`You rolled a **${roll}**! You can move to **${roll}** different airports.`);

    const availableMarkers = airportMarkers.filter(marker => marker !== currentMarker);

    const shuffledMarkers = availableMarkers.sort(() => 0.5 - Math.random());
    const selectableMarkers = shuffledMarkers.slice(0, roll);

    selectableMarkers.forEach(marker => {
        const airportData = marker.airportData;

        marker.setStyle({
            fillColor: '#27ba35',
            color: 'yellow',
            weight: 3
        });

        marker.off('click').on('click', function() {
            movePlayerTo(airportData, marker);
        });
    });

    // ei saatavilla olevat lentokentät
    availableMarkers.filter(marker => !selectableMarkers.includes(marker)).forEach(marker => {
        marker.setStyle({
            fillColor: '#333333',
            color: 'gray',
            fillOpacity: 0.5
        });
        marker.off('click');
    });

    // nykyinen lentokenttä
    if (currentMarker) {
        currentMarker.setStyle({
            fillColor: 'yellow',
            color: 'black'
        });
    }

    document.getElementById(DICE_BTN_ID).disabled = true;
    addMessage("Select one of the **highlighted** airports on the map to fly to.");
}

document.querySelector('.dice').innerHTML = `
    Fly to a new location: <br>
    <button id="${DICE_BTN_ID}">Roll Dice</button>
`;
document.getElementById(DICE_BTN_ID).addEventListener('click', handleMovement);

fetch("http://localhost:5000/api/airports")
    .then(res => {
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
    })
    .then(data => {
        allAirports = data; // kaikki lentokentät

        initializeGoldenBalls(allAirports);

        data.forEach(airport => {
            const marker = L.circleMarker([airport.latitude_deg, airport.longitude_deg], {
                radius: 12,
                fillColor: '#2474ff', // Default blue
                color: 'white',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            })
                .addTo(map)
                .bindPopup(`<b>${airport.ident}</b><br>${airport.name}`);

            marker.airportData = airport;
            airportMarkers.push(marker);
        });

        const randomIndex = Math.floor(Math.random() * allAirports.length);
        const startingAirport = allAirports[randomIndex];
        const startingMarker = airportMarkers[randomIndex];

        movePlayerTo(startingAirport, startingMarker);

        addMessage(`Game started! Your initial location is ${startingAirport.name}.`);

    })
    .catch(err => {
        console.error("Error loading airports:", err);
        addMessage("Failed to load airports. Ensure the Flask server is running at http://localhost:5000.");
    });

// kultasia palloja varten pohjustus
let balls = 0;
function addGoldenBall() {
    balls++;
    document.getElementById("gold-count").textContent = balls;
    checkGameEnd()
}

// joku etanapohjustus
let snailLevel = 0;
function moveSnail() {
    snailLevel++;
    document.getElementById("snail-progress").value = snailLevel;
    checkGameEnd()
    addMessage("The snail is getting closer...");
}

function checkGameEnd() {
    const goldenBalls = parseInt(document.getElementById("gold-count").innerText);
    const snailValue = parseInt(document.getElementById("snail-progress").value);

    const playedCharacter = JSON.parse(localStorage.getItem("chosenCharacter"));

    if (goldenBalls >= 5) {   // voitto
        showEndPopup("Congratulations!", "You collected enough golden balls!", "victoryscreen.html?char=" + playedCharacter);
        return true;
    }

    if (snailValue >= 10) {
        showEndPopup("Oh no!", "The snail has caught you!", "defeatscreen.html?char=" + playedCharacter);
        return true;
    }
    return false;
}

function showEndPopup(title, message, redirectUrl) {
    document.getElementById("endTitle").innerText = title;
    document.getElementById("endText").innerText = message;

    const popup = document.getElementById("endPopup");
    popup.classList.remove("hide");

    document.getElementById("continueBtn").onclick = () => {
        window.location.href = redirectUrl;
    };
}

// tekstikenttä vasemmas alakulmas pohjana mahollisille eri viesteille/tarinaelementeille
function addMessage(text) {
    const area = document.getElementById("messages");
    const p = document.createElement("p");
    p.innerHTML = text; // Use innerHTML to allow for bolding the dice roll
    area.appendChild(p);

    // scroollaa alas ( ei toimi)
    area.scrollDown = area.scrollHeight;
}

// info boxi
const popup = document.getElementById("popup");
const openBtn = document.getElementById("openPopup");
const closeBtn = document.getElementById("closePopup");

openBtn.addEventListener("click", () => {
    popup.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
    popup.style.display = "none";
});

popup.addEventListener("click", (event) => {
    if (event.target === popup) {
        popup.style.display = "none";
    }
});

const infoText = document.getElementById("popuptext");
infoText.textContent = "To win you need to banish the snail's curse. " +
    "To banish the curse you need 5 golden balls. To collect these balls you'll " +
    "have to travel through different airports looking for golden guardians whom " +
    "you'll need to face. To travel between these airports you need to throw a dice, " +
    "which will give you a random amount of locations to choose from. Throughout" +
    " these airports you can also find items that slow either you, or the snail." +
    " So be careful, and good luck!";

// for loading the map
setTimeout(() => {
    map.invalidateSize();
}, 300);
