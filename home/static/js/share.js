function shareRecipe(recipeUrl) {
    if (navigator.share) {
        // If Web Share API is supported
        navigator.share({
            title: "Check out this recipe on FeastFit!",
            text: "I found an amazing recipe for you!",
            url: recipeUrl
        }).then(() => {
        }).catch((error) => {
            console.error("Error sharing:", error);
        });
    } else {
        // Fallback: Copy to clipboard
        navigator.clipboard.writeText(recipeUrl).then(() => {
            alert("Link copied to clipboard!");
        }).catch((error) => {
            console.error("Failed to copy:", error);
        });
    }
}