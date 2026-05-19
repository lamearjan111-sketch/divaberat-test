const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

async function fetchPoints() {
    const response = await fetch("/points");
    const points = await response.json();

    draw(points);
}

function draw(points) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const point of points) {
        ctx.beginPath();

        ctx.arc(point.x, point.y, 6, 0, Math.PI * 2);

        ctx.fillStyle = "dodgerblue";
        ctx.fill();

        ctx.closePath();
    }
}

async function addPoint() {
    const x = parseInt(document.getElementById("xInput").value);
    const y = parseInt(document.getElementById("yInput").value);

    await fetch("/points", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ x, y })
    });

    fetchPoints();
}

fetchPoints();