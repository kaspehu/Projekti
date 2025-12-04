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
            return "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        case "Malcolm Middleman":
            return "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        case "Howard Highroller":
            return "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        default:
            return "Your journey begins...";
    }
}



