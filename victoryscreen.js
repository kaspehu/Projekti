'use strict'

const player = JSON.parse(localStorage.getItem("chosenCharacter"));

const img = document.getElementById("main-img")

if (!player) {
    img.src = "img/MadSnail.png";
} else if (player.name === "Suzie Safebet") {
    img.src = "img/SuzieWin.png";
} else if (player.name === "Malcolm Middleman") {
    img.src = "img/MalcolmWin.png";
} else {
    img.src = "img/HowardWin.png";
}

const clickBtn = document.getElementById("next-btn");
clickBtn.addEventListener("click", () => {
    window.location.href = "aloitussivu.html";
});

