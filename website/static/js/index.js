function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/like-post/${postId}`, {method: "POST"}).then((res) => res.json()).then((data) => {
        likeCount.innerHTML = data["likes"]
    }
)
}