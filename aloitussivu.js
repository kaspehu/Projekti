'use strict'

const characterCards = [
    {
        name: "Suzie Safebet",
        stats: "tähän jotain statseja vaik jos ehtii",
        image: "img/Suzie.png"
    },
    {
        name: "Malcolm Middleman",
        stats: "tähän jotain 2",
        image: "img/Malcolm.png"
    },
    {
        name: "Howard Highroller",
        stats: "tähän jotain 3",
        image: "img/Howard.png"
    }
]

// Start with null, confirm selected character later
let selectedCharacter = null;

const picturesElem = document.getElementById("pictures");

for (const pic of characterCards) {
    const articleElem = document.createElement("article");
    articleElem.classList.add("card");

    const figureElem = document.createElement("figure");

    const h3Elem = document.createElement("h3");
    h3Elem.textContent = pic.name;
    figureElem.appendChild(h3Elem);

    const imgElem = document.createElement("img");
    imgElem.src = pic.image;
    imgElem.alt = pic.name;
    figureElem.appendChild(imgElem);

    articleElem.appendChild(figureElem);

    articleElem.addEventListener("click", () => {
    selectedCharacter = pic;  // store temporarily
    confirmText.textContent = `You chose ${pic.name}. Start the game?`;
    confirmPopup.style.display = "flex";
});

    picturesElem.appendChild(articleElem);
}

const popup = document.getElementById("popup");
const openBtn = document.getElementById("openPopup");
const closeBtn = document.getElementById("closePopup");

openBtn.addEventListener("click", () => {
    popup.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
    popup.style.display = "none";
});

// Close when clicking outside the popup box
popup.addEventListener("click", (event) => {
    if (event.target === popup) {
        popup.style.display = "none";
    }
});

// voi muokata paremmaksi
const infoText = document.getElementById("popuptext");
infoText.textContent = "To win you need to banish the snail's curse. " +
    "To banish the curse you need 5 golden balls. To collect these balls you'll " +
    "have to travel through different airports looking for golden guardians whom " +
    "you'll need to face. To travel between these airports you need to throw a dice, " +
    "which will give you a random amount of locations to choose from. Throughout" +
    " these airports you can also find items that slow either you, or the snail." +
    " So be careful, and good luck!";

// Confirmation popup
const confirmPopup = document.getElementById("confirmPopup");
const confirmText = document.getElementById("confirmText");
const closeConfirm = document.getElementById("closeConfirm");
const confirmYes = document.getElementById("confirmYes");
const confirmNo = document.getElementById("confirmNo");

// Backstory popup
const storyPopup = document.getElementById("storyPopup");
const storyText = document.getElementById("storyText");
const closeStory = document.getElementById("closeStory");
const storyContinue = document.getElementById("storyContinue");

// Close with NO
confirmNo.addEventListener("click", () => {
    confirmPopup.style.display = "none";
});

// Close X
closeConfirm.addEventListener("click", () => {
    confirmPopup.style.display = "none";
});

// YES → show backstory
confirmYes.addEventListener("click", () => {
    confirmPopup.style.display = "none";
    storyText.textContent = getBackstory(selectedCharacter.name);
    storyPopup.style.display = "flex";
});

closeStory.addEventListener("click", () => {
    storyPopup.style.display = "none";
});

storyContinue.addEventListener("click", () => {
    // save chosen character
    localStorage.setItem("chosenCharacter", JSON.stringify(selectedCharacter));

    // go to main page
    window.location.href = "mainpage.html";
});

//tänne voi esim keksiä oikeita backstoryja...
function getBackstory(name) {
    switch (name) {
        case "Suzie Safebet":
            return "Suzie is an overly cautious young adult who lives her life as if it were always a moment to hide. She constantly observes her surroundings and makes decisions only after much deliberation. Her movements are slow, deliberate, and precise — as if she is trying to minimize every possible risk. When Suzie speaks, she speaks calmly, weighing each of her words carefully.";
        case "Malcolm Middleman":
            return "Malcolm is a middle-aged, chronically tired man whose life is so boring it borders on supernatural event. He is neither sad nor happy – just tired of everything. He does everything with precision, and nothing ever surprises him — because nothing ever changes. Malcolm moves through life guided by routine, avoiding social life and especially adventure. He is a master of everyday life, a semi-deity of mediocrity.";
        case "Howard Highroller":
            return "Howard is a retired casino mastermind who spent his life under the glow of gaming tables and in smoky VIP lounges. Now he is enjoying his well-earned golden years in Brazil. Though he’s left the casinos behind, his eyes still scan everything — spotting risks, hidden opportunities. He lives large, moves with effortless charm, and approaches life like a slow, steady game he intends to win purely through experience. The steady glow of a cigar and the swirl of smoke that wraps around is integral part of Howard as his confident appearance.";
        default:
            return "Your journey begins...";
    }
}

