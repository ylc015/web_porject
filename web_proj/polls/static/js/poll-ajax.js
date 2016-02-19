$('#invite').click(function(){
    var user_id;
    user_id = $(this).attr("data-user_id");
    $.get('/polls/invite_user', {user_id: user_id}, function(data){
               $('#invite').hide();
    });
});
