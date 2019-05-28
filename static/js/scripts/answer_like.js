let answerRate = function(aid, c_type) {
    let $btn = $(this);
    let my_token = document.cookie.match(/csrftoken=([^;]*)/) && RegExp.$1;
    $.ajax({
        type: 'POST',
        url: '/answer_like/',
        data: {val: aid, csrfmiddlewaretoken: my_token, type : c_type}
    }).done(function(resp) {
        $("#answer_rating-"+aid).html(resp.val);
    }).fail(function(err){});
};


