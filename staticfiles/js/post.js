const editPostButtons = document.getElementsByClassName("btn-edit-post");
const postText = document.getElementById("id_content");
const postForm = document.getElementById("postForm");
const submitPostButton = document.getElementById("submitPostButton");


for (let button of editPostButtons) {
    button.addEventListener("click", (e) => {
        let postId = e.target.getAttribute("post_id");
        let postContent = document.getElementById(`post${postId}`).innerText;
        postText.value = postContent;
        submitPostButton.innerText = "Update";
        postForm.setAttribute("action", `edit_post/${postId}`);
    });
}