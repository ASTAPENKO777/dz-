function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).on('click', '.add-comment', function() {
    const postId = $(this).data('post-id');
    const input = $(`.comment-input[data-post-id="${postId}"]`);
    const text = input.val().trim();
    
    if (!text) {
        alert('Please enter comment text');
        return;
    }
    
    $.ajax({
        url: '/add_comment/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            post_id: postId,
            text: text
        }),
        success: function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            const commentsList = $(`#comments-list-${postId}`);
            const emptyItem = commentsList.find('li:contains("No comments yet.")');
            
            if (emptyItem.length > 0) {
                emptyItem.remove();
            }
            
            commentsList.append(`
                <li class="list-group-item comment-item" id="comment-${response.id}">
                    <span class="comment-text">${response.text}</span>
                    <button class="btn btn-sm btn-outline-danger delete-comment" 
                            data-id="${response.id}">
                        Delete
                    </button>
                </li>
            `);
            
            $(`#comments-count-${postId}`).text(response.comments_count);
            
            input.val('');
        },
        error: function(xhr, status, error) {
            alert('Error adding comment: ' + error);
        }
    });
});

$(document).on('keypress', '.comment-input', function(e) {
    if (e.which === 13) { 
        const postId = $(this).data('post-id');
        $(`.add-comment[data-post-id="${postId}"]`).click();
    }
});

$(document).on('click', '.delete-comment', function() {
    const commentId = $(this).data('id');
    const button = $(this);
    
    if (!confirm('Are you sure you want to delete this comment?')) {
        return;
    }
    
    $.ajax({
        url: `/delete_comment/${commentId}/`,
        method: 'POST',
        success: function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            $(`#comment-${commentId}`).remove();
            
            const commentElement = button.closest('.card-body');
            const postId = commentElement.find('.like-button').data('id');
            $(`#comments-count-${postId}`).text(response.comments_count);
            
            const commentsList = $(`#comments-list-${postId}`);
            if (commentsList.children().length === 0) {
                commentsList.append('<li class="list-group-item text-muted">No comments yet. Be the first to comment!</li>');
            }
        },
        error: function(xhr, status, error) {
            alert('Error deleting comment: ' + error);
        }
    });
});

$(document).on('click', '.like-button', function() {
    const postId = $(this).data('id');
    
    $.ajax({
        url: `/like_post/${postId}/`,
        method: 'POST',
        success: function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            $(`#likes-count-${postId}`).text(response.likes);
            $(`#dislikes-count-${postId}`).text(response.dislikes);
        },
        error: function(xhr, status, error) {
            alert('Error liking post: ' + error);
        }
    });
});

$(document).on('click', '.dislike-button', function() {
    const postId = $(this).data('id');
    
    $.ajax({
        url: `/dislike_post/${postId}/`,
        method: 'POST',
        success: function(response) {
            if (response.error) {
                alert(response.error);
                return;
            }
            
            $(`#likes-count-${postId}`).text(response.likes);
            $(`#dislikes-count-${postId}`).text(response.dislikes);
        },
        error: function(xhr, status, error) {
            alert('Error disliking post: ' + error);
        }
    });
});