document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    // Fetch CSRF token from cookies
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith('csrftoken=')) {
                    cookieValue = cookie.substring(10);
                    break;
                }
            }
        }
        return cookieValue;
    }

    likeButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent form submission

            const recipeId = this.getAttribute('data-recipe-id');
            const likeUrl = this.getAttribute('data-url');
            const csrftoken = getCSRFToken();

            fetch(likeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    'recipe_id': recipeId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the like button UI
                    const likeIcon = button.querySelector('.like-icon');
                    const likeCount = button.querySelector('.like-count');

                    if (data.liked) {
                        likeIcon.textContent = '❤️'; // Liked icon
                        button.classList.add('liked');
                    } else {
                        likeIcon.textContent = '🤍'; // Unliked icon
                        button.classList.remove('liked');
                    }

                    // Update like count
                    likeCount.textContent = data.likes;
                } else {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
