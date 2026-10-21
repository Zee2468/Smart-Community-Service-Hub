

const typingElement = document.getElementById("typing-text");

const words = [

    "Connecting Communities Through Technology",

    "Report Community Issues Easily",

    "Track Service Delivery in Real Time",

    "Discover Jobs & Opportunities",

    "Join Community Events",

    "Building Smarter Communities Together"

];

let wordIndex = 0;
let letterIndex = 0;
let deleting = false;

function typeEffect() {

    const currentWord = words[wordIndex];

    if (!deleting) {

        typingElement.textContent =
            currentWord.substring(0, letterIndex);

        letterIndex++;

        if (letterIndex > currentWord.length) {

            deleting = true;

            setTimeout(typeEffect, 1800);

            return;
        }

    } else {

        typingElement.textContent =
            currentWord.substring(0, letterIndex);

        letterIndex--;

        if (letterIndex < 0) {

            deleting = false;

            wordIndex++;

            if (wordIndex >= words.length) {

                wordIndex = 0;

            }

        }

    }

    setTimeout(typeEffect, deleting ? 40 : 80);

}

typeEffect();



const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    const updateCounter = () => {

        const target = +counter.getAttribute("data-target");

        const current = +counter.innerText;

        const increment = Math.ceil(target / 150);

        if (current < target) {

            counter.innerText = current + increment;

            setTimeout(updateCounter, 20);

        } else {

            counter.innerText = target + "+";

        }

    };

    updateCounter();

});



const observer = new IntersectionObserver(

(entries)=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("show");

}

});

},

{

threshold:0.2

}

);

document.querySelectorAll(".animate").forEach(el=>{

observer.observe(el);

});



const cards = document.querySelectorAll(".floating-card");

cards.forEach((card,index)=>{

card.style.animationDelay=`${index*0.5}s`;

});


window.addEventListener("mousemove",(e)=>{

const x=(window.innerWidth/2-e.pageX)/80;

const y=(window.innerHeight/2-e.pageY)/80;

cards.forEach((card,index)=>{

const speed=(index+1)*0.15;

card.style.transform=
`translate(${x*speed}px,${y*speed}px)`;

});

});



document.querySelectorAll(".hero-buttons .btn").forEach(btn=>{

btn.addEventListener("mouseenter",()=>{

btn.style.transform="translateY(-6px) scale(1.05)";

});

btn.addEventListener("mouseleave",()=>{

btn.style.transform="translateY(0) scale(1)";

});

});

window.addEventListener("load",()=>{

document.querySelector(".hero-content")
.classList.add("show");

});