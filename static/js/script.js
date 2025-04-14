document.getElementById("upload-form").onsubmit = async function (e) {
    e.preventDefault();
    const file = document.getElementById("image").files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/detect/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const error = await response.text();
            console.error("Server error:", error);
            document.getElementById("result").innerText = "Detection failed.";
            return;
        }

        const data = await response.json();
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = "";

        data.result.forEach((imgPath) => {
            const img = document.createElement("img");
            img.src = imgPath;
            img.style.maxWidth = "200px";
            img.style.margin = "10px";
            resultDiv.appendChild(img);
        });
    } catch (err) {
        console.error("Error:", err);
        document.getElementById("result").innerText = "Error during detection.";
    }
};
