$('#invite').click(function(){
    var user_id;
    var req_id;
    user_id = $(this).attr("data-user_id");
    $.get('/polls/invite_user', {user_ids: [user_id, req_id]}, function(data){
               $('#invite').hide();
    });
});
