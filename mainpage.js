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

const DICE_BTN_ID = "rollDiceBtn";// dice id
const eventPopup = document.getElementById("eventPopup");
const eventContinueBtn = document.getElementById("eventContinueBtn");


function handleEventCollection() {
    if (!currentAirport || currentAirport.eventCollected) return;

    const eventType = currentAirport.event;
    let message = "";

    switch (eventType) {
        case 'goldenBall':
            addGoldenBall();
            message = `Golden Ball collected!`;
            break;
        case 'adhesive':
            adjustSnail(-1);
            message = `Snail Adhesive collected! Snail progress reduced by 1.`;
            break;
        case 'headache':
            adjustSnail(+1);
            message = `Your head aches! Snail progress increased by 1.`;
            break;
        case 'shield':
            adjustSnail(-2);
            message = "You've aquired a snail shield, the snail slows down by 2.";
            break;
        case 'diarrhea':
            adjustSnail(+2);
            message = "A diarrhea strikes! Snail progresses by 2.";
            break;
        default:
            message = "Event resolved.";
    }

    if (eventType) {
        currentAirport.eventCollected = true;
        addMessage(`**${message}**`);
    }

    eventPopup.classList.add("hide");
    document.getElementById(DICE_BTN_ID).disabled = false;
}

eventContinueBtn.addEventListener('click', handleEventCollection);


// eventti funktio mistä tulee pallot ja buustit
function initializeEvents(airports) {
    airports.forEach(a => {
        a.event = null;
        a.eventCollected = false;
    });

    // tsäänssit
    const eventsToPlace = [
        ...Array(10).fill('goldenBall'),
        ...Array(7).fill('adhesive'),
        ...Array(7).fill('headache'),
        ...Array(3).fill('shield'),
        ...Array(3).fill('diarrhea')

    ];

    const shuffledAirports = airports.slice().sort(() => 0.5 - Math.random());

    for (let i = 0; i < eventsToPlace.length; i++) {
        const airport = shuffledAirports[i];
        if (airport) {
            airport.event = eventsToPlace[i];
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

    // jo käyty lentokenttä
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

    map.setView([airport.latitude_deg, airport.longitude_deg], 8);
    addMessage(`You arrived at ${airport.name}!`);
    moveSnail();// etana liikkuu kun  pelaaja liikkuu

    currentMarker.setStyle({
        fillColor: 'yellow',
        color: 'black',
        weight: 2
    });

    if (currentAirport.event && !currentAirport.eventCollected) {

        document.getElementById(DICE_BTN_ID).disabled = true;

        const eventType = currentAirport.event;
        let title = "Event Found!";
        let text = "You encountered an unknown object. Click 'Continue' to resolve the event.";

        // popup ikkuna tekstit tänne
        switch (eventType) {
            case 'goldenBall':
                title = "Golden Ball Found!";
                text = "bossi tähän";
                break;
            case 'adhesive':
                title = "Snail Adhesive Found!";
                text = "You found a powerful adhesive! The snail will slow down. Click 'Continue' to apply it.";
                break;
            case 'headache':
                title = "Headache acquired";
                text = "Oh no, you stumbled upon a Snail Booster! The snail will speed up. Click 'Continue' to activate it.";
                break;
            case 'shield':
                title = "Snail Shield found!"
                text = "You found a snail shield...press continue";
                break;
            case 'diarrhea':
                title = "Diarrhea acquired"
                text = "Stomach rumbles...press continue"
                break;
        }

        addMessage(`**${title}** at ${currentAirport.name}.`);

        document.getElementById("eventTitle").textContent = title;
        document.getElementById("eventText").textContent = text;
        eventPopup.classList.remove("hide");

    } else {
        document.getElementById(DICE_BTN_ID).disabled = false;
    }
}

// noppa
function rollDice() {
    return Math.floor(Math.random() * 6) + 1;
}

function handleMovement() {
    if (checkGameEnd()) return;

    resetAirportMarkers();

    const roll = rollDice();
    addMessage(`You rolled ${roll}!`);

    const availableMarkers = airportMarkers.filter(marker => marker !== currentMarker);

    const shuffledMarkers = availableMarkers.sort(() => 0.5 - Math.random());
    const selectableMarkers = shuffledMarkers.slice(0, roll);

    selectableMarkers.forEach(marker => {
        const airportData = marker.airportData;

        // nopan valitsema kenttä
        marker.setStyle({
            fillColor: '#27ba35',
            color: 'yellow',
            weight: 3
        });

        marker.off('click').on('click', function() {
            movePlayerTo(airportData, marker);
        });
    });

    availableMarkers.filter(marker => !selectableMarkers.includes(marker)).forEach(marker => {
        marker.setStyle({
            fillColor: '#333333',
            color: 'gray',
            fillOpacity: 0.5
        });
        marker.off('click');
    });

    // nylyinen lentokenttä
    if (currentMarker) {
        currentMarker.setStyle({
            fillColor: 'yellow',
            color: 'black'
        });
    }

    document.getElementById(DICE_BTN_ID).disabled = true;
    addMessage("Select one of the highlighted airports.");
}

// noppa nappi html
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

        initializeEvents(allAirports);

        // kaikki lentokentät
        data.forEach(airport => {

            const marker = L.circleMarker([airport.latitude_deg, airport.longitude_deg], {
                radius: 12,
                fillColor: '#2474ff',
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
    if (!currentAirport || !currentAirport.event || currentAirport.eventCollected) {
        adjustSnail(1);
    }
}

// boostit ja hidasteet
function adjustSnail(amount) {
    const oldValue = parseInt(document.getElementById("snail-progress").value);
    const newSnailLevel = Math.max(0, oldValue + amount); // Prevent going below 0
    snailLevel = newSnailLevel;
    document.getElementById("snail-progress").value = snailLevel;
    checkGameEnd();

    if (amount < 0) {
        addMessage(`Snail's progress decreased by ${Math.abs(amount)}.`);
    } else if (amount > 0 && amount !== 1) {
        addMessage(`Snail's progress increased by ${amount}.`);
    }
}


function checkGameEnd() {
    const goldenBalls = parseInt(document.getElementById("gold-count").innerText);
    const snailValue = parseInt(document.getElementById("snail-progress").value);

    const playedCharacter = JSON.parse(localStorage.getItem("chosenCharacter"));

    if (goldenBalls >= 5) {   // voitto ehto
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

    // Remove older messages so only 3 remain
    while (area.children.length >= 3) {
        area.removeChild(area.firstChild);
    }

    // Create and add the new message
    const p = document.createElement("p");
    p.innerHTML = text;
    area.appendChild(p);

    // Correct scroll code
    area.scrollTop = area.scrollHeight;
}

//info boxi
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
