
document.addEventListener("DOMContentLoaded", function () {
    // Handle Like Button Click
    document.querySelectorAll(".like-button").forEach(button => {
        button.addEventListener("click", function () {
            let recipeId = this.getAttribute("data-recipe-id");
            let url = this.getAttribute("data-url");
            let likeCountSpan = this.querySelector(".like-count");
            let likeIcon = this.querySelector(".like-icon");
            let isLiked = this.classList.contains("liked");

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ liked: !isLiked })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle("liked");
                    likeIcon.innerHTML = data.liked ? "❤️" : "🤍";
                    likeCountSpan.innerText = data.likes;
                }
            });
        });
    });

    // Handle Save Button Click
    document.querySelectorAll(".save-button").forEach(button => {
        button.addEventListener("click", function () {
            let recipeId = this.getAttribute("data-recipe-id");
            let url = this.getAttribute("data-url");

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle("saved");
                    this.innerHTML = data.saved ? '<i class="fas fa-bookmark"></i> Saved' : '<i class="fas fa-bookmark"></i> Save';
                }
            });
        });
    });

    // Function to get CSRF Token
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
