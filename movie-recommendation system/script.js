

// let selectedMood = "";

// // ==========================
// // 🎯 MOOD BUTTON CLICK
// // ==========================
// function setMood(mood){
//     selectedMood = mood;
//     getRecommendations();
// }

// // ==========================
// // 🔍 SEARCH FUNCTION
// // ==========================
// async function getRecommendations(){

//     let movie = document.getElementById("movieInput").value.trim();
//     let results = document.getElementById("results");

//     results.innerHTML = "Loading...";

//     try{

//         let response = await fetch("http://127.0.0.1:5000/recommend", {
//             method:"POST",
//             headers:{"Content-Type":"application/json"},
//             body:JSON.stringify({
//                 movie: movie,
//                 mood: selectedMood
//             })
//         });

//         let data = await response.json();

//         if(!data || data.length === 0){
//             results.innerHTML = "No movies found";
//             return;
//         }

//         let cards = "";

//         data.forEach(m => {

//             let poster = m.poster
//                 ? `<img src="${m.poster}" class="poster">`
//                 : `<div class="no-poster">No Poster</div>`;

//             let ott = m.ott && m.ott.length
//                 ? m.ott.join(", ")
//                 : "OTT not available";

//             // 🔥 NEW: Reason + Watch Link
//             cards += `
//             <div class="movie-card">
//                 ${poster}
//                 <div class="card-content">
//                     <h3>${m.title}</h3>
//                     <p>⭐ ${m.rating}</p>
//                     <p>${m.genres}</p>

//                     ${m.reason ? `<p class="reason">💡 ${m.reason}</p>` : ""}

//                     <p>📺 ${ott}</p>

//                     ${m.link ? `<a href="${m.link}" target="_blank" class="watch-btn">▶ Watch Now</a>` : ""}
//                 </div>
//             </div>
//             `;
//         });

//         results.innerHTML = cards;

//     } catch(err){
//         results.innerHTML = "Server error";
//     }
// }

// // ==========================
// // ⌨️ ENTER KEY
// // ==========================
// document.getElementById("movieInput")
// .addEventListener("keypress", function(e){
//     if(e.key === "Enter"){
//         getRecommendations();
//     }
// });



let selectedMood = "";

// ==========================
// 🎯 MOOD BUTTON CLICK
// ==========================
function setMood(mood){
    selectedMood = mood;
    getRecommendations();
}

// ==========================
// 🔍 SEARCH FUNCTION
// ==========================
async function getRecommendations(){

    let movie = document.getElementById("movieInput").value.trim();
    let results = document.getElementById("results");

    results.innerHTML = "Loading...";

    try{

        let response = await fetch("http://127.0.0.1:5000/recommend", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                movie: movie,
                mood: selectedMood
            })
        });

        let data = await response.json();

        if(!data || data.length === 0){
            results.innerHTML = "No movies found";
            return;
        }

        let cards = "";

        data.forEach(m => {

            let ott = m.ott && m.ott.length
                ? m.ott.join(", ")
                : "OTT not available";

            // 🔥 NEW: Reason + Watch Link
            cards += `
            <div class="movie-card">
                <div class="card-content">
                    <h3>${m.title}</h3>
                    <p>⭐ ${m.rating}</p>
                    <p>${m.genres}</p>

                    ${m.reason ? `<p class="reason">💡 ${m.reason}</p>` : ""}

                    <p>📺 ${ott}</p>

                    ${m.link ? `<a href="${m.link}" target="_blank" class="watch-btn">▶ Watch Now</a>` : ""}
                </div>
            </div>
            `;
        });

        results.innerHTML = cards;

    } catch(err){
        results.innerHTML = "Server error";
    }
}

// ==========================
// ⌨️ ENTER KEY
// ==========================
document.getElementById("movieInput")
.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        getRecommendations();
    }
});