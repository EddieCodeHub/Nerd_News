const deletePostButtons = document.getElementsByClassName("btn-delete-post");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteConfirm = document.getElementById("deleteConfirm");


for (let button of deletePostButtons) {
    button.addEventListener("click", (e) => {
        let postId = e.target.getAttribute("post_id");
        deleteConfirm.href = `delete/${postId}`;
        deleteModal.show();
    });
}