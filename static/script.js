async function buscarVideo() {
    const url = document.getElementById("url").value;

    const res = await fetch("/info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    });

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById("preview").innerHTML = `
        <h3>${data.title}</h3>
        <img src="${data.thumbnail}" width="100%">
    `;

    const select = document.getElementById("formats");
    select.innerHTML = "";

    data.formats.forEach(f => {
        const option = document.createElement("option");
        option.value = f.format_id;
        option.text = `${f.quality} (${f.ext})`;
        select.appendChild(option);
    });

    document.getElementById("hiddenUrl").value = url;
}