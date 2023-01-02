document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.edit-view').forEach(function (edit_view) {
        edit_view.style.display = 'none';
    });
    document.querySelectorAll('.save-button').forEach(function (button) {
        button.style.display = 'none';
        button.addEventListener('click', save_new_content);
    });

    // press like button, do this 
    document.querySelectorAll('.like-button').forEach(function (button) {
        button.addEventListener('click', like);
    })

    // press unlike button, do this 
    document.querySelectorAll('.unlike-button').forEach(function (button) {
        button.addEventListener('click', like)
    })

    // if submit the form, do this 
    document.querySelectorAll('.edit-form').forEach(function (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const post = form.parentElement.parentElement;
            edit_post(post);
        });
    })

})

function edit_post(post) {
    // const post = this.parentElement;

    const post_content_view = post.querySelector('.post-content-view');
    const edit_view = post.querySelector('.edit-view');
    const save_button = post.querySelector('.save-button');
    const edit_button = post.querySelector('.edit-button');

    post_content_view.style.display = 'none';
    edit_button.style.display = 'none';
    edit_view.style.display = 'block';
    save_button.style.display = 'block';
}

function save_new_content() {

    const post = this.parentElement.parentElement;
    const form = post.querySelector("form");
    const csrf_token = form.querySelector('input').value;

    // get new content
    const new_content = post.querySelector('.new-content').value;
    const post_id = post.querySelector('.hidden-post-id').value;

    const post_content_view = post.querySelector('.post-content-view');
    const edit_view = post.querySelector('.edit-view');
    const save_button = post.querySelector('.save-button');
    const edit_button = post.querySelector('.edit-button');

    // console.log(post_id);
    // console.log(new_content);

    // update post content
    fetch(`/post/${post_id}`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrf_token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: new_content
        })
    })
        .then(() => {
            // after updating new content, do this 
            post_content_view.innerHTML = new_content;

            post_content_view.style.display = 'block';
            edit_button.style.display = 'block';
            edit_view.style.display = 'none';
            save_button.style.display = 'none';
        })
}

function like() {

    const post = this.parentElement.parentElement;
    const post_id = post.querySelector('.hidden-post-id').value;
    const like_numbers_element = post.querySelector('.like-numbers');
    const like_numbers = parseInt(like_numbers_element.innerHTML);
    const button = this;

    if (button.classList.contains("like-button")) {
        fetch(`/post/${post_id}/like`)
            .then(response => response.json())
            .then(result => {
                console.log(result)

                button.classList.remove("like-button");
                button.classList.add("unlike-button");
                button.innerHTML = 'unlike';
                like_numbers_element.innerHTML = like_numbers + 1;

            })
    } else if (button.classList.contains("unlike-button")) {
        fetch(`/post/${post_id}/unlike`)
            .then(response => response.json())
            .then(result => {
                console.log(result)

                button.classList.remove("unlike-button");
                button.classList.add("like-button");
                button.innerHTML = 'like';
                like_numbers_element.innerHTML = like_numbers - 1;
            })
    }

}
