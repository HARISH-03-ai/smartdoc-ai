

function showFiles(files) {

    let preview = document.getElementById("file-preview");

    preview.innerHTML = "";

    if (files.length > 0) {
        document.getElementById("upload-btn").style.display = "block";
    }

    for (let i = 0; i < files.length; i++) {

        let file = files[i];

        let size = file.size < 1024 * 1024
            ? (file.size / 1024).toFixed(1) + " KB"
            : (file.size / 1024 / 1024).toFixed(1) + " MB";

        preview.innerHTML += `
                
                <div class="file-box">

                    <div class="file-name">
                        ${file.name}
                    </div>

                    <div class="file-size">
                        ${size}
                    </div>

                </div>
                `;
    }
}

function showThinking() {
    document.getElementById("thinking").style.display = "flex";
}