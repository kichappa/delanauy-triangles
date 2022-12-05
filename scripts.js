const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
var svgHref = "https://api-triangles.ramdon.team/generate?xmax=";
svgHref = svgHref.concat(String(vw).concat("&ymax="));
svgHref = svgHref.concat(String(vh).concat("&density="));
svgHref = svgHref.concat(String(150));
document.getElementById("triangles-svg").src = svgHref;
// document.getElementById("vh").textContent=vh;
// document.getElementById("vw").textContent=vw;
// document.getElementById("abdc").textContent=svgHref;