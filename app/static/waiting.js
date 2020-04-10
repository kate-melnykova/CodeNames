$(document).ready(function(){
    loadState();
});

function loadState() {
    window.setTimeout(function(){
        $.ajax({
            url: '/waiting',
            method: 'POST',
            dataType: 'json',
            success: function(result){
                if (result.url){
                    window.location.href = result.url;
                } else {
                    console.log(result);
                    $('#user_list').html(
                        'Currently in the game: ' + result.users.join(', ')
                    );
                    loadState();
                }
            },
        });
    }, 2000);
}
