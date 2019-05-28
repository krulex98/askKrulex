let questionRate = function(qid, c_type) {
    let $btn = $(this);
    let my_token = document.cookie.match(/csrftoken=([^;]*)/) && RegExp.$1;
    $.ajax({
        type: 'POST',
        url: '/question_like/',
        data: {val: qid, csrfmiddlewaretoken: my_token, type : c_type}
    }).done(function(resp) {
        $("#question_rating-"+qid).html(resp.val);
    }).fail(function(err){});
};

