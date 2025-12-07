// Load chosen character from selection page
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

// kultasia palloja varten pohjustus
let balls = 0;
function addGoldenBall() {
    balls++;
    document.getElementById("gold-count").textContent = balls;
    checkGameEnd()
    addMessage("You've beaten the guardian, and got yourself a golden ball!'");
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

    if (goldenBalls >= 5) {   // example win condition
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

// tähän noppafunktiota??

// tekstikenttä vasemmas alakulmas pohjana mahollisille eri viesteille/tarinaelementeille
function addMessage(text) {
    const area = document.getElementById("messages");
    const p = document.createElement("p");
    p.textContent = text;
    area.appendChild(p);
    area.scrollTop = area.scrollHeight;
}

// game info box
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